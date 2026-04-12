from __future__ import annotations

import copy
import csv
import json
import os
import platform
import re
import shlex
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

from scripts.skills.export_skill_registry import build_registry as build_dynamic_registry


ROOT = Path(__file__).resolve().parents[1]
REGISTRY_DIR = ROOT / "registry"
EXAMPLES_DIR = ROOT / "examples"
SESSION_FILES = {
    "request": "request.json",
    "plans": "plans.json",
    "review": "review.json",
    "approved_plan": "approved-plan.json",
    "execution_draft": "execution-draft.json",
    "run": "run.json",
    "run_status": "run-status.json",
    "run_review": "run-review.json",
    "history": "history.json",
    "session": "session.json",
}


def _slugify(text: str) -> str:
    value = re.sub(r"[^a-zA-Z0-9]+", "-", text.strip().lower()).strip("-")
    return value or "request"


def _load_yaml(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        payload = yaml.safe_load(handle) or {}
    if not isinstance(payload, dict):
        raise ValueError(f"Expected mapping at {path}")
    return payload


def _load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)
    if not isinstance(payload, dict):
        raise ValueError(f"Expected mapping at {path}")
    return payload


def load_structured_file(path: Path) -> dict[str, Any]:
    suffix = path.suffix.lower()
    if suffix == ".json":
        return _load_json(path)
    if suffix in {".yaml", ".yml"}:
        return _load_yaml(path)
    raise ValueError(f"Unsupported structured file format: {path}")


def _load_markdown_plan(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    matches = re.findall(r"```(?:yaml|yml)\n(.*?)```", text, flags=re.DOTALL)
    if not matches:
        raise ValueError(f"Expected a fenced yaml block in markdown plan file: {path}")

    payload = yaml.safe_load(matches[-1]) or {}
    if not isinstance(payload, dict):
        raise ValueError(f"Expected mapping in markdown plan yaml block: {path}")
    return payload


def load_plan_document(path: Path) -> dict[str, Any]:
    suffix = path.suffix.lower()
    if suffix == ".md":
        return _load_markdown_plan(path)
    return load_structured_file(path)


def save_json(payload: dict[str, Any], output_path: Path | None = None) -> str:
    text = json.dumps(payload, indent=2, ensure_ascii=False) + "\n"
    if output_path is not None:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(text, encoding="utf-8")
    return text


def _now_iso() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def _resolve_repo_path(raw_path: str | None) -> Path | None:
    value = str(raw_path or "").strip()
    if not value:
        return None
    path = Path(value)
    if path.is_absolute():
        return path
    return (ROOT / path).resolve()


def _session_file(session_dir: Path, artifact_key: str) -> Path:
    try:
        file_name = SESSION_FILES[artifact_key]
    except KeyError as exc:
        raise KeyError(f"Unknown session artifact key: {artifact_key}") from exc
    return session_dir / file_name


def _load_optional_structured_file(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    return load_structured_file(path)


def _yaml_block(payload: dict[str, Any]) -> str:
    return yaml.safe_dump(
        payload,
        sort_keys=False,
        allow_unicode=True,
        width=4096,
    ).strip()


def _ensure_session_directory(
    session_dir: Path,
    require_empty: bool = False,
    must_exist: bool = False,
) -> Path:
    session_dir = session_dir.resolve()
    if must_exist:
        if not session_dir.exists():
            raise FileNotFoundError(f"Session directory does not exist: {session_dir}")
    else:
        session_dir.mkdir(parents=True, exist_ok=True)

    if require_empty and any(session_dir.iterdir()):
        raise FileExistsError(f"Session directory is not empty: {session_dir}")

    return session_dir


def _parse_skill_runtime_metadata(skill_doc_path: Path | None) -> dict[str, Any]:
    if skill_doc_path is None or not skill_doc_path.exists():
        return {}

    command = ""
    local_executable = ""
    install_hint = ""
    for raw_line in skill_doc_path.read_text(encoding="utf-8", errors="ignore").splitlines():
        line = raw_line.strip()
        if line.startswith("- **Command"):
            matches = re.findall(r"`([^`]+)`", line)
            if matches:
                command = matches[0].strip()
        elif line.startswith("- **Local executable"):
            matches = re.findall(r"`([^`]+)`", line)
            if matches:
                local_executable = matches[0].strip()
        elif line.startswith("- **Install hint"):
            matches = re.findall(r"`([^`]+)`", line)
            if matches:
                install_hint = matches[0].strip()
            else:
                install_hint = line.split(":", 1)[-1].strip()

    return {
        "command": command or None,
        "local_executable": local_executable or None,
        "install_hint": install_hint or None,
    }


def _load_session_bundle(session_dir: Path) -> dict[str, Any]:
    resolved = session_dir.resolve()
    if not resolved.exists():
        raise FileNotFoundError(f"Session directory does not exist: {resolved}")

    bundle: dict[str, Any] = {}
    for artifact_key in SESSION_FILES:
        payload = _load_optional_structured_file(_session_file(resolved, artifact_key))
        if payload is not None:
            bundle[artifact_key] = payload

    if "request" not in bundle and "plans" in bundle:
        request = bundle["plans"].get("request")
        if isinstance(request, dict):
            bundle["request"] = request

    return bundle


def _ensure_history_payload(bundle: dict[str, Any], session_dir: Path) -> dict[str, Any]:
    payload = bundle.get("history")
    events: list[dict[str, Any]] = []
    if isinstance(payload, dict):
        raw_events = payload.get("events", [])
        if isinstance(raw_events, list):
            events = [dict(item) for item in raw_events if isinstance(item, dict)]

    return {
        "session_id": session_dir.name,
        "events": events,
    }


def _append_history_event(
    bundle: dict[str, Any],
    session_dir: Path,
    *,
    event_type: str,
    message: str,
    data: dict[str, Any] | None = None,
) -> dict[str, Any]:
    history = _ensure_history_payload(bundle, session_dir)
    event = {
        "event_id": f"evt_{len(history['events']) + 1:04d}",
        "timestamp": _now_iso(),
        "type": event_type,
        "message": message,
    }
    if data:
        event["data"] = data
    history["events"].append(event)
    bundle["history"] = history
    return event


def _latest_history_event(events: list[dict[str, Any]]) -> dict[str, Any] | None:
    return events[-1] if events else None


def _latest_event_of_type(events: list[dict[str, Any]], event_type: str) -> dict[str, Any] | None:
    for event in reversed(events):
        if event.get("type") == event_type:
            return event
    return None


def _diff_string_list(before: list[Any] | None, after: list[Any] | None) -> dict[str, list[str]]:
    before_values = {str(item) for item in (before or [])}
    after_values = {str(item) for item in (after or [])}
    return {
        "added": sorted(after_values - before_values),
        "removed": sorted(before_values - after_values),
    }


def _has_list_diff(diff_payload: dict[str, list[str]]) -> bool:
    return bool(diff_payload.get("added") or diff_payload.get("removed"))


def build_plan_diff_summary(
    baseline_plan: dict[str, Any] | None,
    candidate_plan: dict[str, Any],
) -> dict[str, Any]:
    if baseline_plan is None:
        return {
            "baseline_plan_id": None,
            "target_plan_id": candidate_plan.get("plan_id"),
            "changed": False,
            "change_count": 0,
            "changed_fields": [],
            "list_changes": {},
            "stage_changes": [],
            "added_stage_ids": [],
            "removed_stage_ids": [],
            "summary_lines": [],
        }

    changed_fields: list[dict[str, Any]] = []
    list_changes: dict[str, dict[str, list[str]]] = {}
    stage_changes: list[dict[str, Any]] = []
    summary_lines: list[str] = []

    for field in ("title", "summary", "strategy_type"):
        before_value = baseline_plan.get(field)
        after_value = candidate_plan.get(field)
        if before_value != after_value:
            changed_fields.append(
                {
                    "field": field,
                    "before": before_value,
                    "after": after_value,
                }
            )
            summary_lines.append(f"Changed `{field}`.")

    for field in ("assumptions", "prerequisites", "expected_outputs", "risks"):
        diff_payload = _diff_string_list(
            list(baseline_plan.get(field, [])),
            list(candidate_plan.get(field, [])),
        )
        if _has_list_diff(diff_payload):
            list_changes[field] = diff_payload
            summary_lines.append(f"Updated `{field}` entries.")

    baseline_stage_map = {
        str(stage["stage_id"]): dict(stage)
        for stage in baseline_plan.get("stages", [])
        if isinstance(stage, dict) and "stage_id" in stage
    }
    candidate_stage_map = {
        str(stage["stage_id"]): dict(stage)
        for stage in candidate_plan.get("stages", [])
        if isinstance(stage, dict) and "stage_id" in stage
    }

    added_stage_ids = sorted(set(candidate_stage_map) - set(baseline_stage_map))
    removed_stage_ids = sorted(set(baseline_stage_map) - set(candidate_stage_map))

    if added_stage_ids:
        summary_lines.append(f"Added stages: {', '.join(added_stage_ids)}.")
    if removed_stage_ids:
        summary_lines.append(f"Removed stages: {', '.join(removed_stage_ids)}.")

    for stage_id in sorted(set(candidate_stage_map).intersection(baseline_stage_map)):
        before_stage = baseline_stage_map[stage_id]
        after_stage = candidate_stage_map[stage_id]
        stage_change: dict[str, Any] = {"stage_id": stage_id}
        stage_changed = False

        for field in ("name", "goal", "requires_user_confirmation"):
            before_value = before_stage.get(field)
            after_value = after_stage.get(field)
            if before_value != after_value:
                stage_change[field] = {
                    "before": before_value,
                    "after": after_value,
                }
                stage_changed = True

        for field in ("candidate_skills", "outputs", "validation"):
            diff_payload = _diff_string_list(
                list(before_stage.get(field, [])),
                list(after_stage.get(field, [])),
            )
            if _has_list_diff(diff_payload):
                stage_change[field] = diff_payload
                stage_changed = True

        if stage_changed:
            stage_changes.append(stage_change)
            summary_lines.append(f"Updated stage `{stage_id}`.")

    change_count = (
        len(changed_fields)
        + len(list_changes)
        + len(stage_changes)
        + len(added_stage_ids)
        + len(removed_stage_ids)
    )

    return {
        "baseline_plan_id": baseline_plan.get("plan_id"),
        "target_plan_id": candidate_plan.get("plan_id"),
        "changed": change_count > 0,
        "change_count": change_count,
        "changed_fields": changed_fields,
        "list_changes": list_changes,
        "stage_changes": stage_changes,
        "added_stage_ids": added_stage_ids,
        "removed_stage_ids": removed_stage_ids,
        "summary_lines": summary_lines,
    }


def _baseline_plan_for_approval(bundle: dict[str, Any], approved_plan: dict[str, Any]) -> dict[str, Any] | None:
    current_approved = bundle.get("approved_plan")
    if isinstance(current_approved, dict) and current_approved.get("plan_id") == approved_plan.get("plan_id"):
        return copy.deepcopy(current_approved)

    plans_payload = bundle.get("plans")
    if isinstance(plans_payload, dict):
        for plan in plans_payload.get("plans", []):
            if isinstance(plan, dict) and plan.get("plan_id") == approved_plan.get("plan_id"):
                return copy.deepcopy(plan)

    return None


def _build_session_manifest(session_dir: Path, bundle: dict[str, Any]) -> dict[str, Any]:
    existing_manifest = dict(bundle.get("session", {}))
    request = dict(bundle.get("request", {}))
    proposals = dict(bundle.get("plans", {}))
    review = dict(bundle.get("review", {}))
    approved_plan = dict(bundle.get("approved_plan", {}))
    run_status = dict(bundle.get("run_status", {}))
    run_review = dict(bundle.get("run_review", {}))
    history = _ensure_history_payload(bundle, session_dir)
    events = list(history.get("events", []))
    latest_event = _latest_history_event(events)
    latest_approval = _latest_event_of_type(events, "plan_approved")

    available_plan_ids = [
        str(plan["plan_id"])
        for plan in proposals.get("plans", [])
        if isinstance(plan, dict) and "plan_id" in plan
    ]

    files = {
        artifact_key: SESSION_FILES[artifact_key]
        for artifact_key in SESSION_FILES
        if artifact_key in bundle
    }
    files["session"] = SESSION_FILES["session"]

    status = "awaiting_plan_selection"
    next_action = "Review candidate plans and approve one."
    if review.get("recommended_plan_id"):
        next_action = (
            f"Review candidate plans. Recommended plan: {review['recommended_plan_id']}."
        )

    approved_plan_id = approved_plan.get("plan_id")
    current_stage = None
    if approved_plan_id:
        status = "plan_approved"
        next_action = "Inspect the execution draft and initialize or continue the run."

    if run_status:
        current_stage = run_status.get("current_stage")
        run_state = str(run_status.get("status", "pending"))
        if run_state == "completed":
            status = "completed"
        elif run_state == "paused":
            if run_review.get("verdict") == "awaiting_confirmation":
                status = "awaiting_confirmation"
            else:
                status = "paused"
        elif run_state == "failed":
            status = "failed"
        else:
            status = "run_active"
        next_action = run_status.get("next_action", next_action)

    return {
        "session_id": existing_manifest.get("session_id", session_dir.name),
        "session_dir": str(session_dir),
        "request_id": request.get("request_id"),
        "status": status,
        "available_plan_ids": available_plan_ids,
        "recommended_plan_id": review.get("recommended_plan_id"),
        "approved_plan_id": approved_plan_id,
        "current_stage": current_stage,
        "run_status": run_status.get("status"),
        "run_verdict": run_review.get("verdict"),
        "next_action": next_action,
        "history_event_count": len(events),
        "latest_event_type": latest_event.get("type") if latest_event else None,
        "latest_event_timestamp": latest_event.get("timestamp") if latest_event else None,
        "latest_approval_reason": (
            latest_approval.get("data", {}).get("reason") if latest_approval else None
        ),
        "latest_plan_change_count": (
            latest_approval.get("data", {}).get("plan_diff", {}).get("change_count")
            if latest_approval
            else None
        ),
        "files": files,
        "created_at": existing_manifest.get("created_at", _now_iso()),
        "updated_at": _now_iso(),
    }


def _find_plan_by_id(plans_payload: dict[str, Any], plan_id: str) -> dict[str, Any]:
    for plan in plans_payload.get("plans", []):
        if isinstance(plan, dict) and plan.get("plan_id") == plan_id:
            return copy.deepcopy(plan)
    raise KeyError(f"Unknown session plan_id: {plan_id}")


def _pick_session_plan(bundle: dict[str, Any], plan_id: str | None = None, approved: bool = False) -> dict[str, Any]:
    if approved:
        approved_plan = bundle.get("approved_plan")
        if not isinstance(approved_plan, dict):
            raise FileNotFoundError("Session does not contain an approved plan yet.")
        return copy.deepcopy(approved_plan)

    plans_payload = bundle.get("plans")
    if not isinstance(plans_payload, dict):
        raise FileNotFoundError("Session does not contain plans.json.")

    if plan_id is not None:
        return _find_plan_by_id(plans_payload, plan_id)

    review = bundle.get("review")
    if isinstance(review, dict) and review.get("recommended_plan_id"):
        return _find_plan_by_id(plans_payload, str(review["recommended_plan_id"]))

    plans = [plan for plan in plans_payload.get("plans", []) if isinstance(plan, dict)]
    if not plans:
        raise ValueError("Session plans.json does not contain any candidate plans.")
    return copy.deepcopy(plans[0])


def render_plan_markdown(
    plan: dict[str, Any],
    *,
    session_manifest: dict[str, Any] | None = None,
) -> str:
    stages = list(plan.get("stages", []))
    stage_lines = []
    for index, stage in enumerate(stages, start=1):
        candidate_skills = ", ".join(str(item) for item in stage.get("candidate_skills", [])) or "-"
        validation = ", ".join(str(item) for item in stage.get("validation", [])) or "-"
        confirmation = "yes" if stage.get("requires_user_confirmation", False) else "no"
        stage_lines.append(
            "\n".join(
                [
                    f"{index}. `{stage.get('stage_id', f's{index}')}` {stage.get('name', 'unnamed-stage')}",
                    f"   - goal: {stage.get('goal', '')}",
                    f"   - confirmation: {confirmation}",
                    f"   - candidate_skills: {candidate_skills}",
                    f"   - validation: {validation}",
                ]
            )
        )

    context_lines = []
    if session_manifest is not None:
        context_lines.extend(
            [
                f"- Session ID: `{session_manifest.get('session_id', '')}`",
                f"- Session dir: `{session_manifest.get('session_dir', '')}`",
                f"- Recommended plan: `{session_manifest.get('recommended_plan_id', '')}`",
            ]
        )
    context_lines.extend(
        [
            f"- Plan ID: `{plan.get('plan_id', '')}`",
            f"- Request ID: `{plan.get('request_id', '')}`",
            f"- Workflow: `{plan.get('source_workflow_id', 'n/a')}`",
            f"- Strategy: `{plan.get('strategy_type', '')}`",
            f"- Approval state: `{plan.get('approval_state', '')}`",
        ]
    )

    stage_outline = "\n".join(stage_lines) if stage_lines else "No stages defined."
    yaml_block = _yaml_block(plan)

    return "\n".join(
        [
            "# Bio Agent Plan Editor",
            "",
            "这个 Markdown 文件是给人和 agent 共用的计划编辑视图。",
            "修改时，优先编辑下面的 YAML 代码块；提交回系统时会从该代码块回读完整计划。",
            "",
            "## Context",
            *context_lines,
            "",
            "## Summary",
            f"- Title: {plan.get('title', '')}",
            f"- Summary: {plan.get('summary', '')}",
            f"- Risks: {len(plan.get('risks', []))}",
            f"- Stage count: {len(stages)}",
            "",
            "## Stage Outline",
            stage_outline,
            "",
            "## Editable Plan YAML",
            "```yaml",
            yaml_block,
            "```",
            "",
            "## Apply Back",
            "使用下面的命令把编辑后的 Markdown 重新批准进 session：",
            "",
            "```bash",
            "python3 scripts/bio_skill_system.py session-approve \\",
            "  --session-dir <session-dir> \\",
            f"  --plan-file {session_manifest.get('session_dir', '<session-dir>') + '/editable-plan.md' if session_manifest else '<edited-plan.md>'}",
            "```",
            "",
        ]
    )


def _sync_session_bundle(session_dir: Path, bundle: dict[str, Any]) -> dict[str, Any]:
    session_dir = session_dir.resolve()
    synced = copy.deepcopy(bundle)
    synced["history"] = _ensure_history_payload(synced, session_dir)

    if "request" not in synced and "plans" in synced:
        request = synced["plans"].get("request")
        if isinstance(request, dict):
            synced["request"] = request

    if "plans" in synced:
        synced["review"] = review_plans(synced["plans"])

    if "run" in synced:
        execution_draft = synced.get("execution_draft")
        synced["run_status"] = summarize_run(synced["run"])
        synced["run_review"] = review_run(
            synced["run"],
            execution_draft=execution_draft if isinstance(execution_draft, dict) else None,
        )

    synced["session"] = _build_session_manifest(session_dir, synced)

    for artifact_key, file_name in SESSION_FILES.items():
        if artifact_key not in synced:
            continue
        save_json(synced[artifact_key], session_dir / file_name)

    return synced


def load_workflow_registry() -> dict[str, Any]:
    return _load_yaml(REGISTRY_DIR / "workflows.yaml")


def load_routing_rules() -> dict[str, Any]:
    return _load_yaml(REGISTRY_DIR / "routing_rules.yaml")


def load_static_skill_registry() -> dict[str, Any]:
    return _load_yaml(REGISTRY_DIR / "skills.yaml")


def load_workflow_knowledge() -> dict[str, Any]:
    return _load_yaml(REGISTRY_DIR / "workflow_knowledge.yaml")


def load_analysis_flows() -> dict[str, Any]:
    return _load_yaml(REGISTRY_DIR / "analysis_flows.yaml")


def load_benchmark_registry() -> dict[str, Any]:
    return _load_yaml(REGISTRY_DIR / "benchmarks.yaml")


def load_execution_bridge_registry() -> dict[str, Any]:
    return _load_yaml(REGISTRY_DIR / "execution_bridges.yaml")


def load_skill_crystallization_registry() -> dict[str, Any]:
    return _load_yaml(REGISTRY_DIR / "skill_crystallization.yaml")


def _execution_bridge_contract(workflow_id: str | None, strategy_profile: str | None, stage_id: str) -> dict[str, Any]:
    if not workflow_id:
        return {"stage_id": stage_id, "contract_defined": False}

    workflow_record = next(
        (item for item in load_execution_bridge_registry().get("workflows", []) if str(item.get("workflow_id")) == str(workflow_id)),
        None,
    )
    if not isinstance(workflow_record, dict):
        return {
            "workflow_id": workflow_id,
            "selected_strategy_profile": strategy_profile,
            "stage_id": stage_id,
            "contract_defined": False,
        }

    merged: dict[str, Any] = {}
    default_stage = dict(workflow_record.get("default_stages", {}).get(stage_id, {}))
    if default_stage:
        merged.update(default_stage)
    if strategy_profile:
        strategy_stage = dict(workflow_record.get("strategies", {}).get(str(strategy_profile), {}).get(stage_id, {}))
        if strategy_stage:
            merged.update(strategy_stage)

    if not merged:
        return {
            "workflow_id": workflow_id,
            "selected_strategy_profile": strategy_profile,
            "stage_id": stage_id,
            "contract_defined": False,
        }

    return {
        "workflow_id": workflow_id,
        "selected_strategy_profile": strategy_profile,
        "stage_id": stage_id,
        "contract_defined": True,
        "bridge_id": merged.get("bridge_id"),
        "bridge_type": merged.get("bridge_type"),
        "execution_mode": merged.get("execution_mode"),
        "required_tools": list(merged.get("required_tools", [])),
        "comparator_supported": bool(merged.get("comparator_supported", False)),
        "reproducibility_support": merged.get("reproducibility_support"),
    }


def _materialize_execution_bridge(
    workflow_id: str | None,
    strategy_profile: str | None,
    stage_id: str,
    skill_map: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    contract = _execution_bridge_contract(workflow_id, strategy_profile, stage_id)
    required_tool_refs: list[dict[str, Any]] = []
    unresolved_required_tools: list[str] = []
    missing_local_tools: list[str] = []

    for tool_id in contract.get("required_tools", []):
        ref = _resolve_skill_ref(str(tool_id), skill_map)
        required_tool_refs.append(ref)
        if not ref.get("resolved", False):
            unresolved_required_tools.append(str(tool_id))
        elif ref.get("runtime_kind") == "tool" and not ref.get("runtime_available", False):
            missing_local_tools.append(str(tool_id))

    return {
        **contract,
        "required_tool_refs": required_tool_refs,
        "unresolved_required_tools": sorted(set(unresolved_required_tools)),
        "missing_local_tools": sorted(set(missing_local_tools)),
        "ready_on_this_machine": bool(contract.get("contract_defined")) and not unresolved_required_tools and not missing_local_tools,
    }


def analysis_flow_for_workflow(workflow_id: str | None) -> dict[str, Any] | None:
    if not workflow_id:
        return None
    for flow in load_analysis_flows().get("flows", []):
        if str(flow.get("workflow_id")) == str(workflow_id):
            return copy.deepcopy(flow)
    return None


def benchmark_definition(benchmark_id: str) -> dict[str, Any]:
    for benchmark in load_benchmark_registry().get("benchmarks", []):
        if str(benchmark.get("id")) == str(benchmark_id):
            return copy.deepcopy(benchmark)
    raise KeyError(f"Unknown benchmark_id: {benchmark_id}")


def benchmark_task_definition(benchmark_id: str, task_id: str) -> tuple[dict[str, Any], dict[str, Any]]:
    benchmark = benchmark_definition(benchmark_id)
    for task in benchmark.get("tasks", []):
        if str(task.get("task_id")) == str(task_id):
            return benchmark, copy.deepcopy(task)
    raise KeyError(f"Unknown task_id `{task_id}` for benchmark `{benchmark_id}`")


def resolve_benchmark_task_payload(task_payload: dict[str, Any]) -> dict[str, Any]:
    benchmark_id = str(task_payload.get("benchmark_id") or "").strip()
    task_id = str(task_payload.get("task_id") or "").strip()
    if benchmark_id and task_id:
        benchmark, task = benchmark_task_definition(benchmark_id, task_id)
        return {
            "benchmark_id": benchmark.get("id"),
            **task,
            **copy.deepcopy(task_payload),
        }
    return copy.deepcopy(task_payload)


def benchmark_task_records(benchmark_id: str | None = None) -> list[dict[str, Any]]:
    benchmarks = load_benchmark_registry().get("benchmarks", [])
    records: list[dict[str, Any]] = []
    for benchmark in benchmarks:
        if benchmark_id and str(benchmark.get("id")) != str(benchmark_id):
            continue
        for task in benchmark.get("tasks", []):
            records.append(
                {
                    "benchmark_id": benchmark.get("id"),
                    "benchmark_title": benchmark.get("title"),
                    "benchmark_type": benchmark.get("benchmark_type"),
                    "benchmark_metrics": list(benchmark.get("key_metrics", [])),
                    **copy.deepcopy(task),
                }
            )
    return records


def benchmark_report(benchmark_id: str | None = None) -> dict[str, Any]:
    registry = load_benchmark_registry()
    benchmarks = list(registry.get("benchmarks", []))
    if benchmark_id:
        benchmarks = [benchmark_definition(benchmark_id)]

    return {
        "version": registry.get("version"),
        "description": registry.get("description"),
        "benchmark_count": len(benchmarks),
        "benchmarks": [
            {
                "id": benchmark.get("id"),
                "title": benchmark.get("title"),
                "benchmark_type": benchmark.get("benchmark_type"),
                "target_workflow_ids": list(benchmark.get("target_workflow_ids", [])),
                "task_count": len(benchmark.get("tasks", [])),
                "key_metrics": list(benchmark.get("key_metrics", [])),
                "official_sources": list(benchmark.get("official_sources", [])),
            }
            for benchmark in benchmarks
        ],
    }


def benchmark_tasks_for_workflow(workflow_id: str | None) -> list[dict[str, Any]]:
    if not workflow_id:
        return []
    tasks: list[dict[str, Any]] = []
    for task in benchmark_task_records():
        benchmark = benchmark_definition(str(task.get("benchmark_id")))
        if str(workflow_id) in {str(item) for item in benchmark.get("target_workflow_ids", [])}:
            tasks.append(task)
    return tasks


def _coverage(required_items: list[str], actual_items: list[str]) -> dict[str, Any]:
    required = [str(item) for item in required_items]
    actual_set = {str(item) for item in actual_items}
    present = [item for item in required if item in actual_set]
    missing = [item for item in required if item not in actual_set]
    return {
        "required": required,
        "present": present,
        "missing": missing,
        "complete": not missing,
    }


def _normalize_tokens(value: str) -> set[str]:
    text = str(value).strip().lower()
    replacements = {
        "bqsr": "recalibration",
        "bigwig": "bigwig",
        "g.vcf": "gvcf",
        "g-vcf": "gvcf",
        "vcf.gz": "vcf",
        "bams": "bam",
    }
    for before, after in replacements.items():
        text = text.replace(before, after)
    tokens = re.findall(r"[a-z0-9]+", text)
    return {token for token in tokens if token not in {"and", "or", "the", "a", "an", "with", "for", "final"}}


def _semantic_coverage(required_items: list[str], actual_items: list[str]) -> dict[str, Any]:
    required = [str(item) for item in required_items]
    actual = [str(item) for item in actual_items]
    present: list[str] = []
    missing: list[str] = []

    actual_token_sets = [(_normalize_tokens(item), item) for item in actual]
    for item in required:
        required_tokens = _normalize_tokens(item)
        matched = False
        for actual_tokens, _actual_item in actual_token_sets:
            if required_tokens and required_tokens.issubset(actual_tokens):
                matched = True
                break
        if matched:
            present.append(item)
        else:
            missing.append(item)

    return {
        "required": required,
        "present": present,
        "missing": missing,
        "complete": not missing,
    }


def _plan_confirmation_stage_ids(plan: dict[str, Any]) -> list[str]:
    return [
        str(stage.get("stage_id"))
        for stage in plan.get("stages", [])
        if isinstance(stage, dict) and stage.get("requires_user_confirmation", False)
    ]


def evaluate_plan_contract_against_benchmark(
    plan: dict[str, Any],
    analysis_flow: dict[str, Any] | None,
    task_payload: dict[str, Any],
) -> dict[str, Any]:
    required_outputs = list(task_payload.get("required_expected_outputs", []))
    required_confirmation_stage_ids = list(task_payload.get("required_confirmation_stage_ids", []))
    required_delivery_bundle_items = list(task_payload.get("required_delivery_bundle_items", []))
    accepted_strategy_profiles = list(task_payload.get("accepted_strategy_profiles", []))

    outputs_coverage = _coverage(required_outputs, list(plan.get("expected_outputs", [])))
    confirmation_coverage = _coverage(required_confirmation_stage_ids, _plan_confirmation_stage_ids(plan))
    delivery_coverage = _coverage(
        required_delivery_bundle_items,
        list((analysis_flow or {}).get("delivery_bundle", [])),
    )

    expected_workflow_id = task_payload.get("expected_workflow_id")
    recommended_workflow_id = plan.get("source_workflow_id")
    workflow_match = recommended_workflow_id == expected_workflow_id
    selected_strategy_profile = plan.get("selected_strategy_profile")
    strategy_match = True
    if accepted_strategy_profiles:
        strategy_match = selected_strategy_profile in accepted_strategy_profiles

    if workflow_match and outputs_coverage["complete"] and confirmation_coverage["complete"] and delivery_coverage["complete"] and strategy_match:
        verdict = "pass"
    elif workflow_match:
        verdict = "partial"
    else:
        verdict = "fail"

    return {
        "benchmark_id": task_payload.get("benchmark_id"),
        "task_id": task_payload.get("task_id"),
        "title": task_payload.get("title"),
        "verdict": verdict,
        "recommended_workflow_id": recommended_workflow_id,
        "expected_workflow_id": expected_workflow_id,
        "workflow_match": workflow_match,
        "selected_strategy_profile": selected_strategy_profile,
        "accepted_strategy_profiles": accepted_strategy_profiles,
        "strategy_match": strategy_match,
        "outputs_coverage": outputs_coverage,
        "confirmation_coverage": confirmation_coverage,
        "delivery_coverage": delivery_coverage,
        "analysis_flow": analysis_flow,
        "unevaluated_requirements": copy.deepcopy(task_payload.get("benchmark_requirements", {})),
    }


def _environment_snapshot(session_dir: Path | None = None) -> dict[str, Any]:
    bridge_snapshot = _execution_bridge_tool_snapshot(session_dir)
    return {
        "generated_at": _now_iso(),
        "python_executable": sys.executable,
        "python_version": sys.version,
        "platform": platform.platform(),
        "cwd": str(ROOT),
        "path": os.environ.get("PATH", ""),
        "stage_bridges": bridge_snapshot["stage_bridges"],
        "tool_resolution": bridge_snapshot["tool_resolution"],
    }


def _session_repro_scorecard(session_dir: Path) -> dict[str, Any] | None:
    scorecard_path = session_dir / "repro" / "scorecard.json"
    if not scorecard_path.exists() or not scorecard_path.is_file():
        return None
    try:
        return _load_json(scorecard_path)
    except Exception:
        return None


def session_skill_crystallization_candidate(session_dir: Path) -> dict[str, Any]:
    session_dir = _ensure_session_directory(session_dir, must_exist=True)
    bundle = _sync_session_bundle(session_dir, _load_session_bundle(session_dir))
    session = dict(bundle.get("session", {}))
    approved_plan = dict(bundle.get("approved_plan", {}))
    execution_draft = dict(bundle.get("execution_draft", {}))
    benchmark_matches = list(bundle_benchmark_matches(bundle, approved_plan.get("source_workflow_id")))
    repro_scorecard = _session_repro_scorecard(session_dir)

    workflow_id = str(approved_plan.get("source_workflow_id") or "")
    strategy_profile = str(approved_plan.get("selected_strategy_profile") or approved_plan.get("strategy_type") or "")
    policy = next((item for item in load_skill_crystallization_registry().get("policies", []) if str(item.get("workflow_id")) == workflow_id), None)

    reasons: list[str] = []
    if not policy:
        reasons.append("workflow is not registered as a crystallizable flow")
    else:
        allowed_profiles = [str(item) for item in policy.get("allowed_strategy_profiles", [])]
        if allowed_profiles and strategy_profile not in allowed_profiles:
            reasons.append("strategy profile is not allowed for skill crystallization")
        if policy.get("require_completed_run", False) and str(session.get("run_status") or "") != "completed":
            reasons.append("session run is not completed")
        allowed_verdicts = [str(item) for item in policy.get("allowed_run_verdicts", [])]
        if allowed_verdicts and str(session.get("run_verdict") or "") not in allowed_verdicts:
            reasons.append("run verdict does not meet crystallization policy")
        if policy.get("require_no_unresolved_skills", False) and list(execution_draft.get("unresolved_skill_ids", [])):
            reasons.append("execution draft still contains unresolved skills")
        if policy.get("require_no_unavailable_runtime_tools", False) and list(execution_draft.get("unavailable_runtime_skill_ids", [])):
            reasons.append("execution draft still depends on unavailable runtime tools")
        if policy.get("require_no_unmapped_execution_bridges", False) and list(execution_draft.get("unmapped_stage_ids", [])):
            reasons.append("some stages do not yet have formal execution bridge contracts")
        if policy.get("require_passing_benchmark", False) and not any(item.get("verdict") == "pass" for item in benchmark_matches):
            reasons.append("no passing benchmark match is attached to this completed flow")
        if policy.get("require_repro_scorecard", False) and not repro_scorecard:
            reasons.append("no reproducibility scorecard is attached to this completed flow")
        if policy.get("require_comparator_backed_score", False):
            if not repro_scorecard or not repro_scorecard.get("scientific_score_ready", False):
                reasons.append("no comparator-backed scientific score is attached to this completed flow")

    return {
        "eligible": not reasons,
        "workflow_id": workflow_id or None,
        "selected_strategy_profile": strategy_profile or None,
        "policy": policy,
        "reasons": reasons,
        "benchmark_matches": benchmark_matches,
        "repro_scorecard": repro_scorecard,
        "environment": _environment_snapshot(session_dir),
    }


def _execution_bridge_tool_snapshot(session_dir: Path | None) -> dict[str, Any]:
    if session_dir is None:
        return {"stage_bridges": [], "tool_resolution": {}}

    try:
        bundle = _load_session_bundle(_ensure_session_directory(session_dir, must_exist=True))
    except FileNotFoundError:
        return {"stage_bridges": [], "tool_resolution": {}}

    execution_draft = dict(bundle.get("execution_draft", {}))
    stage_bridges: list[dict[str, Any]] = []
    required_tools: set[str] = set()
    for stage in execution_draft.get("stages", []):
        if not isinstance(stage, dict):
            continue
        bridge = dict(stage.get("execution_bridge", {}))
        if not bridge:
            continue
        tools = [str(item) for item in bridge.get("required_tools", [])]
        required_tools.update(tools)
        stage_bridges.append(
            {
                "stage_id": str(stage.get("stage_id")),
                "bridge_id": bridge.get("bridge_id"),
                "bridge_type": bridge.get("bridge_type"),
                "execution_mode": bridge.get("execution_mode"),
                "required_tools": tools,
                "contract_defined": bool(bridge.get("contract_defined", False)),
                "ready_on_this_machine": bool(bridge.get("ready_on_this_machine", False)),
            }
        )

    return {
        "stage_bridges": stage_bridges,
        "tool_resolution": {tool: shutil.which(tool) for tool in sorted(required_tools)},
    }


def export_benchmark_repro_bundle(
    result_payload: dict[str, Any],
    output_dir: Path,
    *,
    invoked_command: str | None = None,
) -> dict[str, Any]:
    output_dir = output_dir.expanduser().resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    evidence = dict(result_payload.get("evidence", {}))
    session_dir_raw = evidence.get("session_dir")
    session_dir = Path(session_dir_raw).resolve() if session_dir_raw else None
    bridge_snapshot = _execution_bridge_tool_snapshot(session_dir)

    commands_path = output_dir / 'commands.sh'
    environment_path = output_dir / 'environment.json'
    artifacts_path = output_dir / 'artifacts.json'
    scorecard_path = output_dir / 'scorecard.json'

    command_lines = [
        '#!/usr/bin/env bash',
        'set -euo pipefail',
        '',
        f'# benchmark_id: {result_payload.get("benchmark_id")}',
        f'# task_id: {result_payload.get("task_id")}',
        f'# verdict: {result_payload.get("verdict")}',
    ]
    if invoked_command:
        command_lines.extend(['', '# benchmark-run invocation', invoked_command])
    if bridge_snapshot['stage_bridges']:
        command_lines.append('')
        command_lines.append('# stage bridge summary')
        for stage in bridge_snapshot['stage_bridges']:
            command_lines.append(
                '# stage {stage_id} bridge={bridge_id} mode={execution_mode} tools={tools}'.format(
                    stage_id=stage.get('stage_id'),
                    bridge_id=stage.get('bridge_id'),
                    execution_mode=stage.get('execution_mode'),
                    tools=','.join(stage.get('required_tools', [])) or '-',
                )
            )
    commands_path.write_text("\n".join(command_lines) + "\n", encoding="utf-8")
    try:
        os.chmod(commands_path, 0o755)
    except OSError:
        pass

    environment_payload = {
        'generated_at': _now_iso(),
        'python_executable': sys.executable,
        'python_version': sys.version,
        'platform': platform.platform(),
        'cwd': str(ROOT),
        'path': os.environ.get('PATH', ''),
        'stage_bridges': bridge_snapshot['stage_bridges'],
        'tool_resolution': bridge_snapshot['tool_resolution'],
    }
    save_json(environment_payload, environment_path)

    artifact_payload = {
        'benchmark_id': result_payload.get('benchmark_id'),
        'task_id': result_payload.get('task_id'),
        'evidence': evidence,
        'artifact_evaluation': dict(result_payload.get('artifact_evaluation', {})),
    }
    save_json(artifact_payload, artifacts_path)

    artifact_evaluation = dict(result_payload.get('artifact_evaluation', {}))
    scorecard_payload = {
        'benchmark_id': result_payload.get('benchmark_id'),
        'task_id': result_payload.get('task_id'),
        'title': result_payload.get('title'),
        'verdict': result_payload.get('verdict'),
        'scorecard': dict(result_payload.get('scorecard', {})),
        'control_evaluation': dict(result_payload.get('control_evaluation', {})),
        'artifact_evaluation': artifact_evaluation,
        'scientific_score_ready': bool(artifact_evaluation.get('truth_artifact_coverage', {}).get('complete')) and bool(artifact_evaluation.get('metric_value_evaluation', {}).get('complete')),
    }
    save_json(scorecard_payload, scorecard_path)

    return {
        'path': str(output_dir),
        'files': {
            'commands': str(commands_path),
            'environment': str(environment_path),
            'artifacts': str(artifacts_path),
            'scorecard': str(scorecard_path),
        },
    }


def benchmark_evidence_from_session(session_dir: Path) -> dict[str, Any]:
    bundle = _load_session_bundle(_ensure_session_directory(session_dir, must_exist=True))
    run_state = dict(bundle.get("run", {}))
    run_status = dict(bundle.get("run_status", {}))
    run_review = dict(bundle.get("run_review", {}))
    artifacts = [
        dict(item)
        for item in run_state.get("artifacts", [])
        if isinstance(item, dict)
    ]
    delivery_items = [
        str(item.get("description") or item.get("path") or "").strip()
        for item in artifacts
        if str(item.get("description") or item.get("path") or "").strip()
    ]
    return {
        "session_dir": str(session_dir.resolve()),
        "run_status": run_status.get("status"),
        "run_verdict": run_review.get("verdict"),
        "artifact_paths": [str(item.get("path")) for item in artifacts if item.get("path")],
        "delivery_items": delivery_items,
        "truth_artifacts": [],
        "metrics": {},
    }


def merge_benchmark_evidence(
    *,
    session_dir: Path | None = None,
    evidence_payload: dict[str, Any] | None = None,
    delivery_items: list[str] | None = None,
    truth_artifacts: list[str] | None = None,
    metrics: dict[str, str] | None = None,
) -> dict[str, Any]:
    merged = {
        "session_dir": None,
        "run_status": None,
        "run_verdict": None,
        "artifact_paths": [],
        "delivery_items": [],
        "truth_artifacts": [],
        "metrics": {},
        "extracted_metrics": {},
    }

    if session_dir is not None:
        merged.update(benchmark_evidence_from_session(session_dir))

    if isinstance(evidence_payload, dict):
        if evidence_payload.get("session_dir"):
            merged["session_dir"] = str(evidence_payload.get("session_dir"))
        if evidence_payload.get("run_status"):
            merged["run_status"] = str(evidence_payload.get("run_status"))
        if evidence_payload.get("run_verdict"):
            merged["run_verdict"] = str(evidence_payload.get("run_verdict"))
        merged["artifact_paths"] = [
            *merged["artifact_paths"],
            *[str(item) for item in evidence_payload.get("artifact_paths", []) if str(item).strip()],
        ]
        merged["delivery_items"] = [
            *merged["delivery_items"],
            *[str(item) for item in evidence_payload.get("delivery_items", []) if str(item).strip()],
        ]
        merged["truth_artifacts"] = [
            *merged["truth_artifacts"],
            *[str(item) for item in evidence_payload.get("truth_artifacts", []) if str(item).strip()],
        ]
        if isinstance(evidence_payload.get("metrics"), dict):
            merged["metrics"] = {
                **merged["metrics"],
                **{str(key): str(value) for key, value in evidence_payload["metrics"].items()},
            }

    if delivery_items:
        merged["delivery_items"].extend(str(item) for item in delivery_items if str(item).strip())
    if truth_artifacts:
        merged["truth_artifacts"].extend(str(item) for item in truth_artifacts if str(item).strip())
    if metrics:
        merged["metrics"] = {
            **merged["metrics"],
            **{str(key): str(value) for key, value in metrics.items()},
        }

    for field in ("artifact_paths", "delivery_items", "truth_artifacts"):
        seen: set[str] = set()
        ordered: list[str] = []
        for item in merged[field]:
            value = str(item).strip()
            if not value or value in seen:
                continue
            seen.add(value)
            ordered.append(value)
        merged[field] = ordered

    extracted_metrics = extract_metrics_from_artifacts(merged["artifact_paths"])
    merged["extracted_metrics"] = extracted_metrics
    for key, value in extracted_metrics.items():
        merged["metrics"].setdefault(str(key), str(value))

    return merged


def _read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        return [
            {str(key): str(value) for key, value in row.items() if key is not None}
            for row in reader
            if isinstance(row, dict)
        ]


def _extract_happy_summary_metrics(path: Path) -> dict[str, str]:
    rows = _read_csv_rows(path)
    if not rows:
        return {}

    def score(row: dict[str, str]) -> tuple[int, int]:
        row_type = str(row.get("Type", "")).strip().upper()
        row_filter = str(row.get("Filter", "")).strip().upper()
        return (
            1 if row_type == "ALL" else 0,
            1 if row_filter == "ALL" else 0,
        )

    ranked_rows = sorted(rows, key=score, reverse=True)
    row = ranked_rows[0]
    precision = row.get("METRIC.Precision") or row.get("Precision") or ""
    recall = row.get("METRIC.Recall") or row.get("Recall") or ""
    metrics: dict[str, str] = {}
    if precision:
        metrics["precision"] = str(precision)
    if recall:
        metrics["recall"] = str(recall)

    precision_value = _parse_float_metric(precision)
    recall_value = _parse_float_metric(recall)
    if precision_value is not None and recall_value is not None and precision_value + recall_value > 0:
        metrics["F1"] = str((2 * precision_value * recall_value) / (precision_value + recall_value))
    return metrics


def extract_metrics_from_artifacts(artifact_paths: list[str]) -> dict[str, str]:
    metrics: dict[str, str] = {}
    for raw_path in artifact_paths:
        path = Path(str(raw_path)).expanduser()
        if not path.exists() or not path.is_file():
            continue
        if path.name.endswith(".summary.csv"):
            metrics.update(_extract_happy_summary_metrics(path))
    return metrics


def _metric_key_coverage(required_metrics: list[str], actual_metrics: dict[str, str]) -> dict[str, Any]:
    required = [str(item) for item in required_metrics]
    actual_keys = {str(key) for key in actual_metrics}
    present = [item for item in required if item in actual_keys]
    missing = [item for item in required if item not in actual_keys]
    return {
        "required": required,
        "present": present,
        "missing": missing,
        "complete": not missing,
    }


def _parse_float_metric(raw_value: str) -> float | None:
    text = str(raw_value).strip()
    if not text:
        return None
    try:
        return float(text)
    except ValueError:
        return None


def _evaluate_metric_values(required_metrics: list[str], actual_metrics: dict[str, str]) -> dict[str, Any]:
    required = [str(item) for item in required_metrics]
    parsed: dict[str, float] = {}
    invalid: list[str] = []
    out_of_range: list[str] = []

    for key, raw_value in actual_metrics.items():
        parsed_value = _parse_float_metric(raw_value)
        if parsed_value is None:
            invalid.append(str(key))
            continue
        parsed[str(key)] = parsed_value
        if str(key) in {"precision", "recall", "F1"} and not (0.0 <= parsed_value <= 1.0):
            out_of_range.append(str(key))

    missing = [item for item in required if item not in parsed]
    inferred: dict[str, float] = {}
    consistency_checks: list[dict[str, Any]] = []

    if "precision" in parsed and "recall" in parsed:
        precision = parsed["precision"]
        recall = parsed["recall"]
        if precision + recall > 0:
            inferred_f1 = (2 * precision * recall) / (precision + recall)
            inferred["F1"] = inferred_f1
            if "F1" in parsed:
                delta = abs(parsed["F1"] - inferred_f1)
                consistency_checks.append(
                    {
                        "metric": "F1",
                        "reported": parsed["F1"],
                        "expected_from_precision_recall": inferred_f1,
                        "delta": delta,
                        "consistent": delta <= 0.01,
                    }
                )
            elif "F1" in missing:
                missing = [item for item in missing if item != "F1"]
                parsed["F1"] = inferred_f1

    complete = not missing and not invalid and not out_of_range and all(
        item.get("consistent", True) for item in consistency_checks
    )

    return {
        "required": required,
        "parsed_metrics": parsed,
        "invalid_metrics": sorted(invalid),
        "out_of_range_metrics": sorted(out_of_range),
        "missing_metrics": sorted(missing),
        "inferred_metrics": inferred,
        "consistency_checks": consistency_checks,
        "complete": complete,
    }


def evaluate_benchmark_run(
    task_payload: dict[str, Any],
    *,
    session_dir: Path | None = None,
    evidence_payload: dict[str, Any] | None = None,
    delivery_items: list[str] | None = None,
    truth_artifacts: list[str] | None = None,
    metrics: dict[str, str] | None = None,
) -> dict[str, Any]:
    control = evaluate_benchmark_task(task_payload)
    evidence = merge_benchmark_evidence(
        session_dir=session_dir,
        evidence_payload=evidence_payload,
        delivery_items=delivery_items,
        truth_artifacts=truth_artifacts,
        metrics=metrics,
    )
    benchmark_requirements = dict(task_payload.get("benchmark_requirements", {}))
    delivery_artifact_coverage = _semantic_coverage(
        list(task_payload.get("required_delivery_bundle_items", [])),
        list(evidence.get("delivery_items", [])),
    )
    truth_artifact_coverage = _semantic_coverage(
        list(benchmark_requirements.get("truth_artifacts", [])),
        list(evidence.get("truth_artifacts", [])),
    )
    metric_key_coverage = _metric_key_coverage(
        list(benchmark_requirements.get("metrics", [])),
        dict(evidence.get("metrics", {})),
    )
    metric_value_evaluation = _evaluate_metric_values(
        list(benchmark_requirements.get("metrics", [])),
        dict(evidence.get("metrics", {})),
    )
    metric_key_coverage["complete"] = metric_key_coverage["complete"] or not metric_value_evaluation["missing_metrics"]
    metric_key_coverage["missing"] = [
        item for item in metric_key_coverage["missing"] if item in metric_value_evaluation["missing_metrics"]
    ]

    checks = [
        ("workflow_match", bool(control.get("workflow_match"))),
        ("strategy_match", bool(control.get("strategy_match"))),
        ("outputs_complete", bool(control["outputs_coverage"]["complete"])),
        ("confirmation_complete", bool(control["confirmation_coverage"]["complete"])),
        ("delivery_contract_complete", bool(control["delivery_coverage"]["complete"])),
        ("delivery_artifacts_complete", bool(delivery_artifact_coverage["complete"])),
        ("truth_artifacts_complete", bool(truth_artifact_coverage["complete"])),
        ("metric_keys_complete", bool(metric_key_coverage["complete"])),
        ("metric_values_complete", bool(metric_value_evaluation["complete"])),
    ]
    passed = [name for name, ok in checks if ok]
    failed = [name for name, ok in checks if not ok]

    if control["verdict"] == "fail":
        verdict = "fail"
    elif not metric_value_evaluation["complete"]:
        verdict = "partial"
    elif not delivery_artifact_coverage["complete"] and not truth_artifact_coverage["complete"]:
        verdict = "partial"
    elif metric_key_coverage["complete"] and truth_artifact_coverage["complete"] and delivery_artifact_coverage["complete"] and control["verdict"] == "pass":
        verdict = "pass"
    else:
        verdict = "partial"

    return {
        "benchmark_id": task_payload.get("benchmark_id"),
        "task_id": task_payload.get("task_id"),
        "title": task_payload.get("title"),
        "verdict": verdict,
        "control_evaluation": control,
        "evidence": evidence,
        "artifact_evaluation": {
            "delivery_artifact_coverage": delivery_artifact_coverage,
            "truth_artifact_coverage": truth_artifact_coverage,
            "metric_key_coverage": metric_key_coverage,
            "metric_value_evaluation": metric_value_evaluation,
        },
        "scorecard": {
            "passed_checks": passed,
            "failed_checks": failed,
            "passed_count": len(passed),
            "total_checks": len(checks),
        },
    }


def benchmark_suite(
    benchmark_id: str | None = None,
    *,
    mode: str = "contract",
    evidence_root: Path | None = None,
) -> dict[str, Any]:
    suite_mode = str(mode).strip().lower()
    if suite_mode not in {"contract", "evidence"}:
        raise ValueError(f"Unsupported benchmark suite mode: {mode}")

    tasks = benchmark_task_records(benchmark_id)
    results: list[dict[str, Any]] = []
    verdict_counts = {"pass": 0, "partial": 0, "fail": 0}
    workflow_match_passes = 0
    outputs_complete_passes = 0
    confirmation_complete_passes = 0
    delivery_contract_complete_passes = 0
    evidence_delivery_complete_passes = 0
    truth_artifact_complete_passes = 0
    metric_key_complete_passes = 0
    metric_value_complete_passes = 0

    for task in tasks:
        if suite_mode == "contract":
            result = evaluate_benchmark_task(task)
            summary_row = {
                "benchmark_id": result["benchmark_id"],
                "task_id": result["task_id"],
                "title": result["title"],
                "verdict": result["verdict"],
                "mode": suite_mode,
                "workflow_match": result["workflow_match"],
                "strategy_match": result["strategy_match"],
                "outputs_complete": result["outputs_coverage"]["complete"],
                "confirmation_complete": result["confirmation_coverage"]["complete"],
                "delivery_contract_complete": result["delivery_coverage"]["complete"],
            }
            workflow_match_passes += int(result["workflow_match"])
            outputs_complete_passes += int(result["outputs_coverage"]["complete"])
            confirmation_complete_passes += int(result["confirmation_coverage"]["complete"])
            delivery_contract_complete_passes += int(result["delivery_coverage"]["complete"])
        else:
            evidence_payload = None
            evidence_path = None
            if evidence_root is not None:
                candidate = evidence_root / f"{task['task_id']}.evidence.json"
                if candidate.exists():
                    evidence_path = candidate
                    evidence_payload = load_structured_file(candidate)
            result = evaluate_benchmark_run(
                task,
                evidence_payload=evidence_payload,
            )
            summary_row = {
                "benchmark_id": result["benchmark_id"],
                "task_id": result["task_id"],
                "title": result["title"],
                "verdict": result["verdict"],
                "mode": suite_mode,
                "workflow_match": result["control_evaluation"]["workflow_match"],
                "strategy_match": result["control_evaluation"]["strategy_match"],
                "outputs_complete": result["control_evaluation"]["outputs_coverage"]["complete"],
                "confirmation_complete": result["control_evaluation"]["confirmation_coverage"]["complete"],
                "delivery_contract_complete": result["control_evaluation"]["delivery_coverage"]["complete"],
                "delivery_artifacts_complete": result["artifact_evaluation"]["delivery_artifact_coverage"]["complete"],
                "truth_artifacts_complete": result["artifact_evaluation"]["truth_artifact_coverage"]["complete"],
                "metric_keys_complete": result["artifact_evaluation"]["metric_key_coverage"]["complete"],
                "metric_values_complete": result["artifact_evaluation"]["metric_value_evaluation"]["complete"],
                "evidence_file": str(evidence_path) if evidence_path else None,
            }
            workflow_match_passes += int(result["control_evaluation"]["workflow_match"])
            outputs_complete_passes += int(result["control_evaluation"]["outputs_coverage"]["complete"])
            confirmation_complete_passes += int(result["control_evaluation"]["confirmation_coverage"]["complete"])
            delivery_contract_complete_passes += int(result["control_evaluation"]["delivery_coverage"]["complete"])
            evidence_delivery_complete_passes += int(result["artifact_evaluation"]["delivery_artifact_coverage"]["complete"])
            truth_artifact_complete_passes += int(result["artifact_evaluation"]["truth_artifact_coverage"]["complete"])
            metric_key_complete_passes += int(result["artifact_evaluation"]["metric_key_coverage"]["complete"])
            metric_value_complete_passes += int(result["artifact_evaluation"]["metric_value_evaluation"]["complete"])

        verdict_counts[result["verdict"]] = verdict_counts.get(result["verdict"], 0) + 1
        results.append(summary_row)

    total_tasks = len(results)
    benchmark_ids = sorted({str(item["benchmark_id"]) for item in results})

    summary = {
        "mode": suite_mode,
        "benchmark_count": len(benchmark_ids),
        "task_count": total_tasks,
        "verdict_counts": verdict_counts,
        "workflow_match_rate": workflow_match_passes / total_tasks if total_tasks else 0.0,
        "outputs_complete_rate": outputs_complete_passes / total_tasks if total_tasks else 0.0,
        "confirmation_complete_rate": confirmation_complete_passes / total_tasks if total_tasks else 0.0,
        "delivery_contract_complete_rate": delivery_contract_complete_passes / total_tasks if total_tasks else 0.0,
    }
    if suite_mode == "evidence":
        summary.update(
            {
                "delivery_artifacts_complete_rate": evidence_delivery_complete_passes / total_tasks if total_tasks else 0.0,
                "truth_artifacts_complete_rate": truth_artifact_complete_passes / total_tasks if total_tasks else 0.0,
                "metric_keys_complete_rate": metric_key_complete_passes / total_tasks if total_tasks else 0.0,
                "metric_values_complete_rate": metric_value_complete_passes / total_tasks if total_tasks else 0.0,
            }
        )

    return {
        "generated_at": _now_iso(),
        "mode": suite_mode,
        "benchmark_ids": benchmark_ids,
        "summary": summary,
        "results": results,
    }


def evaluate_benchmark_task(task_payload: dict[str, Any]) -> dict[str, Any]:
    request_text = str(task_payload.get("request_text") or "").strip()
    goal = str(task_payload.get("goal") or "").strip() or None
    extra_tags = [str(item).strip() for item in task_payload.get("extra_tags", []) if str(item).strip()]

    request = build_request(
        request_text=request_text,
        goal=goal,
        extra_tags=extra_tags,
    )
    plans = generate_candidate_plans(request)
    proposals = {
        "request": request,
        "plans": plans,
    }
    review = review_plans(proposals)
    recommended_plan = next(
        (copy.deepcopy(plan) for plan in plans if plan.get("plan_id") == review.get("recommended_plan_id")),
        copy.deepcopy(plans[0]) if plans else {},
    )
    recommended_workflow_id = recommended_plan.get("source_workflow_id")
    analysis_flow = analysis_flow_for_workflow(recommended_workflow_id)
    contract_evaluation = evaluate_plan_contract_against_benchmark(
        recommended_plan,
        analysis_flow,
        task_payload,
    )

    return {
        "benchmark_id": task_payload.get("benchmark_id"),
        "task_id": task_payload.get("task_id"),
        "title": task_payload.get("title"),
        "verdict": contract_evaluation["verdict"],
        "request": request,
        "review": review,
        "recommended_plan_id": recommended_plan.get("plan_id"),
        **contract_evaluation,
    }


def bundle_benchmark_matches(bundle: dict[str, Any], workflow_id: str | None) -> list[dict[str, Any]]:
    if not workflow_id:
        return []
    approved_plan = bundle.get("approved_plan")
    plan: dict[str, Any] | None = None
    if isinstance(approved_plan, dict) and approved_plan.get("source_workflow_id") == workflow_id:
        plan = copy.deepcopy(approved_plan)
    else:
        for candidate in dict(bundle.get("plans", {})).get("plans", []):
            if isinstance(candidate, dict) and candidate.get("source_workflow_id") == workflow_id:
                plan = copy.deepcopy(candidate)
                break
    if not isinstance(plan, dict):
        return []

    analysis_flow = analysis_flow_for_workflow(workflow_id)
    matches: list[dict[str, Any]] = []
    for task in benchmark_tasks_for_workflow(workflow_id):
        evaluation = evaluate_plan_contract_against_benchmark(plan, analysis_flow, task)
        matches.append(
            {
                "benchmark_id": task.get("benchmark_id"),
                "benchmark_title": task.get("benchmark_title"),
                "benchmark_type": task.get("benchmark_type"),
                "benchmark_metrics": list(task.get("benchmark_metrics", [])),
                "task_id": task.get("task_id"),
                "title": task.get("title"),
                "verdict": evaluation["verdict"],
                "workflow_match": evaluation["workflow_match"],
                "strategy_match": evaluation["strategy_match"],
                "outputs_complete": evaluation["outputs_coverage"]["complete"],
                "confirmation_complete": evaluation["confirmation_coverage"]["complete"],
                "delivery_complete": evaluation["delivery_coverage"]["complete"],
                "missing_outputs": list(evaluation["outputs_coverage"]["missing"]),
                "missing_confirmation_stage_ids": list(evaluation["confirmation_coverage"]["missing"]),
                "missing_delivery_items": list(evaluation["delivery_coverage"]["missing"]),
            }
        )
    return matches


def infer_request_tags(request_text: str, goal: str | None, extra_tags: list[str], workflows: list[dict[str, Any]]) -> list[str]:
    normalized = f"{request_text} {goal or ''}".lower()
    tags: set[str] = {tag.strip().lower() for tag in extra_tags if tag.strip()}

    heuristic_tags = {
        "rnaseq": ["rna-seq", "rna seq", "rnaseq"],
        "scrnaseq": ["scrna", "scrnaseq", "single-cell rna", "single cell rna"],
        "single-cell": ["single-cell", "single cell", "10x"],
        "differential-expression": ["differential expression", "de analysis", "de results"],
        "fastq": ["fastq", "fastqs"],
        "bulk-transcriptomics": ["bulk rna", "bulk transcriptomics", "bulk rna-seq"],
        "atacseq": ["atac-seq", "atac seq", "atacseq"],
        "chromatin-accessibility": ["chromatin accessibility", "open chromatin", "accessibility peaks"],
        "germline-variant": ["germline variant", "germline snp", "germline indel"],
        "variant-calling": ["variant calling", "variant discovery", "joint genotyping"],
        "wes": ["wes", "whole exome"],
        "wgs": ["wgs", "whole genome"],
        "snp-indel": ["snp/indel", "snp indel", "snv indel"],
        "sequence": ["sequence", "sequences"],
        "annotation": ["annotation", "annotate"],
        "protein": ["protein", "proteins"],
        "structure": ["structure", "folding"],
    }
    for tag, cues in heuristic_tags.items():
        if any(cue in normalized for cue in cues):
            tags.add(tag)

    for workflow in workflows:
        for tag in workflow.get("request_tags", []):
            tag_text = str(tag).lower()
            variants = {
                tag_text,
                tag_text.replace("-", " "),
                tag_text.replace("-", ""),
            }
            if any(variant and variant in normalized for variant in variants):
                tags.add(tag_text)

    if not tags:
        tags.add("bioinformatics")

    return sorted(tags)


def build_request(request_text: str, goal: str | None = None, extra_tags: list[str] | None = None) -> dict[str, Any]:
    workflow_registry = load_workflow_registry()
    workflows = workflow_registry.get("workflows", [])
    goal_text = goal.strip() if goal else request_text.strip()
    request_tags = infer_request_tags(request_text, goal_text, extra_tags or [], workflows)

    request_slug = _slugify(goal_text)[:40]
    return {
        "request_id": f"req_{request_slug}",
        "user_goal": goal_text,
        "request_text": request_text.strip(),
        "request_tags": request_tags,
        "inputs": [],
        "constraints": [],
        "preferred_outputs": [],
        "context_notes": [],
    }


def _dedupe_text_items(items: list[str]) -> list[str]:
    seen: set[str] = set()
    ordered: list[str] = []
    for item in items:
        value = str(item).strip().lower()
        if not value or value in seen:
            continue
        seen.add(value)
        ordered.append(value)
    return ordered


def _resolve_workflow_family_template(workflow_family: str) -> tuple[dict[str, Any], dict[str, Any]]:
    requested = str(workflow_family).strip().lower()
    knowledge = load_workflow_knowledge()
    workflow_registry = load_workflow_registry()

    family_template = next(
        (
            dict(item)
            for item in knowledge.get("family_templates", [])
            if requested in {
                str(item.get("family_id", "")).lower(),
                str(item.get("registry_workflow_id", "")).lower(),
            }
        ),
        None,
    )
    if family_template is None:
        raise KeyError(f"Unknown workflow family: {workflow_family}")

    workflow_id = str(family_template.get("registry_workflow_id", "")).strip()
    workflow = next(
        (dict(item) for item in workflow_registry.get("workflows", []) if str(item.get("id")) == workflow_id),
        None,
    )
    if workflow is None:
        raise KeyError(f"Workflow family `{workflow_family}` points to an unknown workflow id: {workflow_id}")
    return family_template, workflow


def _resolve_strategy_profile(family_template: dict[str, Any], strategy_profile: str | None) -> dict[str, Any] | None:
    if not strategy_profile:
        return None
    requested = str(strategy_profile).strip().lower()
    profile = next(
        (
            dict(item)
            for item in family_template.get("strategy_profiles", [])
            if str(item.get("id", "")).lower() == requested
        ),
        None,
    )
    if profile is None:
        raise KeyError(f"Unknown strategy profile `{strategy_profile}` for family `{family_template.get('family_id')}`")
    return profile


def prepare_session_start_inputs(
    *,
    request_text: str | None,
    goal: str | None,
    extra_tags: list[str] | None,
    workflow_family: str | None = None,
    strategy_profile: str | None = None,
    session_name: str | None = None,
) -> dict[str, Any]:
    effective_request_text = str(request_text or "").strip()
    effective_goal = str(goal or "").strip() or None
    effective_session_name = str(session_name or "").strip() or None
    effective_tags = _dedupe_text_items(list(extra_tags or []))

    family_template = None
    workflow = None
    profile = None

    if workflow_family:
        family_template, workflow = _resolve_workflow_family_template(workflow_family)
        effective_tags = _dedupe_text_items(effective_tags + list(workflow.get("request_tags", [])))
        if effective_session_name is None:
            effective_session_name = str(family_template.get("family_id") or workflow.get("id") or "bio-session")
        if not effective_request_text:
            effective_request_text = f"Plan a {str(workflow.get('summary', workflow.get('id', 'bioinformatics workflow'))).lower()} workflow with stage-by-stage review and a final evidence bundle."
        if effective_goal is None:
            effective_goal = f"Generate a staged {str(workflow.get('summary', workflow.get('id', 'bioinformatics workflow'))).lower()} plan."

    if family_template is not None:
        profile = _resolve_strategy_profile(family_template, strategy_profile)
        if profile is not None:
            request_tag = str(profile.get("request_tag") or "").strip().lower()
            if request_tag:
                effective_tags = _dedupe_text_items(effective_tags + [request_tag])
            if session_name is None:
                suffix = str(profile.get("id") or "").strip().lower()
                if suffix:
                    effective_session_name = f"{effective_session_name}-{suffix}"
            if not request_text:
                effective_request_text = f"{effective_request_text.rstrip('.')} Use the {profile.get('label')} strategy."

    if not effective_request_text:
        raise ValueError("`request_text` is required unless `workflow_family` supplies a default prompt.")

    return {
        "request_text": effective_request_text,
        "goal": effective_goal,
        "extra_tags": effective_tags,
        "workflow_family": str(workflow.get("id")) if workflow else None,
        "strategy_profile": str(profile.get("id")) if profile else None,
        "session_name": effective_session_name,
    }


def _match_workflow_ids(request_tags: list[str], workflow_registry: dict[str, Any], routing_rules: dict[str, Any]) -> list[str]:
    tags = set(request_tags)
    matched: list[str] = []

    for rule in routing_rules.get("routing_rules", []):
        when = rule.get("when", {})
        then = rule.get("then", {})
        expected_tags = set(when.get("request_has_any_tags", []))
        proposed = list(then.get("propose_workflows", []))
        if expected_tags and proposed and tags.intersection(expected_tags):
            for workflow_id in proposed:
                if workflow_id not in matched:
                    matched.append(workflow_id)

    if matched:
        return matched

    for workflow in workflow_registry.get("workflows", []):
        workflow_tags = set(workflow.get("request_tags", []))
        if tags.intersection(workflow_tags):
            matched.append(str(workflow["id"]))

    return matched


def _example_plan_path(workflow_id: str) -> Path:
    return EXAMPLES_DIR / "plans" / f"{workflow_id}.plan.yaml"


def _strategy_profile_for_workflow(workflow_id: str, request_tags: list[str]) -> dict[str, Any] | None:
    knowledge = load_workflow_knowledge()
    tags = {str(tag) for tag in request_tags}
    for family in knowledge.get("family_templates", []):
        if str(family.get("registry_workflow_id")) != workflow_id:
            continue
        for profile in family.get("strategy_profiles", []):
            request_tag = str(profile.get("request_tag") or "")
            if request_tag and request_tag in tags:
                return dict(profile)
    return None


def _apply_strategy_profile(plan: dict[str, Any], request: dict[str, Any]) -> dict[str, Any]:
    workflow_id = str(plan.get("source_workflow_id") or "")
    profile = _strategy_profile_for_workflow(workflow_id, list(request.get("request_tags", [])))
    if not profile:
        return plan

    updated = copy.deepcopy(plan)
    updated["selected_strategy_profile"] = profile.get("id")
    updated["selected_strategy_label"] = profile.get("label")
    summary_suffix = str(profile.get("summary_suffix") or "").strip()
    if summary_suffix:
        updated["summary"] = f"{updated.get('summary', '').rstrip()} {summary_suffix}".strip()
    note = str(profile.get("note") or "").strip()
    if note:
        assumptions = list(updated.get("assumptions", []))
        if note not in assumptions:
            assumptions.append(note)
        updated["assumptions"] = assumptions

    overrides = dict(profile.get("stage_overrides", {}))
    for stage in updated.get("stages", []):
        stage_id = str(stage.get("stage_id") or "")
        override = dict(overrides.get(stage_id, {}))
        if not override:
            continue
        if "candidate_skills" in override:
            stage["candidate_skills"] = list(override["candidate_skills"])
        if "requires_user_confirmation" in override:
            stage["requires_user_confirmation"] = bool(override["requires_user_confirmation"])
        if "outputs" in override:
            stage["outputs"] = list(override["outputs"])
        if "validation" in override:
            stage["validation"] = list(override["validation"])

    return updated


def _build_generic_workflow_plan(workflow: dict[str, Any], request: dict[str, Any], strategy_type: str) -> dict[str, Any]:
    workflow_id = str(workflow["id"])
    stage_names = [str(item) for item in workflow.get("stages", [])]
    atomic_skills = [str(item) for item in workflow.get("candidate_atomic_skills", [])]
    stages: list[dict[str, Any]] = []
    for index, stage_name in enumerate(stage_names, start=1):
        requires_confirmation = strategy_type == "conservative" and index == 2
        candidate_skills = ["skill-router", *atomic_skills[:3]]
        stages.append(
            {
                "stage_id": f"s{index}",
                "name": stage_name,
                "goal": f"Execute stage `{stage_name}` for workflow `{workflow_id}`.",
                "candidate_skills": candidate_skills,
                "requires_user_confirmation": requires_confirmation,
                "outputs": [stage_name.replace("-", "_")],
                "validation": [f"{stage_name.replace('-', '_')}_completed"],
            }
        )

    plan = {
        "plan_id": f"plan_{workflow_id}_{strategy_type}",
        "request_id": request["request_id"],
        "source_workflow_id": workflow_id,
        "title": workflow.get("summary", workflow_id),
        "summary": f"{strategy_type.capitalize()} plan for workflow `{workflow_id}`.",
        "strategy_type": strategy_type,
        "assumptions": [],
        "prerequisites": [],
        "expected_outputs": stage_names,
        "risks": [],
        "estimated_cost": {
            "time": "medium" if strategy_type == "conservative" else "low",
            "compute": "medium",
        },
        "stages": stages,
        "approval_state": "draft",
    }
    return _apply_strategy_profile(plan, request)


def _build_plan_from_workflow(workflow: dict[str, Any], request: dict[str, Any], strategy_type: str) -> dict[str, Any]:
    workflow_id = str(workflow["id"])
    template_path = _example_plan_path(workflow_id)
    if template_path.exists():
        plan = load_structured_file(template_path)
        plan = copy.deepcopy(plan)
        plan["plan_id"] = f"plan_{workflow_id}_{strategy_type}"
        plan["request_id"] = request["request_id"]
        plan["source_workflow_id"] = workflow_id
        plan["strategy_type"] = strategy_type
        plan["approval_state"] = "draft"
        if strategy_type == "efficient":
            plan["summary"] = (
                f"Efficient plan for `{workflow_id}` that reduces manual pauses while keeping the same stage skeleton."
            )
            estimated_cost = dict(plan.get("estimated_cost", {}))
            estimated_cost["time"] = "low"
            plan["estimated_cost"] = estimated_cost
            for stage in plan.get("stages", []):
                if stage.get("stage_id") == "s2":
                    stage["requires_user_confirmation"] = False
        else:
            plan["summary"] = (
                f"Conservative plan for `{workflow_id}` with explicit stage validation and manual checkpoints."
            )
        return _apply_strategy_profile(plan, request)

    return _build_generic_workflow_plan(workflow, request, strategy_type)


def generate_candidate_plans(request: dict[str, Any]) -> list[dict[str, Any]]:
    workflow_registry = load_workflow_registry()
    routing_rules = load_routing_rules()
    matched_ids = _match_workflow_ids(request.get("request_tags", []), workflow_registry, routing_rules)

    workflows_by_id = {
        str(workflow["id"]): workflow
        for workflow in workflow_registry.get("workflows", [])
    }

    if matched_ids:
        workflow = workflows_by_id[matched_ids[0]]
        return [
            _build_plan_from_workflow(workflow, request, "conservative"),
            _build_plan_from_workflow(workflow, request, "efficient"),
        ]

    generic_workflow = {
        "id": "generic-bio-workflow",
        "summary": "Generic bioinformatics execution flow",
        "stages": ["request-review", "skill-routing", "execution-review"],
        "candidate_atomic_skills": ["sequence-analysis", "bioinformatics-toolkit"],
    }
    return [
        _build_generic_workflow_plan(generic_workflow, request, "conservative"),
        _build_generic_workflow_plan(generic_workflow, request, "efficient"),
    ]


def approve_plan(proposals_payload: dict[str, Any], plan_id: str) -> dict[str, Any]:
    for plan in proposals_payload.get("plans", []):
        if plan.get("plan_id") == plan_id:
            approved = copy.deepcopy(plan)
            approved["approval_state"] = "approved"
            return approved
    raise KeyError(f"Unknown plan_id: {plan_id}")


def review_plans(proposals_payload: dict[str, Any]) -> dict[str, Any]:
    plans = list(proposals_payload.get("plans", []))
    comparison: list[dict[str, Any]] = []

    for plan in plans:
        stages = list(plan.get("stages", []))
        comparison.append(
            {
                "plan_id": plan.get("plan_id"),
                "strategy_type": plan.get("strategy_type"),
                "source_workflow_id": plan.get("source_workflow_id"),
                "stage_count": len(stages),
                "risk_count": len(plan.get("risks", [])),
                "manual_confirmations": sum(
                    1 for stage in stages if stage.get("requires_user_confirmation", False)
                ),
                "estimated_cost": plan.get("estimated_cost", {}),
            }
        )

    recommended_plan_id = None
    rationale = "No plans available."
    conservative = next((item for item in comparison if item["strategy_type"] == "conservative"), None)
    efficient = next((item for item in comparison if item["strategy_type"] == "efficient"), None)

    if conservative is not None:
        recommended_plan_id = conservative["plan_id"]
        rationale = "Recommended conservative plan because it preserves explicit checkpoints and clearer validation boundaries."
    elif efficient is not None:
        recommended_plan_id = efficient["plan_id"]
        rationale = "Recommended efficient plan because it minimizes manual pauses while keeping the workflow shape intact."
    elif comparison:
        recommended_plan_id = comparison[0]["plan_id"]
        rationale = "Recommended the first available plan because no named strategy preference was available."

    return {
        "recommended_plan_id": recommended_plan_id,
        "rationale": rationale,
        "comparison": comparison,
    }


def _parse_bool_text(value: str) -> bool:
    normalized = value.strip().lower()
    if normalized in {"true", "1", "yes", "y"}:
        return True
    if normalized in {"false", "0", "no", "n"}:
        return False
    raise ValueError(f"Invalid boolean value: {value}")


def edit_plan(
    plan: dict[str, Any],
    set_summary: str | None = None,
    set_strategy: str | None = None,
    add_risks: list[str] | None = None,
    require_confirmation_updates: list[str] | None = None,
) -> dict[str, Any]:
    updated = copy.deepcopy(plan)
    structural_change = False

    if set_summary is not None:
        updated["summary"] = set_summary

    if set_strategy is not None:
        updated["strategy_type"] = set_strategy
        structural_change = True

    if add_risks:
        risks = list(updated.get("risks", []))
        for risk in add_risks:
            if risk not in risks:
                risks.append(risk)
        updated["risks"] = risks
        structural_change = True

    if require_confirmation_updates:
        stage_map = {stage["stage_id"]: stage for stage in updated.get("stages", [])}
        for item in require_confirmation_updates:
            if "=" not in item:
                raise ValueError(f"Invalid stage confirmation update: {item}")
            stage_id, raw_value = item.split("=", 1)
            if stage_id not in stage_map:
                raise KeyError(f"Unknown stage id: {stage_id}")
            stage_map[stage_id]["requires_user_confirmation"] = _parse_bool_text(raw_value)
            structural_change = True

    if structural_change and updated.get("approval_state") == "approved":
        updated["approval_state"] = "draft"

    return updated


def _merge_skill_maps() -> dict[str, dict[str, Any]]:
    dynamic_payload = build_dynamic_registry(ROOT / ".claude" / "skills")
    discovered = {
        str(item["id"]): dict(item, resolved=True)
        for item in dynamic_payload.get("skills", [])
    }

    static_registry = load_static_skill_registry()
    for item in static_registry.get("skills", []):
        skill_id = str(item["id"])
        discovered[skill_id] = {
            **discovered.get(skill_id, {}),
            **item,
            "id": skill_id,
            "resolved": True,
        }

    for skill_id, record in discovered.items():
        skill_doc_path = _resolve_repo_path(record.get("path"))
        runtime_metadata = _parse_skill_runtime_metadata(skill_doc_path)
        if runtime_metadata:
            discovered[skill_id] = {
                **record,
                **{key: value for key, value in runtime_metadata.items() if value},
            }
    return discovered


def _resolve_skill_ref(skill_id: str, skill_map: dict[str, dict[str, Any]]) -> dict[str, Any]:
    if skill_id in skill_map:
        record = skill_map[skill_id]
        command = str(record.get("command") or "").strip() or None
        local_executable = str(record.get("local_executable") or "").strip() or None
        install_hint = str(record.get("install_hint") or "").strip() or None
        runtime_kind = "tool" if command or local_executable else "prompt"
        executable_path = None
        runtime_available = True
        runtime_status = "prompt-skill"

        if runtime_kind == "tool":
            runtime_available = False
            if local_executable:
                candidate_path = Path(local_executable).expanduser()
                if candidate_path.is_file():
                    executable_path = str(candidate_path.resolve())
                    runtime_available = True
            if not runtime_available and command:
                try:
                    tokens = shlex.split(command)
                except ValueError:
                    tokens = command.split()
                if tokens:
                    resolved_binary = shutil.which(tokens[0])
                    if resolved_binary:
                        executable_path = resolved_binary
                        runtime_available = True
            runtime_status = "available" if runtime_available else "missing-local-tool"

        return {
            "id": skill_id,
            "layer": record.get("layer", "unknown"),
            "path": record.get("path"),
            "description": record.get("description", ""),
            "resolved": True,
            "runtime_kind": runtime_kind,
            "runtime_available": runtime_available,
            "runtime_status": runtime_status,
            "command": command,
            "local_executable": local_executable,
            "executable_path": executable_path,
            "install_hint": install_hint,
        }

    return {
        "id": skill_id,
        "layer": "unknown",
        "path": None,
        "description": "",
        "resolved": False,
        "runtime_kind": "unknown",
        "runtime_available": False,
        "runtime_status": "unresolved-skill",
        "command": None,
        "local_executable": None,
        "executable_path": None,
        "install_hint": None,
    }


def build_execution_draft(plan: dict[str, Any]) -> dict[str, Any]:
    skill_map = _merge_skill_maps()
    stages: list[dict[str, Any]] = []
    unresolved: set[str] = set()
    unavailable_runtime: set[str] = set()
    unmapped_stage_ids: list[str] = []

    for stage in plan.get("stages", []):
        refs = []
        for skill_id in stage.get("candidate_skills", []):
            ref = _resolve_skill_ref(str(skill_id), skill_map)
            refs.append(ref)
            if not ref["resolved"]:
                unresolved.add(str(skill_id))
            elif ref["runtime_kind"] == "tool" and not ref["runtime_available"]:
                unavailable_runtime.add(str(skill_id))
        execution_bridge = _materialize_execution_bridge(
            plan.get("source_workflow_id"),
            plan.get("selected_strategy_profile"),
            str(stage["stage_id"]),
            skill_map,
        )
        if not execution_bridge.get("contract_defined", False):
            unmapped_stage_ids.append(str(stage["stage_id"]))
        for tool_id in execution_bridge.get("unresolved_required_tools", []):
            unresolved.add(str(tool_id))
        for tool_id in execution_bridge.get("missing_local_tools", []):
            unavailable_runtime.add(str(tool_id))
        stages.append(
            {
                "stage_id": stage["stage_id"],
                "name": stage["name"],
                "goal": stage["goal"],
                "requires_user_confirmation": bool(stage.get("requires_user_confirmation", False)),
                "candidate_skill_refs": refs,
                "execution_bridge": execution_bridge,
                "validation": list(stage.get("validation", [])),
                "outputs": list(stage.get("outputs", [])),
            }
        )

    return {
        "plan_id": plan["plan_id"],
        "request_id": plan["request_id"],
        "source_workflow_id": plan.get("source_workflow_id"),
        "status": "draft",
        "stages": stages,
        "unresolved_skill_ids": sorted(unresolved),
        "unavailable_runtime_skill_ids": sorted(unavailable_runtime),
        "unmapped_stage_ids": sorted(set(unmapped_stage_ids)),
    }


def initialize_run(plan: dict[str, Any]) -> dict[str, Any]:
    stages = list(plan.get("stages", []))
    if not stages:
        raise ValueError("Plan must contain at least one stage to initialize a run.")

    stage_order = [str(stage["stage_id"]) for stage in stages]
    current_stage = stage_order[0]
    stage_status = {stage_id: "pending" for stage_id in stage_order}
    stage_context = {
        str(stage["stage_id"]): {
            "name": stage["name"],
            "goal": stage["goal"],
            "requires_user_confirmation": bool(stage.get("requires_user_confirmation", False)),
            "outputs": list(stage.get("outputs", [])),
            "validation": list(stage.get("validation", [])),
            "candidate_skills": list(stage.get("candidate_skills", [])),
        }
        for stage in stages
    }

    return {
        "run_id": f"run_{plan['plan_id']}",
        "plan_id": plan["plan_id"],
        "request_id": plan["request_id"],
        "status": "pending",
        "current_stage": current_stage,
        "stage_status": stage_status,
        "stage_order": stage_order,
        "stage_context": stage_context,
        "validation_results": {},
        "artifacts": [],
        "decisions": [],
        "issues": [],
        "resume_from": current_stage,
        "last_update": _now_iso(),
    }


def _next_stage_id(run_state: dict[str, Any], current_stage: str) -> str | None:
    stage_order = list(run_state.get("stage_order", []))
    try:
        current_index = stage_order.index(current_stage)
    except ValueError as exc:
        raise KeyError(f"Unknown current stage in run state: {current_stage}") from exc

    for stage_id in stage_order[current_index + 1 :]:
        if run_state.get("stage_status", {}).get(stage_id) in {"pending", "running"}:
            return stage_id
    return None


def _parse_validation_items(items: list[str]) -> dict[str, str]:
    parsed: dict[str, str] = {}
    for item in items:
        if "=" not in item:
            raise ValueError(f"Invalid validation assignment: {item}")
        key, value = item.split("=", 1)
        parsed[key] = value
    return parsed


def _parse_artifact_items(items: list[str]) -> list[dict[str, str]]:
    parsed: list[dict[str, str]] = []
    for item in items:
        path, artifact_type, *rest = item.split(":", 2)
        if not path or not artifact_type:
            raise ValueError(f"Invalid artifact spec: {item}")
        record = {"path": path, "type": artifact_type}
        if rest and rest[0]:
            record["description"] = rest[0]
        parsed.append(record)
    return parsed


def advance_run_stage(
    run_state: dict[str, Any],
    confirm: bool = False,
    validation_updates: list[str] | None = None,
    artifacts: list[str] | None = None,
) -> dict[str, Any]:
    updated = copy.deepcopy(run_state)
    current_stage = str(updated["current_stage"])
    stage_context = dict(updated.get("stage_context", {})).get(current_stage)
    if stage_context is None:
        raise KeyError(f"Missing stage context for {current_stage}")

    if updated.get("status") == "paused" and not confirm:
        return updated

    if stage_context.get("requires_user_confirmation", False) and not confirm:
        updated["status"] = "paused"
        updated["resume_from"] = current_stage
        updated.setdefault("issues", []).append(
            {
                "stage": current_stage,
                "severity": "warning",
                "message": f"Stage {current_stage} requires confirmation before execution.",
            }
        )
        updated["last_update"] = _now_iso()
        return updated

    updated.setdefault("stage_status", {})[current_stage] = "completed"

    validation_rules = list(stage_context.get("validation", []))
    validation_map = _parse_validation_items(validation_updates or [])
    updated.setdefault("validation_results", {})[current_stage] = {
        rule: validation_map.get(rule, "passed") for rule in validation_rules
    }

    artifact_records = _parse_artifact_items(artifacts or [])
    updated.setdefault("artifacts", []).extend(artifact_records)

    next_stage = _next_stage_id(updated, current_stage)
    if next_stage is None:
        updated["status"] = "completed"
        updated["resume_from"] = current_stage
        updated["current_stage"] = current_stage
    else:
        updated["status"] = "pending"
        updated["resume_from"] = next_stage
        updated["current_stage"] = next_stage

    updated["last_update"] = _now_iso()
    return updated


def pause_run(run_state: dict[str, Any], reason: str) -> dict[str, Any]:
    updated = copy.deepcopy(run_state)
    current_stage = str(updated["current_stage"])
    updated["status"] = "paused"
    updated["resume_from"] = current_stage
    updated.setdefault("issues", []).append(
        {
            "stage": current_stage,
            "severity": "warning",
            "message": reason,
        }
    )
    updated["last_update"] = _now_iso()
    return updated


def resume_run(run_state: dict[str, Any]) -> dict[str, Any]:
    updated = copy.deepcopy(run_state)
    updated["status"] = "pending"
    updated["resume_from"] = str(updated["current_stage"])
    updated.setdefault("decisions", []).append(
        f"Run resumed at stage {updated['current_stage']}."
    )
    updated["last_update"] = _now_iso()
    return updated


def summarize_run(run_state: dict[str, Any]) -> dict[str, Any]:
    current_stage = str(run_state["current_stage"])
    stage_status = dict(run_state.get("stage_status", {}))
    stage_context = dict(run_state.get("stage_context", {}))
    issues = list(run_state.get("issues", []))
    artifacts = list(run_state.get("artifacts", []))

    grouped_status = {
        "completed": sorted(stage_id for stage_id, state in stage_status.items() if state == "completed"),
        "pending": sorted(stage_id for stage_id, state in stage_status.items() if state == "pending"),
        "running": sorted(stage_id for stage_id, state in stage_status.items() if state == "running"),
        "failed": sorted(stage_id for stage_id, state in stage_status.items() if state == "failed"),
        "skipped": sorted(stage_id for stage_id, state in stage_status.items() if state == "skipped"),
    }
    current_context = dict(stage_context.get(current_stage, {}))
    latest_issue = issues[-1] if issues else None

    if run_state.get("status") == "paused":
        if latest_issue and "requires confirmation" in str(latest_issue.get("message", "")).lower():
            next_action = f"Confirm and resume stage {current_stage}."
        else:
            next_action = f"Review the pause reason and resume stage {current_stage} when ready."
    elif run_state.get("status") == "completed":
        next_action = "Run is complete. Review artifacts and deliver outputs."
    elif current_context.get("requires_user_confirmation", False) and current_stage in grouped_status["pending"]:
        next_action = f"Advance stage {current_stage}. Confirmation may be required before execution."
    else:
        next_action = f"Advance stage {current_stage}."

    return {
        "run_id": run_state["run_id"],
        "plan_id": run_state["plan_id"],
        "request_id": run_state["request_id"],
        "status": run_state["status"],
        "current_stage": current_stage,
        "resume_from": run_state.get("resume_from"),
        "progress": {
            "total": len(stage_status),
            "completed": len(grouped_status["completed"]),
            "pending": len(grouped_status["pending"]),
            "failed": len(grouped_status["failed"]),
            "skipped": len(grouped_status["skipped"]),
        },
        "stage_groups": grouped_status,
        "current_stage_context": current_context,
        "latest_issue": latest_issue,
        "recent_artifacts": artifacts[-3:],
        "next_action": next_action,
        "last_update": run_state.get("last_update"),
    }


def review_run(
    run_state: dict[str, Any],
    execution_draft: dict[str, Any] | None = None,
) -> dict[str, Any]:
    current_stage = str(run_state["current_stage"])
    status = str(run_state.get("status", "pending"))
    stage_status = dict(run_state.get("stage_status", {}))
    stage_context = dict(run_state.get("stage_context", {}))
    validation_results = dict(run_state.get("validation_results", {}))
    issues = list(run_state.get("issues", []))
    artifacts = list(run_state.get("artifacts", []))

    current_context = dict(stage_context.get(current_stage, {}))
    latest_issue = issues[-1] if issues else None

    draft_stage_map: dict[str, dict[str, Any]] = {}
    unresolved_skill_ids: list[str] = []
    if execution_draft is not None:
        draft_stage_map = {
            str(stage["stage_id"]): dict(stage)
            for stage in execution_draft.get("stages", [])
        }
        unresolved_skill_ids = sorted(set(str(item) for item in execution_draft.get("unresolved_skill_ids", [])))

    current_draft = dict(draft_stage_map.get(current_stage, {}))
    current_skill_refs = list(current_draft.get("candidate_skill_refs", []))
    current_execution_bridge = dict(current_draft.get("execution_bridge", {}))
    current_unresolved_skills = sorted(
        {
            *(str(item["id"]) for item in current_skill_refs if not item.get("resolved", False)),
            *(str(item) for item in current_execution_bridge.get("unresolved_required_tools", [])),
        }
    )
    current_missing_local_tools = sorted(
        {
            *(
                str(item["id"])
                for item in current_skill_refs
                if item.get("resolved", False)
                and item.get("runtime_kind") == "tool"
                and not item.get("runtime_available", False)
            ),
            *(str(item) for item in current_execution_bridge.get("missing_local_tools", [])),
        }
    )

    pending_or_running_stage_ids = [
        stage_id for stage_id, state in stage_status.items() if state in {"pending", "running"}
    ]
    completed_stage_ids = [
        stage_id for stage_id, state in stage_status.items() if state == "completed"
    ]

    future_unresolved_skills = sorted(
        {
            *(
                str(item["id"])
                for stage_id in pending_or_running_stage_ids
                if stage_id != current_stage
                for item in list(dict(draft_stage_map.get(stage_id, {})).get("candidate_skill_refs", []))
                if not item.get("resolved", False)
            ),
            *(
                str(item)
                for stage_id in pending_or_running_stage_ids
                if stage_id != current_stage
                for item in list(dict(draft_stage_map.get(stage_id, {})).get("execution_bridge", {}).get("unresolved_required_tools", []))
            ),
        }
    )
    future_missing_local_tools = sorted(
        {
            *(
                str(item["id"])
                for stage_id in pending_or_running_stage_ids
                if stage_id != current_stage
                for item in list(dict(draft_stage_map.get(stage_id, {})).get("candidate_skill_refs", []))
                if item.get("resolved", False)
                and item.get("runtime_kind") == "tool"
                and not item.get("runtime_available", False)
            ),
            *(
                str(item)
                for stage_id in pending_or_running_stage_ids
                if stage_id != current_stage
                for item in list(dict(draft_stage_map.get(stage_id, {})).get("execution_bridge", {}).get("missing_local_tools", []))
            ),
        }
    )
    completed_missing_local_tools = sorted(
        {
            str(item["id"])
            for stage_id in completed_stage_ids
            for item in list(dict(draft_stage_map.get(stage_id, {})).get("candidate_skill_refs", []))
            if item.get("resolved", False)
            and item.get("runtime_kind") == "tool"
            and not item.get("runtime_available", False)
        }
    )
    missing_execution_bridge_contracts = sorted(
        str(stage_id)
        for stage_id in pending_or_running_stage_ids
        if stage_id != current_stage
        and not dict(draft_stage_map.get(stage_id, {})).get("execution_bridge", {}).get("contract_defined", False)
    )

    completed_stage_reviews: list[dict[str, Any]] = []
    validation_gaps: list[dict[str, Any]] = []
    for stage_id, state in stage_status.items():
        context = dict(stage_context.get(stage_id, {}))
        expected_rules = list(context.get("validation", []))
        recorded = dict(validation_results.get(stage_id, {}))
        missing_rules = sorted(rule for rule in expected_rules if rule not in recorded)
        review = {
            "stage_id": stage_id,
            "status": state,
            "validation_rules": expected_rules,
            "recorded_validations": recorded,
            "missing_validations": missing_rules,
            "validation_complete": not missing_rules,
        }
        if state == "completed":
            completed_stage_reviews.append(review)
            if missing_rules:
                validation_gaps.append(
                    {
                        "type": "validation_gap",
                        "stage": stage_id,
                        "message": f"Completed stage {stage_id} is missing validation evidence.",
                        "missing_validations": missing_rules,
                    }
                )

    blocking_issues: list[dict[str, Any]] = []
    if (
        status == "paused"
        and current_context.get("requires_user_confirmation", False)
        and latest_issue is not None
        and "requires confirmation" in str(latest_issue.get("message", "")).lower()
    ):
        blocking_issues.append(
            {
                "type": "confirmation_required",
                "stage": current_stage,
                "message": str(latest_issue["message"]),
            }
        )
    if current_unresolved_skills:
        blocking_issues.append(
            {
                "type": "unresolved_current_stage_skills",
                "stage": current_stage,
                "message": f"Current stage {current_stage} has unresolved candidate skills.",
                "skills": current_unresolved_skills,
            }
        )
    if current_missing_local_tools:
        blocking_issues.append(
            {
                "type": "missing_local_tools",
                "stage": current_stage,
                "message": f"Current stage {current_stage} requires tools that are not available on this machine.",
                "skills": current_missing_local_tools,
            }
        )
    blocking_issues.extend(validation_gaps)

    future_issues: list[dict[str, Any]] = []
    if future_unresolved_skills:
        future_issues.append(
            {
                "type": "future_unresolved_skills",
                "message": "Later stages still contain unresolved candidate skills.",
                "skills": future_unresolved_skills,
            }
        )
    if future_missing_local_tools:
        future_issues.append(
            {
                "type": "future_missing_local_tools",
                "message": "Later pending stages still depend on tools that are not available on this machine.",
                "skills": future_missing_local_tools,
            }
        )
    if missing_execution_bridge_contracts:
        future_issues.append(
            {
                "type": "future_missing_execution_bridge_contracts",
                "message": "Later pending stages do not yet have formal execution bridge contracts.",
                "stage_ids": missing_execution_bridge_contracts,
            }
        )
    for stage_id, context in stage_context.items():
        if stage_id == current_stage or stage_status.get(stage_id) != "pending":
            continue
        if context.get("requires_user_confirmation", False):
            future_issues.append(
                {
                    "type": "future_confirmation_gate",
                    "stage": stage_id,
                    "message": f"Stage {stage_id} will require explicit confirmation before execution.",
                }
            )

    delivery_issues: list[dict[str, Any]] = []
    if completed_missing_local_tools:
        delivery_issues.append(
            {
                "type": "completed_stage_missing_local_tools",
                "message": "Completed stages depended on tools that are not available on this machine.",
                "skills": completed_missing_local_tools,
            }
        )

    if status == "completed":
        if delivery_issues:
            verdict = "completed_with_environment_gaps"
            summary = "Run reached completed state, but some completed stages depended on tools unavailable on this machine."
        else:
            verdict = "ready_to_deliver"
            summary = "Run completed. Review artifacts and deliver outputs."
    elif any(item["type"] == "confirmation_required" for item in blocking_issues):
        verdict = "awaiting_confirmation"
        summary = f"Run is paused at {current_stage} and needs explicit confirmation."
    elif blocking_issues:
        verdict = "blocked"
        summary = f"Run has blocking issues at or before {current_stage}."
    elif status == "paused":
        verdict = "paused_manual_review"
        summary = f"Run is paused at {current_stage} for manual review."
    else:
        verdict = "ready_to_continue"
        summary = f"Run can continue from {current_stage}."

    next_action = summarize_run(run_state)["next_action"]

    return {
        "run_id": run_state["run_id"],
        "plan_id": run_state["plan_id"],
        "request_id": run_state["request_id"],
        "status": status,
        "current_stage": current_stage,
        "resume_from": run_state.get("resume_from"),
        "verdict": verdict,
        "summary": summary,
        "blocking_issues": blocking_issues,
        "future_issues": future_issues,
        "delivery_issues": delivery_issues,
        "artifact_count": len(artifacts),
        "current_stage_review": {
            "stage_id": current_stage,
            "name": current_context.get("name"),
            "status": stage_status.get(current_stage, "pending"),
            "confirmation_required": bool(current_context.get("requires_user_confirmation", False)),
            "candidate_skills": list(current_context.get("candidate_skills", [])),
            "execution_bridge": current_execution_bridge,
            "unresolved_skills": current_unresolved_skills,
            "missing_local_tools": current_missing_local_tools,
            "validation_rules": list(current_context.get("validation", [])),
            "recorded_validations": dict(validation_results.get(current_stage, {})),
        },
        "completed_stage_reviews": completed_stage_reviews,
        "next_action": next_action,
        "last_update": run_state.get("last_update"),
    }


def start_session(
    session_dir: Path,
    request_text: str | None,
    goal: str | None = None,
    extra_tags: list[str] | None = None,
    workflow_family: str | None = None,
    strategy_profile: str | None = None,
) -> dict[str, Any]:
    session_dir = _ensure_session_directory(session_dir, require_empty=True)
    resolved = prepare_session_start_inputs(
        request_text=request_text,
        goal=goal,
        extra_tags=extra_tags,
        workflow_family=workflow_family,
        strategy_profile=strategy_profile,
    )
    request = build_request(
        request_text=resolved["request_text"],
        goal=resolved["goal"],
        extra_tags=resolved["extra_tags"],
    )
    proposals = {
        "request": request,
        "plans": generate_candidate_plans(request),
    }
    bundle = {
        "request": request,
        "plans": proposals,
    }
    _append_history_event(
        bundle,
        session_dir,
        event_type="session_started",
        message="Session started and candidate plans were generated.",
        data={
            "request_id": request.get("request_id"),
            "plan_count": len(proposals.get("plans", [])),
            "workflow_family": resolved.get("workflow_family"),
            "strategy_profile": resolved.get("strategy_profile"),
        },
    )
    return _sync_session_bundle(session_dir, bundle)["session"]


def approve_session_plan(
    session_dir: Path,
    plan_id: str | None = None,
    plan_file: Path | None = None,
    reason: str | None = None,
) -> dict[str, Any]:
    session_dir = _ensure_session_directory(session_dir, must_exist=True)
    bundle = _load_session_bundle(session_dir)
    request = dict(bundle.get("request", {}))
    proposals = dict(bundle.get("plans", {}))

    if not request or not proposals:
        raise FileNotFoundError(
            f"Session is missing request/plans artifacts: {session_dir}"
        )

    if bool(plan_id) == bool(plan_file):
        raise ValueError("Provide exactly one of `plan_id` or `plan_file`.")

    if plan_id is not None:
        approved_plan = approve_plan(proposals, plan_id)
    else:
        approved_plan = load_plan_document(Path(plan_file).resolve())
        approved_plan = copy.deepcopy(approved_plan)
        if approved_plan.get("request_id") != request.get("request_id"):
            raise ValueError(
                "Edited plan request_id does not match the session request_id."
            )
        approved_plan["approval_state"] = "approved"

    baseline_plan = _baseline_plan_for_approval(bundle, approved_plan)
    plan_diff = build_plan_diff_summary(baseline_plan, approved_plan)
    execution_draft = build_execution_draft(approved_plan)
    run_state = initialize_run(approved_plan)
    approval_message = f"Approved plan {approved_plan['plan_id']}."
    if reason:
        approval_message = f"{approval_message} Reason: {reason}"
    run_state.setdefault("decisions", []).append(approval_message)
    if plan_diff.get("changed"):
        summary_lines = plan_diff.get("summary_lines", [])
        run_state["decisions"].append(
            "Plan changes vs baseline: "
            + (" ".join(summary_lines[:3]) if summary_lines else "Structured edits detected.")
        )

    bundle["approved_plan"] = approved_plan
    bundle["execution_draft"] = execution_draft
    bundle["run"] = run_state
    _append_history_event(
        bundle,
        session_dir,
        event_type="plan_approved",
        message=approval_message,
        data={
            "approved_plan_id": approved_plan.get("plan_id"),
            "reason": reason,
            "source": "plan_id" if plan_id is not None else "plan_file",
            "plan_diff": plan_diff,
        },
    )

    return _sync_session_bundle(session_dir, bundle)["session"]


def _stage_missing_local_tools(execution_draft: dict[str, Any] | None, stage_id: str) -> list[str]:
    if not isinstance(execution_draft, dict):
        return []
    for stage in execution_draft.get("stages", []):
        if isinstance(stage, dict) and str(stage.get("stage_id")) == stage_id:
            return sorted(
                str(item["id"])
                for item in stage.get("candidate_skill_refs", [])
                if isinstance(item, dict)
                and item.get("resolved", False)
                and item.get("runtime_kind") == "tool"
                and not item.get("runtime_available", False)
            )
    return []


def advance_session_run(
    session_dir: Path,
    confirm: bool = False,
    validation_updates: list[str] | None = None,
    artifacts: list[str] | None = None,
    allow_missing_tools: bool = False,
) -> dict[str, Any]:
    session_dir = _ensure_session_directory(session_dir, must_exist=True)
    bundle = _load_session_bundle(session_dir)
    run_state = bundle.get("run")
    if not isinstance(run_state, dict):
        raise FileNotFoundError(
            f"Session is missing run.json and cannot advance: {session_dir}"
        )

    previous_stage = str(run_state.get("current_stage"))
    current_stage_missing_tools = _stage_missing_local_tools(bundle.get("execution_draft"), previous_stage)
    if current_stage_missing_tools and not allow_missing_tools:
        paused_run = copy.deepcopy(run_state)
        paused_run["status"] = "paused"
        paused_run["resume_from"] = previous_stage
        paused_run.setdefault("issues", []).append(
            {
                "stage": previous_stage,
                "severity": "error",
                "message": (
                    f"Stage {previous_stage} cannot execute locally because required tools are unavailable: "
                    + ", ".join(current_stage_missing_tools)
                ),
            }
        )
        paused_run["last_update"] = _now_iso()
        bundle["run"] = paused_run
        _append_history_event(
            bundle,
            session_dir,
            event_type="run_blocked",
            message=f"Run blocked at stage {previous_stage} because local tools are unavailable.",
            data={
                "stage": previous_stage,
                "missing_local_tools": current_stage_missing_tools,
            },
        )
        return _sync_session_bundle(session_dir, bundle)["session"]

    bundle["run"] = advance_run_stage(
        run_state,
        confirm=confirm,
        validation_updates=validation_updates,
        artifacts=artifacts,
    )
    updated_run = bundle["run"]
    if current_stage_missing_tools and allow_missing_tools:
        updated_run.setdefault("decisions", []).append(
            "Manual override: advanced despite missing local tools for stage "
            f"{previous_stage}: {', '.join(current_stage_missing_tools)}."
        )
    message = f"Advanced run from stage {previous_stage} to {updated_run.get('current_stage')}."
    if updated_run.get("status") == "paused":
        message = f"Run paused at stage {updated_run.get('current_stage')}."
    elif updated_run.get("status") == "completed":
        message = "Run completed."
    _append_history_event(
        bundle,
        session_dir,
        event_type="run_advanced",
        message=message,
        data={
            "from_stage": previous_stage,
            "to_stage": updated_run.get("current_stage"),
            "status": updated_run.get("status"),
            "confirm": confirm,
        },
    )
    return _sync_session_bundle(session_dir, bundle)["session"]


def pause_session_run(session_dir: Path, reason: str) -> dict[str, Any]:
    session_dir = _ensure_session_directory(session_dir, must_exist=True)
    bundle = _load_session_bundle(session_dir)
    run_state = bundle.get("run")
    if not isinstance(run_state, dict):
        raise FileNotFoundError(
            f"Session is missing run.json and cannot pause: {session_dir}"
        )

    bundle["run"] = pause_run(run_state, reason)
    _append_history_event(
        bundle,
        session_dir,
        event_type="run_paused",
        message=f"Run paused: {reason}",
        data={
            "stage": bundle["run"].get("current_stage"),
            "reason": reason,
        },
    )
    return _sync_session_bundle(session_dir, bundle)["session"]


def resume_session_run(session_dir: Path) -> dict[str, Any]:
    session_dir = _ensure_session_directory(session_dir, must_exist=True)
    bundle = _load_session_bundle(session_dir)
    run_state = bundle.get("run")
    if not isinstance(run_state, dict):
        raise FileNotFoundError(
            f"Session is missing run.json and cannot resume: {session_dir}"
        )

    bundle["run"] = resume_run(run_state)
    _append_history_event(
        bundle,
        session_dir,
        event_type="run_resumed",
        message=f"Run resumed at stage {bundle['run'].get('current_stage')}.",
        data={
            "stage": bundle["run"].get("current_stage"),
        },
    )
    return _sync_session_bundle(session_dir, bundle)["session"]


def session_status(session_dir: Path) -> dict[str, Any]:
    session_dir = _ensure_session_directory(session_dir, must_exist=True)
    bundle = _sync_session_bundle(session_dir, _load_session_bundle(session_dir))
    return {
        "session": bundle["session"],
        "review": bundle.get("review"),
        "run_status": bundle.get("run_status"),
        "run_review": bundle.get("run_review"),
        "history": bundle.get("history"),
        "skill_crystallization_candidate": session_skill_crystallization_candidate(session_dir),
    }


def render_session_plan_markdown(
    session_dir: Path,
    plan_id: str | None = None,
    approved: bool = False,
) -> str:
    session_dir = _ensure_session_directory(session_dir, must_exist=True)
    bundle = _sync_session_bundle(session_dir, _load_session_bundle(session_dir))
    plan = _pick_session_plan(bundle, plan_id=plan_id, approved=approved)
    return render_plan_markdown(plan, session_manifest=bundle.get("session"))


def _console_candidate_plans(bundle: dict[str, Any]) -> list[dict[str, Any]]:
    review = dict(bundle.get("review", {}))
    recommended_plan_id = review.get("recommended_plan_id")
    plans_payload = dict(bundle.get("plans", {}))
    items: list[dict[str, Any]] = []

    for plan in plans_payload.get("plans", []):
        if not isinstance(plan, dict):
            continue
        stages = list(plan.get("stages", []))
        items.append(
            {
                "plan_id": plan.get("plan_id"),
                "strategy_type": plan.get("strategy_type"),
                "source_workflow_id": plan.get("source_workflow_id"),
                "selected_strategy_profile": plan.get("selected_strategy_profile"),
                "selected_strategy_label": plan.get("selected_strategy_label"),
                "summary": plan.get("summary", ""),
                "stage_count": len(stages),
                "risk_count": len(plan.get("risks", [])),
                "manual_confirmations": sum(
                    1 for stage in stages if isinstance(stage, dict) and stage.get("requires_user_confirmation", False)
                ),
                "estimated_cost": dict(plan.get("estimated_cost", {})),
                "recommended": plan.get("plan_id") == recommended_plan_id,
            }
        )

    return items


def _skill_slug(value: str) -> str:
    slug = _slugify(value).replace('-', '_')
    return slug or 'generated_workflow_skill'


def _copy_session_repro_bundle(session_dir: Path, references_dir: Path) -> dict[str, str]:
    repro_dir = session_dir / "repro"
    if not repro_dir.exists() or not repro_dir.is_dir():
        return {}

    target_dir = references_dir / "repro"
    target_dir.mkdir(parents=True, exist_ok=True)
    copied: dict[str, str] = {}
    for name in ("commands.sh", "environment.json", "artifacts.json", "scorecard.json"):
        source = repro_dir / name
        if not source.exists() or not source.is_file():
            continue
        destination = target_dir / name
        shutil.copy2(source, destination)
        copied[name] = str(destination)
    return copied


def export_session_as_skill(
    *,
    session_dir: Path,
    skill_root: Path,
    skill_name: str | None = None,
    overwrite: bool = False,
    force: bool = False,
) -> dict[str, Any]:
    session_dir = _ensure_session_directory(session_dir, must_exist=True)
    bundle = _sync_session_bundle(session_dir, _load_session_bundle(session_dir))
    session = dict(bundle.get('session', {}))
    if str(session.get('run_status') or '') != 'completed':
        raise ValueError('Only completed sessions can be exported as persistent workflow skills.')

    candidate = session_skill_crystallization_candidate(session_dir)
    if not candidate.get('eligible', False) and not force:
        raise ValueError('Session is not eligible for automatic skill crystallization: ' + '; '.join(candidate.get('reasons', [])))

    approved_plan = dict(bundle.get('approved_plan', {}))
    workflow_id = str(approved_plan.get('source_workflow_id') or session.get('approved_plan_id') or session_dir.name)
    strategy_profile = str(approved_plan.get('selected_strategy_profile') or approved_plan.get('strategy_type') or 'default')
    slug = _skill_slug(skill_name or f'{workflow_id}-{strategy_profile}')

    target_dir = skill_root.expanduser().resolve() / 'workflow' / slug
    references_dir = target_dir / 'references'
    skill_path = target_dir / 'SKILL.md'
    summary_path = references_dir / 'session-summary.json'
    environment_path = references_dir / 'environment.json'

    if target_dir.exists() and not overwrite:
        raise FileExistsError(f'Generated skill directory already exists: {target_dir}')

    references_dir.mkdir(parents=True, exist_ok=True)

    analysis_flow = analysis_flow_for_workflow(workflow_id)
    benchmark_matches = bundle_benchmark_matches(bundle, workflow_id)
    execution_draft = dict(bundle.get('execution_draft', {}))
    run_state = dict(bundle.get('run', {}))
    repro_files = _copy_session_repro_bundle(session_dir, references_dir)
    expected_outputs = list(approved_plan.get('expected_outputs', []))
    stage_lines = []
    for stage in approved_plan.get('stages', []):
        if not isinstance(stage, dict):
            continue
        draft_stage = next((item for item in execution_draft.get('stages', []) if str(item.get('stage_id')) == str(stage.get('stage_id'))), {})
        bridge = dict(draft_stage.get('execution_bridge', {}))
        bridge_copy = bridge.get('bridge_id') or 'unmapped-bridge'
        stage_lines.append(
            f"- `{stage.get('stage_id')}` {stage.get('name')}: {stage.get('goal')} | bridge={bridge_copy} | confirm={'yes' if stage.get('requires_user_confirmation') else 'no'}"
        )

    benchmark_lines = []
    for item in benchmark_matches:
        benchmark_lines.append(
            f"- `{item.get('benchmark_id')}` / `{item.get('task_id')}`: verdict={item.get('verdict')} outputs={'ok' if item.get('outputs_complete') else 'gap'} delivery={'ok' if item.get('delivery_complete') else 'gap'}"
        )

    flow_lines = []
    if analysis_flow:
        for stage in analysis_flow.get('stage_flows', []):
            flow_lines.append(
                f"- `{stage.get('stage_id')}` {stage.get('label')}: consumes {', '.join(stage.get('consumes', []))} -> produces {', '.join(stage.get('produces', []))}"
            )

    decision_lines = [f'- {item}' for item in run_state.get('decisions', []) if str(item).strip()]
    repro_lines = [f'- `references/repro/{name}`' for name in sorted(repro_files)]

    skill_lines = [
        '---',
        f'name: {slug}',
        f'description: Generated workflow skill from completed session {session.get("session_id")} for {workflow_id}.',
        'user-invocable: true',
        '---',
        '',
        f'# {slug}',
        '',
        '## Origin',
        f'- Session ID: `{session.get("session_id")}`',
        f'- Session Dir: `{session.get("session_dir")}`',
        f'- Workflow: `{workflow_id}`',
        f'- Approved Plan: `{approved_plan.get("plan_id")}`',
        f'- Strategy: `{approved_plan.get("selected_strategy_profile") or approved_plan.get("strategy_type")}`',
        '',
        '## When To Use',
        f'- Use when you need a workflow shaped like `{workflow_id}` with the same staged control semantics captured by this completed session.',
        '',
        '## Expected Outputs',
    ]
    skill_lines.extend([f'- {item}' for item in expected_outputs] or ['- No explicit expected outputs recorded.'])
    skill_lines.extend(['', '## Stage Skeleton'])
    skill_lines.extend(stage_lines or ['- No stage skeleton recorded.'])
    skill_lines.extend(['', '## Analysis Flow'])
    skill_lines.extend(flow_lines or ['- No grounded analysis flow attached.'])
    skill_lines.extend(['', '## Benchmark Fit'])
    skill_lines.extend(benchmark_lines or ['- No benchmark matches attached.'])
    skill_lines.extend(['', '## Run Decisions'])
    skill_lines.extend(decision_lines or ['- No explicit run decisions recorded.'])
    skill_lines.extend(['', '## Execution Evidence'])
    skill_lines.extend(repro_lines or ['- No reproducibility bundle was copied from the source session.'])
    skill_lines.extend(['', '## Persistent References', f'- Session summary JSON: `references/{summary_path.name}`', f'- Environment JSON: `references/{environment_path.name}`'])
    skill_markdown = "\n".join(skill_lines) + '\n'

    summary_payload = {
        'session': session,
        'approved_plan': approved_plan,
        'analysis_flow': analysis_flow,
        'benchmark_matches': benchmark_matches,
        'skill_crystallization_candidate': candidate,
        'history': dict(bundle.get('history', {})),
        'run': run_state,
        'copied_repro_files': repro_files,
        'execution_bridge_summary': {
            'unmapped_stage_ids': list(execution_draft.get('unmapped_stage_ids', [])),
            'unavailable_runtime_skill_ids': list(execution_draft.get('unavailable_runtime_skill_ids', [])),
        },
    }

    skill_path.write_text(skill_markdown, encoding='utf-8')
    save_json(summary_payload, summary_path)
    save_json(candidate.get('environment', {}), environment_path)

    return {
        'skill_id': slug,
        'skill_dir': str(target_dir),
        'eligibility': candidate,
        'files': {
            'skill_markdown': str(skill_path),
            'session_summary': str(summary_path),
            'environment': str(environment_path),
        },
    }


def export_session_console_bundle(
    session_dir: Path,
    *,
    scenario_name: str | None = None,
    scenario_note: str | None = None,
) -> dict[str, Any]:
    session_dir = _ensure_session_directory(session_dir, must_exist=True)
    bundle = _sync_session_bundle(session_dir, _load_session_bundle(session_dir))

    session = dict(bundle.get("session", {}))
    approved_plan = dict(bundle.get("approved_plan", {}))
    run_status = dict(bundle.get("run_status", {}))
    run_review = dict(bundle.get("run_review", {}))
    request = dict(bundle.get("request", {}))

    workflow_id = approved_plan.get("source_workflow_id")
    if workflow_id is None:
        workflow_id = next(
            (
                plan.get("source_workflow_id")
                for plan in dict(bundle.get("plans", {})).get("plans", [])
                if isinstance(plan, dict) and plan.get("source_workflow_id")
            ),
            "unknown-workflow",
        )

    note = scenario_note
    if note is None:
        note = (
            f"Exported from session `{session.get('session_id', session_dir.name)}` "
            f"with status `{session.get('status', run_status.get('status', 'unknown'))}`."
        )

    return {
        "scenario": {
            "name": scenario_name or f"{session.get('session_id', session_dir.name)} console bundle",
            "workflow_id": workflow_id,
            "note": note,
        },
        "request": request,
        "analysis_flow": analysis_flow_for_workflow(workflow_id),
        "skill_crystallization_candidate": session_skill_crystallization_candidate(session_dir),
        "execution_bridge_summary": {
            "unmapped_stage_ids": list(dict(bundle.get("execution_draft", {})).get("unmapped_stage_ids", [])),
            "unavailable_runtime_skill_ids": list(dict(bundle.get("execution_draft", {})).get("unavailable_runtime_skill_ids", [])),
        },
        "benchmark_matches": bundle_benchmark_matches(bundle, workflow_id),
        "candidate_plans": _console_candidate_plans(bundle),
        "review": dict(bundle.get("review", {})),
        "session": session,
        "approved_plan": approved_plan,
        "execution_draft": dict(bundle.get("execution_draft", {})),
        "run_state": dict(bundle.get("run", {})),
        "run_status": run_status,
        "run_review": run_review,
        "history": dict(bundle.get("history", {})),
    }

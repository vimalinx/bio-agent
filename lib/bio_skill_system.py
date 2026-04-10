from __future__ import annotations

import copy
import json
import re
import shlex
import shutil
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


def analysis_flow_for_workflow(workflow_id: str | None) -> dict[str, Any] | None:
    if not workflow_id:
        return None
    for flow in load_analysis_flows().get("flows", []):
        if str(flow.get("workflow_id")) == str(workflow_id):
            return copy.deepcopy(flow)
    return None


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

    for stage in plan.get("stages", []):
        refs = []
        for skill_id in stage.get("candidate_skills", []):
            ref = _resolve_skill_ref(str(skill_id), skill_map)
            refs.append(ref)
            if not ref["resolved"]:
                unresolved.add(str(skill_id))
            elif ref["runtime_kind"] == "tool" and not ref["runtime_available"]:
                unavailable_runtime.add(str(skill_id))
        stages.append(
            {
                "stage_id": stage["stage_id"],
                "name": stage["name"],
                "goal": stage["goal"],
                "requires_user_confirmation": bool(stage.get("requires_user_confirmation", False)),
                "candidate_skill_refs": refs,
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
    current_unresolved_skills = sorted(
        str(item["id"]) for item in current_skill_refs if not item.get("resolved", False)
    )
    current_missing_local_tools = sorted(
        str(item["id"])
        for item in current_skill_refs
        if item.get("resolved", False)
        and item.get("runtime_kind") == "tool"
        and not item.get("runtime_available", False)
    )

    pending_or_running_stage_ids = [
        stage_id for stage_id, state in stage_status.items() if state in {"pending", "running"}
    ]
    completed_stage_ids = [
        stage_id for stage_id, state in stage_status.items() if state == "completed"
    ]

    future_unresolved_skills = sorted(
        {
            str(item["id"])
            for stage_id in pending_or_running_stage_ids
            if stage_id != current_stage
            for item in list(dict(draft_stage_map.get(stage_id, {})).get("candidate_skill_refs", []))
            if not item.get("resolved", False)
        }
    )
    future_missing_local_tools = sorted(
        {
            str(item["id"])
            for stage_id in pending_or_running_stage_ids
            if stage_id != current_stage
            for item in list(dict(draft_stage_map.get(stage_id, {})).get("candidate_skill_refs", []))
            if item.get("resolved", False)
            and item.get("runtime_kind") == "tool"
            and not item.get("runtime_available", False)
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

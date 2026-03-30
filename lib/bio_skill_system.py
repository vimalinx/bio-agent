from __future__ import annotations

import copy
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

from scripts.skills.export_skill_registry import build_registry as build_dynamic_registry


ROOT = Path(__file__).resolve().parents[1]
REGISTRY_DIR = ROOT / "registry"
EXAMPLES_DIR = ROOT / "examples"


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


def save_json(payload: dict[str, Any], output_path: Path | None = None) -> str:
    text = json.dumps(payload, indent=2, ensure_ascii=False) + "\n"
    if output_path is not None:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(text, encoding="utf-8")
    return text


def _now_iso() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def load_workflow_registry() -> dict[str, Any]:
    return _load_yaml(REGISTRY_DIR / "workflows.yaml")


def load_routing_rules() -> dict[str, Any]:
    return _load_yaml(REGISTRY_DIR / "routing_rules.yaml")


def load_static_skill_registry() -> dict[str, Any]:
    return _load_yaml(REGISTRY_DIR / "skills.yaml")


def infer_request_tags(request_text: str, goal: str | None, extra_tags: list[str], workflows: list[dict[str, Any]]) -> list[str]:
    normalized = f"{request_text} {goal or ''}".lower()
    tags: set[str] = {tag.strip().lower() for tag in extra_tags if tag.strip()}

    heuristic_tags = {
        "rnaseq": ["rna-seq", "rna seq", "rnaseq"],
        "differential-expression": ["differential expression", "de analysis", "de results"],
        "fastq": ["fastq", "fastqs"],
        "bulk-transcriptomics": ["bulk rna", "bulk transcriptomics", "bulk rna-seq"],
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

    return {
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
        return plan

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
    return discovered


def _resolve_skill_ref(skill_id: str, skill_map: dict[str, dict[str, Any]]) -> dict[str, Any]:
    if skill_id in skill_map:
        record = skill_map[skill_id]
        return {
            "id": skill_id,
            "layer": record.get("layer", "unknown"),
            "path": record.get("path"),
            "description": record.get("description", ""),
            "resolved": True,
        }

    return {
        "id": skill_id,
        "layer": "unknown",
        "path": None,
        "description": "",
        "resolved": False,
    }


def build_execution_draft(plan: dict[str, Any]) -> dict[str, Any]:
    skill_map = _merge_skill_maps()
    stages: list[dict[str, Any]] = []
    unresolved: set[str] = set()

    for stage in plan.get("stages", []):
        refs = []
        for skill_id in stage.get("candidate_skills", []):
            ref = _resolve_skill_ref(str(skill_id), skill_map)
            refs.append(ref)
            if not ref["resolved"]:
                unresolved.add(str(skill_id))
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
    future_unresolved_skills = sorted(
        skill_id for skill_id in unresolved_skill_ids if skill_id not in current_unresolved_skills
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

    if status == "completed":
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
        "artifact_count": len(artifacts),
        "current_stage_review": {
            "stage_id": current_stage,
            "name": current_context.get("name"),
            "status": stage_status.get(current_stage, "pending"),
            "confirmation_required": bool(current_context.get("requires_user_confirmation", False)),
            "candidate_skills": list(current_context.get("candidate_skills", [])),
            "unresolved_skills": current_unresolved_skills,
            "validation_rules": list(current_context.get("validation", [])),
            "recorded_validations": dict(validation_results.get(current_stage, {})),
        },
        "completed_stage_reviews": completed_stage_reviews,
        "next_action": next_action,
        "last_update": run_state.get("last_update"),
    }

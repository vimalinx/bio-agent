from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CLI_SCRIPT = ROOT / "scripts" / "bio_skill_system.py"


def run_cli(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(CLI_SCRIPT), *args],
        check=True,
        capture_output=True,
        text=True,
    )


def prepare_approved_plan(tmp_path: Path, request_text: str, goal: str) -> Path:
    proposals_path = tmp_path / "plans.json"
    approved_path = tmp_path / "approved-plan.json"

    run_cli(
        "propose",
        "--request-text",
        request_text,
        "--goal",
        goal,
        "--output",
        str(proposals_path),
    )

    proposals = json.loads(proposals_path.read_text(encoding="utf-8"))
    selected_plan_id = proposals["plans"][0]["plan_id"]

    run_cli(
        "approve",
        "--plans-file",
        str(proposals_path),
        "--plan-id",
        selected_plan_id,
        "--output",
        str(approved_path),
    )

    return approved_path


def test_propose_generates_multiple_plans_for_rnaseq_request(tmp_path: Path) -> None:
    output_path = tmp_path / "plans.json"

    run_cli(
        "propose",
        "--request-text",
        "I have bulk RNA-seq FASTQ files for treated and control samples and want a differential expression result bundle.",
        "--goal",
        "Generate candidate plans for RNA-seq differential expression analysis.",
        "--output",
        str(output_path),
    )

    payload = json.loads(output_path.read_text(encoding="utf-8"))

    assert payload["request"]["request_id"].startswith("req_")
    assert "rnaseq" in payload["request"]["request_tags"]
    assert len(payload["plans"]) >= 2
    strategies = {plan["strategy_type"] for plan in payload["plans"]}
    assert {"conservative", "efficient"}.issubset(strategies)
    assert any(plan["source_workflow_id"] == "rnaseq-differential-expression" for plan in payload["plans"])


def test_approve_and_draft_create_execution_mapping(tmp_path: Path) -> None:
    draft_path = tmp_path / "execution-draft.json"
    approved_plan_path = prepare_approved_plan(
        tmp_path,
        "I need an RNA-seq differential expression workflow for treated and control samples.",
        "Plan the analysis and prepare execution routing.",
    )

    approved_plan = json.loads(approved_plan_path.read_text(encoding="utf-8"))
    assert approved_plan["approval_state"] == "approved"

    run_cli(
        "draft",
        "--plan-file",
        str(approved_plan_path),
        "--output",
        str(draft_path),
    )

    draft = json.loads(draft_path.read_text(encoding="utf-8"))

    assert draft["plan_id"] == approved_plan["plan_id"]
    assert len(draft["stages"]) >= 1
    assert any(
        any(skill["id"] == "request-normalizer" and skill["resolved"] for skill in stage["candidate_skill_refs"])
        for stage in draft["stages"]
    )
    assert any(
        any(skill["id"] in {"fastqc", "star", "feature-counts"} for skill in stage["candidate_skill_refs"])
        for stage in draft["stages"]
    )


def test_review_compares_plans_and_recommends_one(tmp_path: Path) -> None:
    proposals_path = tmp_path / "plans.json"

    run_cli(
        "propose",
        "--request-text",
        "I have bulk RNA-seq FASTQ files for treated and control samples and want a differential expression result bundle.",
        "--goal",
        "Generate candidate plans for RNA-seq differential expression analysis.",
        "--output",
        str(proposals_path),
    )

    completed = run_cli("review", "--plans-file", str(proposals_path))
    review_payload = json.loads(completed.stdout)
    plan_ids = {plan["plan_id"] for plan in json.loads(proposals_path.read_text(encoding="utf-8"))["plans"]}

    assert review_payload["recommended_plan_id"] in plan_ids
    assert len(review_payload["comparison"]) >= 2
    assert all("strategy_type" in item for item in review_payload["comparison"])


def test_edit_updates_plan_and_resets_approval_on_structural_change(tmp_path: Path) -> None:
    edited_path = tmp_path / "edited-plan.json"
    approved_path = prepare_approved_plan(
        tmp_path,
        "I need an RNA-seq differential expression workflow for treated and control samples.",
        "Plan the analysis and prepare execution routing.",
    )

    run_cli(
        "edit",
        "--plan-file",
        str(approved_path),
        "--require-confirmation",
        "s2=false",
        "--add-risk",
        "Need extra QC review before quantification.",
        "--output",
        str(edited_path),
    )

    edited = json.loads(edited_path.read_text(encoding="utf-8"))
    stage_s2 = next(stage for stage in edited["stages"] if stage["stage_id"] == "s2")

    assert edited["approval_state"] == "draft"
    assert stage_s2["requires_user_confirmation"] is False
    assert "Need extra QC review before quantification." in edited["risks"]


def test_run_init_creates_pending_run_with_first_stage(tmp_path: Path) -> None:
    approved_path = prepare_approved_plan(
        tmp_path,
        "I need an RNA-seq differential expression workflow for treated and control samples.",
        "Plan the analysis and prepare execution routing.",
    )
    run_path = tmp_path / "run.json"

    run_cli("run-init", "--plan-file", str(approved_path), "--output", str(run_path))

    run_state = json.loads(run_path.read_text(encoding="utf-8"))

    assert run_state["status"] == "pending"
    assert run_state["current_stage"] == "s1"
    assert run_state["resume_from"] == "s1"
    assert run_state["stage_status"]["s1"] == "pending"
    assert run_state["stage_order"][0] == "s1"


def test_run_next_stage_advances_and_pauses_on_confirmation_stage(tmp_path: Path) -> None:
    approved_path = prepare_approved_plan(
        tmp_path,
        "I need an RNA-seq differential expression workflow for treated and control samples.",
        "Plan the analysis and prepare execution routing.",
    )
    run_path = tmp_path / "run.json"

    run_cli("run-init", "--plan-file", str(approved_path), "--output", str(run_path))
    run_cli("run-next-stage", "--run-file", str(run_path), "--output", str(run_path))

    run_after_s1 = json.loads(run_path.read_text(encoding="utf-8"))
    assert run_after_s1["stage_status"]["s1"] == "completed"
    assert run_after_s1["current_stage"] == "s2"
    assert run_after_s1["status"] == "pending"
    assert "s1" in run_after_s1["validation_results"]

    run_cli("run-next-stage", "--run-file", str(run_path), "--output", str(run_path))
    paused_run = json.loads(run_path.read_text(encoding="utf-8"))
    assert paused_run["status"] == "paused"
    assert paused_run["resume_from"] == "s2"

    run_cli("run-resume", "--run-file", str(run_path), "--output", str(run_path))
    resumed_run = json.loads(run_path.read_text(encoding="utf-8"))
    assert resumed_run["status"] == "pending"
    assert resumed_run["current_stage"] == "s2"


def test_run_pause_and_resume_update_run_state(tmp_path: Path) -> None:
    approved_path = prepare_approved_plan(
        tmp_path,
        "I need an RNA-seq differential expression workflow for treated and control samples.",
        "Plan the analysis and prepare execution routing.",
    )
    run_path = tmp_path / "run.json"

    run_cli("run-init", "--plan-file", str(approved_path), "--output", str(run_path))
    run_cli(
        "run-pause",
        "--run-file",
        str(run_path),
        "--reason",
        "Manual hold before execution.",
        "--output",
        str(run_path),
    )

    paused_run = json.loads(run_path.read_text(encoding="utf-8"))
    assert paused_run["status"] == "paused"
    assert paused_run["issues"][-1]["message"] == "Manual hold before execution."

    run_cli("run-resume", "--run-file", str(run_path), "--output", str(run_path))
    resumed_run = json.loads(run_path.read_text(encoding="utf-8"))
    assert resumed_run["status"] == "pending"
    assert resumed_run["resume_from"] == resumed_run["current_stage"]


def test_run_status_summarizes_paused_confirmation_stage(tmp_path: Path) -> None:
    approved_path = prepare_approved_plan(
        tmp_path,
        "I need an RNA-seq differential expression workflow for treated and control samples.",
        "Plan the analysis and prepare execution routing.",
    )
    run_path = tmp_path / "run.json"

    run_cli("run-init", "--plan-file", str(approved_path), "--output", str(run_path))
    run_cli("run-next-stage", "--run-file", str(run_path), "--output", str(run_path))
    run_cli("run-next-stage", "--run-file", str(run_path), "--output", str(run_path))

    completed = run_cli("run-status", "--run-file", str(run_path))
    summary = json.loads(completed.stdout)

    assert summary["status"] == "paused"
    assert summary["current_stage"] == "s2"
    assert summary["progress"]["completed"] == 1
    assert summary["progress"]["pending"] >= 1
    assert summary["latest_issue"]["message"].endswith("requires confirmation before execution.")
    assert summary["next_action"] == "Confirm and resume stage s2."


def test_run_review_flags_confirmation_blocker_and_future_unresolved_skill(tmp_path: Path) -> None:
    approved_path = prepare_approved_plan(
        tmp_path,
        "I need an RNA-seq differential expression workflow for treated and control samples.",
        "Plan the analysis and prepare execution routing.",
    )
    draft_path = tmp_path / "draft.json"
    run_path = tmp_path / "run.json"

    run_cli("draft", "--plan-file", str(approved_path), "--output", str(draft_path))
    run_cli("run-init", "--plan-file", str(approved_path), "--output", str(run_path))
    run_cli("run-next-stage", "--run-file", str(run_path), "--output", str(run_path))
    run_cli("run-next-stage", "--run-file", str(run_path), "--output", str(run_path))

    completed = run_cli(
        "run-review",
        "--run-file",
        str(run_path),
        "--draft-file",
        str(draft_path),
    )
    review = json.loads(completed.stdout)

    assert review["verdict"] == "awaiting_confirmation"
    assert review["current_stage_review"]["stage_id"] == "s2"
    assert review["current_stage_review"]["confirmation_required"] is True
    assert any(item["type"] == "confirmation_required" for item in review["blocking_issues"])
    assert any(item["type"] == "future_unresolved_skills" for item in review["future_issues"])
    future_issue = next(item for item in review["future_issues"] if item["type"] == "future_unresolved_skills")
    assert "pydeseq2" in future_issue["skills"]
    assert review["next_action"] == "Confirm and resume stage s2."

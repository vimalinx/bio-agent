from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
CLI_SCRIPT = ROOT / "scripts" / "bio_skill_system.py"


def run_cli(*args: str, env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(CLI_SCRIPT), *args],
        check=True,
        capture_output=True,
        text=True,
        env={**os.environ, **(env or {})},
    )


def prepare_approved_plan(
    tmp_path: Path,
    request_text: str,
    goal: str,
    *,
    env: dict[str, str] | None = None,
) -> Path:
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
        env=env,
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
        env=env,
    )

    return approved_path


def prepare_session(
    tmp_path: Path,
    request_text: str,
    goal: str,
    *,
    env: dict[str, str] | None = None,
) -> Path:
    session_dir = tmp_path / "session"
    run_cli(
        "session-start",
        "--session-dir",
        str(session_dir),
        "--request-text",
        request_text,
        "--goal",
        goal,
        env=env,
    )
    return session_dir


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


def test_benchmark_report_lists_grounded_benchmarks() -> None:
    payload = json.loads(run_cli("benchmark-report").stdout)

    benchmark_ids = {item["id"] for item in payload["benchmarks"]}
    assert payload["benchmark_count"] >= 4
    assert {
        "seqc2-bulk-rnaseq",
        "giab-precisionfda-small-variant",
        "openproblems-single-cell",
        "encode-atac-conformance",
    }.issubset(benchmark_ids)


def test_benchmark_evaluate_giab_task_passes() -> None:
    payload = json.loads(
        run_cli(
            "benchmark-evaluate",
            "--benchmark-id",
            "giab-precisionfda-small-variant",
            "--task-id",
            "giab-wes-bwa-gatk-hardfilter",
        ).stdout
    )

    assert payload["verdict"] == "pass"
    assert payload["workflow_match"] is True
    assert payload["strategy_match"] is True
    assert payload["recommended_workflow_id"] == "germline-short-variant-discovery"
    assert payload["outputs_coverage"]["complete"] is True
    assert payload["confirmation_coverage"]["complete"] is True
    assert payload["delivery_coverage"]["complete"] is True


def test_benchmark_run_giab_with_explicit_evidence_passes() -> None:
    payload = json.loads(
        run_cli(
            "benchmark-run",
            "--task-file",
            str(ROOT / "examples" / "benchmarks" / "giab-wes-bwa-gatk-hardfilter.task.json"),
            "--evidence-file",
            str(ROOT / "examples" / "benchmarks" / "giab-wes-bwa-gatk-hardfilter.evidence.json"),
        ).stdout
    )

    assert payload["verdict"] == "pass"
    assert payload["control_evaluation"]["verdict"] == "pass"
    assert payload["artifact_evaluation"]["delivery_artifact_coverage"]["complete"] is True
    assert payload["artifact_evaluation"]["truth_artifact_coverage"]["complete"] is True
    assert payload["artifact_evaluation"]["metric_key_coverage"]["complete"] is True
    assert payload["artifact_evaluation"]["metric_value_evaluation"]["complete"] is True
    assert payload["scorecard"]["passed_count"] == payload["scorecard"]["total_checks"]


def test_benchmark_run_giab_from_happy_summary_artifact_passes() -> None:
    payload = json.loads(
        run_cli(
            "benchmark-run",
            "--task-file",
            str(ROOT / "examples" / "benchmarks" / "giab-wes-bwa-gatk-hardfilter.task.json"),
            "--evidence-file",
            str(ROOT / "examples" / "benchmarks" / "giab-wes-bwa-gatk-hardfilter.happy.evidence.json"),
        ).stdout
    )

    assert payload["verdict"] == "pass"
    assert payload["artifact_evaluation"]["metric_value_evaluation"]["complete"] is True
    assert payload["evidence"]["metrics"]["precision"] == "0.992"
    assert payload["evidence"]["metrics"]["recall"] == "0.985"
    assert "F1" in payload["evidence"]["metrics"]


def test_benchmark_run_giab_infers_f1_when_missing() -> None:
    evidence_payload = {
        "delivery_items": [
            "analysis-ready BAM inventory",
            "recalibration metrics",
            "gVCF manifest",
            "joint VCF manifest",
            "filtered VCF manifest",
            "cohort QC summary",
        ],
        "truth_artifacts": [
            "benchmark VCF",
            "confident regions BED",
        ],
        "metrics": {
            "precision": "0.99",
            "recall": "0.98",
        },
    }
    evidence_path = ROOT / "examples" / "benchmarks" / "_tmp_giab_infer_f1.evidence.json"
    evidence_path.write_text(json.dumps(evidence_payload, indent=2), encoding="utf-8")
    try:
        payload = json.loads(
            run_cli(
                "benchmark-run",
                "--task-file",
                str(ROOT / "examples" / "benchmarks" / "giab-wes-bwa-gatk-hardfilter.task.json"),
                "--evidence-file",
                str(evidence_path),
            ).stdout
        )
    finally:
        evidence_path.unlink(missing_ok=True)

    assert payload["verdict"] == "pass"
    assert payload["artifact_evaluation"]["metric_value_evaluation"]["complete"] is True
    assert payload["artifact_evaluation"]["metric_value_evaluation"]["missing_metrics"] == []
    assert "F1" in payload["artifact_evaluation"]["metric_value_evaluation"]["parsed_metrics"]


def test_benchmark_run_giab_flags_inconsistent_f1() -> None:
    evidence_payload = {
        "delivery_items": [
            "analysis-ready BAM inventory",
            "recalibration metrics",
            "gVCF manifest",
            "joint VCF manifest",
            "filtered VCF manifest",
            "cohort QC summary",
        ],
        "truth_artifacts": [
            "benchmark VCF",
            "confident regions BED",
        ],
        "metrics": {
            "precision": "0.99",
            "recall": "0.98",
            "F1": "0.50",
        },
    }
    evidence_path = ROOT / "examples" / "benchmarks" / "_tmp_giab_bad_f1.evidence.json"
    evidence_path.write_text(json.dumps(evidence_payload, indent=2), encoding="utf-8")
    try:
        payload = json.loads(
            run_cli(
                "benchmark-run",
                "--task-file",
                str(ROOT / "examples" / "benchmarks" / "giab-wes-bwa-gatk-hardfilter.task.json"),
                "--evidence-file",
                str(evidence_path),
            ).stdout
        )
    finally:
        evidence_path.unlink(missing_ok=True)

    assert payload["verdict"] == "partial"
    assert payload["artifact_evaluation"]["metric_value_evaluation"]["complete"] is False
    assert payload["artifact_evaluation"]["metric_value_evaluation"]["consistency_checks"][0]["consistent"] is False
    assert "metric_values_complete" in payload["scorecard"]["failed_checks"]


def test_benchmark_run_giab_from_session_requires_truth_artifacts(tmp_path: Path) -> None:
    session_dir = tmp_path / "session"
    run_cli(
        "session-start",
        "--session-dir",
        str(session_dir),
        "--workflow-family",
        "germline-short-variant-discovery",
        "--strategy-profile",
        "bwa-gatk-hardfilter",
    )
    review = json.loads((session_dir / "review.json").read_text(encoding="utf-8"))
    run_cli(
        "session-approve",
        "--session-dir",
        str(session_dir),
        "--plan-id",
        review["recommended_plan_id"],
    )

    bam_inventory = session_dir / "analysis_ready_bams.tsv"
    recalibration = session_dir / "recalibration_metrics.tsv"
    gvcf_manifest = session_dir / "gvcf_bundle.tsv"
    joint_vcf = session_dir / "joint_vcf.tsv"
    filtered_vcf = session_dir / "filtered_vcf.tsv"
    qc_summary = session_dir / "qc_summary.txt"
    bam_inventory.write_text("sample\tbam\nS1\tbam/S1.bam\n", encoding="utf-8")
    recalibration.write_text("sample\tmetric\nS1\tok\n", encoding="utf-8")
    gvcf_manifest.write_text("sample\tgvcf\nS1\tgvcf/S1.g.vcf.gz\n", encoding="utf-8")
    joint_vcf.write_text("joint_vcf\ncohort/joint.vcf.gz\n", encoding="utf-8")
    filtered_vcf.write_text("filtered_vcf\ncohort/filtered.vcf.gz\n", encoding="utf-8")
    qc_summary.write_text("qc: pass\n", encoding="utf-8")

    run_cli(
        "session-next-stage",
        "--session-dir",
        str(session_dir),
        "--validation",
        "input_paths_exist=passed",
        "--validation",
        "reference_bundle_available=passed",
    )
    run_cli(
        "session-next-stage",
        "--session-dir",
        str(session_dir),
        "--confirm",
        "--validation",
        "analysis_ready_bams_exist=passed",
        "--validation",
        "recalibration_metrics_exist=passed",
        "--artifact",
        f"{bam_inventory}:tsv:Analysis-ready BAM inventory",
        "--artifact",
        f"{recalibration}:tsv:BQSR metrics summary",
    )
    run_cli(
        "session-next-stage",
        "--session-dir",
        str(session_dir),
        "--allow-missing-tools",
        "--validation",
        "gvcf_bundle_exists=passed",
        "--artifact",
        f"{gvcf_manifest}:tsv:Per-sample gVCF bundle manifest",
    )
    run_cli(
        "session-next-stage",
        "--session-dir",
        str(session_dir),
        "--allow-missing-tools",
        "--validation",
        "joint_vcf_exists=passed",
        "--artifact",
        f"{joint_vcf}:tsv:Cohort joint VCF manifest",
    )
    run_cli(
        "session-next-stage",
        "--session-dir",
        str(session_dir),
        "--validation",
        "filtered_vcf_exists=passed",
        "--validation",
        "summary_exists=passed",
        "--artifact",
        f"{filtered_vcf}:tsv:Filtered cohort VCF manifest",
        "--artifact",
        f"{qc_summary}:txt:Run summary and cohort QC summary",
    )

    payload = json.loads(
        run_cli(
            "benchmark-run",
            "--benchmark-id",
            "giab-precisionfda-small-variant",
            "--task-id",
            "giab-wes-bwa-gatk-hardfilter",
            "--session-dir",
            str(session_dir),
        ).stdout
    )

    assert payload["verdict"] == "partial"
    assert payload["control_evaluation"]["verdict"] == "pass"
    assert payload["artifact_evaluation"]["delivery_artifact_coverage"]["complete"] is True
    assert payload["artifact_evaluation"]["truth_artifact_coverage"]["complete"] is False
    assert "benchmark VCF" in payload["artifact_evaluation"]["truth_artifact_coverage"]["missing"]


def test_benchmark_suite_contract_reports_passes() -> None:
    payload = json.loads(run_cli("benchmark-suite", "--mode", "contract").stdout)

    assert payload["mode"] == "contract"
    assert payload["summary"]["task_count"] >= 4
    assert payload["summary"]["verdict_counts"]["pass"] >= 4
    assert payload["summary"]["workflow_match_rate"] == 1.0


def test_benchmark_suite_evidence_for_giab_passes_with_example_evidence() -> None:
    payload = json.loads(
        run_cli(
            "benchmark-suite",
            "--benchmark-id",
            "giab-precisionfda-small-variant",
            "--mode",
            "evidence",
            "--evidence-root",
            str(ROOT / "examples" / "benchmarks"),
        ).stdout
    )

    assert payload["mode"] == "evidence"
    assert payload["summary"]["task_count"] == 1
    assert payload["summary"]["verdict_counts"]["pass"] == 1
    assert payload["summary"]["truth_artifacts_complete_rate"] == 1.0
    assert payload["summary"]["metric_values_complete_rate"] == 1.0
    assert payload["results"][0]["task_id"] == "giab-wes-bwa-gatk-hardfilter"
    assert payload["results"][0]["verdict"] == "pass"

def test_benchmark_run_can_export_repro_bundle(tmp_path: Path) -> None:
    repro_dir = tmp_path / "repro"
    payload = json.loads(
        run_cli(
            "benchmark-run",
            "--task-file",
            str(ROOT / "examples" / "benchmarks" / "giab-wes-bwa-gatk-hardfilter.task.json"),
            "--evidence-file",
            str(ROOT / "examples" / "benchmarks" / "giab-wes-bwa-gatk-hardfilter.evidence.json"),
            "--export-repro-bundle",
            "--repro-dir",
            str(repro_dir),
        ).stdout
    )

    assert payload["repro_bundle"]["path"] == str(repro_dir.resolve())
    assert (repro_dir / "commands.sh").exists()
    assert (repro_dir / "environment.json").exists()
    assert (repro_dir / "artifacts.json").exists()
    assert (repro_dir / "scorecard.json").exists()


def test_session_export_skill_requires_eligible_session_or_force(tmp_path: Path) -> None:
    session_dir = tmp_path / "session"
    skill_root = tmp_path / "skills"
    run_cli(
        "session-start",
        "--session-dir",
        str(session_dir),
        "--workflow-family",
        "germline-short-variant-discovery",
        "--strategy-profile",
        "bwa-gatk-hardfilter",
    )
    review = json.loads((session_dir / "review.json").read_text(encoding="utf-8"))
    run_cli(
        "session-approve",
        "--session-dir",
        str(session_dir),
        "--plan-id",
        review["recommended_plan_id"],
    )

    run_cli("session-next-stage", "--session-dir", str(session_dir), "--validation", "input_paths_exist=passed", "--validation", "reference_bundle_available=passed")
    run_cli("session-next-stage", "--session-dir", str(session_dir), "--confirm", "--validation", "analysis_ready_bams_exist=passed", "--validation", "recalibration_metrics_exist=passed")
    run_cli("session-next-stage", "--session-dir", str(session_dir), "--allow-missing-tools", "--validation", "gvcf_bundle_exists=passed")
    run_cli("session-next-stage", "--session-dir", str(session_dir), "--allow-missing-tools", "--validation", "joint_vcf_exists=passed")
    run_cli("session-next-stage", "--session-dir", str(session_dir), "--validation", "filtered_vcf_exists=passed", "--validation", "summary_exists=passed")

    candidate = json.loads(run_cli("session-skill-candidate", "--session-dir", str(session_dir)).stdout)
    assert candidate["eligible"] is False
    assert any("run verdict" in reason or "unavailable runtime tools" in reason for reason in candidate["reasons"])

    failed = subprocess.run(
        [sys.executable, str(CLI_SCRIPT), "session-export-skill", "--session-dir", str(session_dir), "--skill-root", str(skill_root)],
        capture_output=True,
        text=True,
    )
    assert failed.returncode != 0
    assert "not eligible for automatic skill crystallization" in (failed.stderr + failed.stdout)

    payload = json.loads(
        run_cli(
            "session-export-skill",
            "--session-dir",
            str(session_dir),
            "--skill-root",
            str(skill_root),
            "--force",
        ).stdout
    )

    skill_dir = Path(payload["skill_dir"])
    skill_md = skill_dir / "SKILL.md"
    summary_json = skill_dir / "references" / "session-summary.json"
    environment_json = skill_dir / "references" / "environment.json"
    assert payload["eligibility"]["eligible"] is False
    assert skill_md.exists()
    assert summary_json.exists()
    assert environment_json.exists()
    skill_text = skill_md.read_text(encoding="utf-8")
    assert "Generated workflow skill" in skill_text
    assert "Benchmark Fit" in skill_text
    assert "Analysis Flow" in skill_text

def test_propose_routes_scrnaseq_request_to_scrnaseq_workflow(tmp_path: Path) -> None:
    output_path = tmp_path / "scrnaseq-plans.json"

    run_cli(
        "propose",
        "--request-text",
        "I have 10x single-cell RNA-seq FASTQ files and need a clustering-ready count matrix.",
        "--goal",
        "Prepare a single-cell preprocessing workflow.",
        "--output",
        str(output_path),
    )

    payload = json.loads(output_path.read_text(encoding="utf-8"))
    assert any(plan["source_workflow_id"] == "scrnaseq-preprocessing" for plan in payload["plans"])


def test_propose_routes_atacseq_request_to_atac_workflow(tmp_path: Path) -> None:
    output_path = tmp_path / "atacseq-plans.json"

    run_cli(
        "propose",
        "--request-text",
        "I need an ATAC-seq workflow from FASTQ to peaks and differential accessibility.",
        "--goal",
        "Generate a chromatin accessibility analysis plan.",
        "--output",
        str(output_path),
    )

    payload = json.loads(output_path.read_text(encoding="utf-8"))
    assert any(plan["source_workflow_id"] == "atacseq-differential-accessibility" for plan in payload["plans"])


def test_propose_routes_germline_request_to_variant_workflow(tmp_path: Path) -> None:
    output_path = tmp_path / "germline-plans.json"

    run_cli(
        "propose",
        "--request-text",
        "I have paired-end WES FASTQ files and need germline SNP/Indel discovery with a filtered cohort VCF.",
        "--goal",
        "Generate a germline short variant discovery workflow.",
        "--output",
        str(output_path),
    )

    payload = json.loads(output_path.read_text(encoding="utf-8"))
    assert any(plan["source_workflow_id"] == "germline-short-variant-discovery" for plan in payload["plans"])




def test_propose_applies_strategy_profile_overrides(tmp_path: Path) -> None:
    output_path = tmp_path / "strategy-plans.json"

    run_cli(
        "propose",
        "--request-text",
        "I have bulk RNA-seq FASTQ files and need differential expression.",
        "--goal",
        "Generate an RNA-seq plan.",
        "--tag",
        "strategy-star-featurecounts",
        "--output",
        str(output_path),
    )

    payload = json.loads(output_path.read_text(encoding="utf-8"))
    plan = payload["plans"][0]
    assert plan["selected_strategy_profile"] == "star-featurecounts"
    assert plan["selected_strategy_label"] == "STAR + featureCounts"
    assert "STAR + featureCounts" in plan["summary"]
    stage_s2 = next(stage for stage in plan["stages"] if stage["stage_id"] == "s2")
    stage_s3 = next(stage for stage in plan["stages"] if stage["stage_id"] == "s3")
    assert "star" in stage_s2["candidate_skills"]
    assert stage_s3["candidate_skills"] == ["feature-counts", "stage-reviewer"]

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
    stage_s2 = next(stage for stage in draft["stages"] if stage["stage_id"] == "s2")
    assert stage_s2["execution_bridge"]["contract_defined"] is True
    assert stage_s2["execution_bridge"]["bridge_id"] in {"generic-rnaseq-alignment-qc", "star-alignment-qc"}


def test_germline_draft_tracks_missing_local_gatk_tools_without_marking_them_unresolved(tmp_path: Path) -> None:
    draft_path = tmp_path / "execution-draft.json"
    approved_plan_path = prepare_approved_plan(
        tmp_path,
        "I have paired-end WES FASTQ files and need germline SNP/Indel discovery with a filtered cohort VCF.",
        "Generate a germline short variant discovery workflow.",
        env={"PATH": ""},
    )

    run_cli(
        "draft",
        "--plan-file",
        str(approved_plan_path),
        "--output",
        str(draft_path),
        env={"PATH": ""},
    )

    draft = json.loads(draft_path.read_text(encoding="utf-8"))
    stage_s3 = next(stage for stage in draft["stages"] if stage["stage_id"] == "s3")
    haplotypecaller = next(skill for skill in stage_s3["candidate_skill_refs"] if skill["id"] == "gatk-haplotypecaller")

    assert haplotypecaller["resolved"] is True
    assert haplotypecaller["runtime_kind"] == "tool"
    assert haplotypecaller["runtime_status"] == "missing-local-tool"
    assert "gatk-haplotypecaller" in draft["unavailable_runtime_skill_ids"]
    assert "gatk-haplotypecaller" not in draft["unresolved_skill_ids"]


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


def test_session_start_writes_request_plans_review_and_manifest(tmp_path: Path) -> None:
    session_dir = prepare_session(
        tmp_path,
        "I have bulk RNA-seq FASTQ files for treated and control samples and want a differential expression result bundle.",
        "Generate candidate plans for RNA-seq differential expression analysis.",
    )

    manifest = json.loads((session_dir / "session.json").read_text(encoding="utf-8"))
    review = json.loads((session_dir / "review.json").read_text(encoding="utf-8"))
    history = json.loads((session_dir / "history.json").read_text(encoding="utf-8"))

    assert (session_dir / "request.json").exists()
    assert (session_dir / "plans.json").exists()
    assert (session_dir / "review.json").exists()
    assert (session_dir / "history.json").exists()
    assert manifest["status"] == "awaiting_plan_selection"
    assert manifest["recommended_plan_id"] == review["recommended_plan_id"]
    assert "plans" in manifest["files"]
    assert "review" in manifest["files"]
    assert "session" in manifest["files"]
    assert "history" in manifest["files"]
    assert manifest["history_event_count"] == 1
    assert manifest["latest_event_type"] == "session_started"
    assert history["events"][0]["type"] == "session_started"


def test_session_approve_creates_run_bundle_from_recommended_plan(tmp_path: Path) -> None:
    session_dir = prepare_session(
        tmp_path,
        "I need an RNA-seq differential expression workflow for treated and control samples.",
        "Plan the analysis and prepare execution routing.",
    )
    review = json.loads((session_dir / "review.json").read_text(encoding="utf-8"))

    run_cli(
        "session-approve",
        "--session-dir",
        str(session_dir),
        "--plan-id",
        review["recommended_plan_id"],
    )

    manifest = json.loads((session_dir / "session.json").read_text(encoding="utf-8"))
    run_status = json.loads((session_dir / "run-status.json").read_text(encoding="utf-8"))
    run_review = json.loads((session_dir / "run-review.json").read_text(encoding="utf-8"))
    history = json.loads((session_dir / "history.json").read_text(encoding="utf-8"))

    assert (session_dir / "approved-plan.json").exists()
    assert (session_dir / "execution-draft.json").exists()
    assert (session_dir / "run.json").exists()
    assert manifest["status"] == "run_active"
    assert manifest["approved_plan_id"] == review["recommended_plan_id"]
    assert run_status["current_stage"] == "s1"
    assert run_review["verdict"] == "ready_to_continue"
    assert run_review["current_stage_review"]["execution_bridge"]["contract_defined"] is True
    assert manifest["history_event_count"] == 2
    assert manifest["latest_event_type"] == "plan_approved"
    assert history["events"][-1]["type"] == "plan_approved"
    assert history["events"][-1]["data"]["plan_diff"]["change_count"] == 0


def test_session_render_plan_exports_editable_markdown_for_candidate_plan(tmp_path: Path) -> None:
    session_dir = prepare_session(
        tmp_path,
        "I need an RNA-seq differential expression workflow for treated and control samples.",
        "Plan the analysis and prepare execution routing.",
    )
    markdown_path = tmp_path / "editable-plan.md"

    run_cli(
        "session-render-plan",
        "--session-dir",
        str(session_dir),
        "--plan-id",
        "plan_rnaseq-differential-expression_conservative",
        "--output",
        str(markdown_path),
    )

    text = markdown_path.read_text(encoding="utf-8")

    assert text.startswith("# Bio Agent Plan Editor")
    assert "## Editable Plan YAML" in text
    assert "plan_id: plan_rnaseq-differential-expression_conservative" in text
    assert "request_id:" in text


def test_session_history_command_returns_timeline(tmp_path: Path) -> None:
    session_dir = prepare_session(
        tmp_path,
        "I need an RNA-seq differential expression workflow for treated and control samples.",
        "Plan the analysis and prepare execution routing.",
    )

    payload = json.loads(run_cli("session-history", "--session-dir", str(session_dir)).stdout)

    assert payload["session_id"] == session_dir.name
    assert payload["events"][0]["type"] == "session_started"


def test_session_export_console_emits_web_bundle_shape(tmp_path: Path) -> None:
    session_dir = tmp_path / "session"
    run_cli(
        "session-start",
        "--session-dir",
        str(session_dir),
        "--request-text",
        "I need an RNA-seq differential expression workflow for treated and control samples.",
        "--goal",
        "Plan the analysis and prepare execution routing.",
        "--tag",
        "strategy-star-featurecounts",
    )
    review = json.loads((session_dir / "review.json").read_text(encoding="utf-8"))
    export_path = tmp_path / "console-bundle.json"

    run_cli(
        "session-approve",
        "--session-dir",
        str(session_dir),
        "--plan-id",
        review["recommended_plan_id"],
        "--reason",
        "Approved for console export coverage.",
    )
    run_cli(
        "session-export-console",
        "--session-dir",
        str(session_dir),
        "--scenario-name",
        "Console export smoke",
        "--output",
        str(export_path),
    )

    payload = json.loads(export_path.read_text(encoding="utf-8"))

    assert payload["scenario"]["name"] == "Console export smoke"
    assert payload["session"]["approved_plan_id"] == review["recommended_plan_id"]
    assert payload["review"]["recommended_plan_id"] == review["recommended_plan_id"]
    assert isinstance(payload["candidate_plans"], list)
    assert payload["analysis_flow"]["workflow_id"] == "rnaseq-differential-expression"
    assert payload["analysis_flow"]["stage_flows"][0]["stage_id"] == "s1"
    assert payload["execution_bridge_summary"]["unmapped_stage_ids"] == []
    assert isinstance(payload["benchmark_matches"], list)
    assert payload["benchmark_matches"][0]["benchmark_id"] == "seqc2-bulk-rnaseq"
    assert payload["candidate_plans"][0]["selected_strategy_profile"] == "star-featurecounts"
    assert payload["candidate_plans"][0]["selected_strategy_label"] == "STAR + featureCounts"
    assert payload["history"]["events"][-1]["type"] == "plan_approved"
    assert payload["run_status"]["current_stage"] == "s1"
    assert payload["run_review"]["verdict"] == "ready_to_continue"


def test_session_approve_accepts_user_edited_plan_file(tmp_path: Path) -> None:
    session_dir = prepare_session(
        tmp_path,
        "I need an RNA-seq differential expression workflow for treated and control samples.",
        "Plan the analysis and prepare execution routing.",
    )
    proposals = json.loads((session_dir / "plans.json").read_text(encoding="utf-8"))
    edited_plan_path = tmp_path / "edited-plan.json"

    edited_plan = dict(proposals["plans"][1])
    edited_plan["summary"] = "User-edited efficient plan for fast iteration."
    edited_plan_path.write_text(json.dumps(edited_plan, indent=2), encoding="utf-8")

    run_cli(
        "session-approve",
        "--session-dir",
        str(session_dir),
        "--plan-file",
        str(edited_plan_path),
    )

    approved_plan = json.loads((session_dir / "approved-plan.json").read_text(encoding="utf-8"))
    manifest = json.loads((session_dir / "session.json").read_text(encoding="utf-8"))

    assert approved_plan["summary"] == "User-edited efficient plan for fast iteration."
    assert approved_plan["approval_state"] == "approved"
    assert manifest["approved_plan_id"] == approved_plan["plan_id"]


def test_session_approve_accepts_user_edited_markdown_plan_file(tmp_path: Path) -> None:
    session_dir = prepare_session(
        tmp_path,
        "I need an RNA-seq differential expression workflow for treated and control samples.",
        "Plan the analysis and prepare execution routing.",
    )
    markdown_path = tmp_path / "editable-plan.md"

    run_cli(
        "session-render-plan",
        "--session-dir",
        str(session_dir),
        "--plan-id",
        "plan_rnaseq-differential-expression_conservative",
        "--output",
        str(markdown_path),
    )

    edited_text = markdown_path.read_text(encoding="utf-8")
    match = re.search(r"```yaml\n(.*?)```", edited_text, flags=re.DOTALL)
    assert match is not None
    plan_payload = yaml.safe_load(match.group(1))
    plan_payload["summary"] = "Markdown-edited plan with relaxed alignment checkpoint handling."
    stage_s2_patch = next(stage for stage in plan_payload["stages"] if stage["stage_id"] == "s2")
    stage_s2_patch["requires_user_confirmation"] = False
    rendered_yaml = yaml.safe_dump(plan_payload, sort_keys=False, allow_unicode=True).strip()
    edited_text = edited_text[: match.start(1)] + rendered_yaml + "\n" + edited_text[match.end(1) :]
    markdown_path.write_text(edited_text, encoding="utf-8")

    run_cli(
        "session-approve",
        "--session-dir",
        str(session_dir),
        "--plan-file",
        str(markdown_path),
        "--reason",
        "User removed the manual alignment checkpoint after review.",
    )

    approved_plan = json.loads((session_dir / "approved-plan.json").read_text(encoding="utf-8"))
    session_payload = json.loads(run_cli("session-status", "--session-dir", str(session_dir)).stdout)
    history = session_payload["history"]
    stage_s2 = next(stage for stage in approved_plan["stages"] if stage["stage_id"] == "s2")
    approval_event = history["events"][-1]

    assert approved_plan["summary"] == "Markdown-edited plan with relaxed alignment checkpoint handling."
    assert stage_s2["requires_user_confirmation"] is False
    assert approved_plan["approval_state"] == "approved"
    assert session_payload["session"]["latest_approval_reason"] == "User removed the manual alignment checkpoint after review."
    assert session_payload["session"]["latest_plan_change_count"] >= 2
    assert approval_event["type"] == "plan_approved"
    assert approval_event["data"]["reason"] == "User removed the manual alignment checkpoint after review."
    assert approval_event["data"]["plan_diff"]["changed"] is True
    assert any(
        item["field"] == "summary" for item in approval_event["data"]["plan_diff"]["changed_fields"]
    )
    stage_change = next(
        item for item in approval_event["data"]["plan_diff"]["stage_changes"] if item["stage_id"] == "s2"
    )
    assert stage_change["requires_user_confirmation"]["before"] is True
    assert stage_change["requires_user_confirmation"]["after"] is False


def test_session_next_stage_refreshes_run_status_and_confirmation_pause(tmp_path: Path) -> None:
    session_dir = prepare_session(
        tmp_path,
        "I need an RNA-seq differential expression workflow for treated and control samples.",
        "Plan the analysis and prepare execution routing.",
    )
    review = json.loads((session_dir / "review.json").read_text(encoding="utf-8"))

    run_cli(
        "session-approve",
        "--session-dir",
        str(session_dir),
        "--plan-id",
        review["recommended_plan_id"],
    )
    run_cli("session-next-stage", "--session-dir", str(session_dir))

    run_status_after_s1 = json.loads((session_dir / "run-status.json").read_text(encoding="utf-8"))
    assert run_status_after_s1["current_stage"] == "s2"
    assert run_status_after_s1["status"] == "pending"

    run_cli("session-next-stage", "--session-dir", str(session_dir))

    manifest = json.loads((session_dir / "session.json").read_text(encoding="utf-8"))
    run_status = json.loads((session_dir / "run-status.json").read_text(encoding="utf-8"))
    run_review = json.loads((session_dir / "run-review.json").read_text(encoding="utf-8"))
    history = json.loads((session_dir / "history.json").read_text(encoding="utf-8"))

    assert manifest["status"] == "awaiting_confirmation"
    assert run_status["status"] == "paused"
    assert run_review["verdict"] == "awaiting_confirmation"
    assert run_review["next_action"] == "Confirm and resume stage s2."
    assert history["events"][-1]["type"] == "run_advanced"
    assert history["events"][-1]["data"]["status"] == "paused"


def test_session_next_stage_blocks_when_current_stage_tool_is_missing(tmp_path: Path) -> None:
    session_dir = tmp_path / "germline-session"

    run_cli(
        "session-start",
        "--session-dir",
        str(session_dir),
        "--workflow-family",
        "germline-short-variant-discovery",
        "--strategy-profile",
        "bwa-gatk-hardfilter",
        env={"PATH": ""},
    )
    review = json.loads((session_dir / "review.json").read_text(encoding="utf-8"))
    run_cli(
        "session-approve",
        "--session-dir",
        str(session_dir),
        "--plan-id",
        review["recommended_plan_id"],
        env={"PATH": ""},
    )

    run_cli("session-next-stage", "--session-dir", str(session_dir), env={"PATH": ""})
    run_cli("session-next-stage", "--session-dir", str(session_dir), "--confirm", env={"PATH": ""})
    run_cli("session-next-stage", "--session-dir", str(session_dir), env={"PATH": ""})

    status = json.loads(run_cli("session-status", "--session-dir", str(session_dir), env={"PATH": ""}).stdout)

    assert status["session"]["status"] == "paused"
    assert status["run_status"]["current_stage"] == "s3"
    assert status["run_status"]["status"] == "paused"
    assert status["run_review"]["verdict"] == "blocked"
    blocking_issue = next(item for item in status["run_review"]["blocking_issues"] if item["type"] == "missing_local_tools")
    assert "gatk-haplotypecaller" in blocking_issue["skills"]
    assert status["history"]["events"][-1]["type"] == "run_blocked"


def test_completed_session_with_missing_local_tools_is_not_ready_to_deliver(tmp_path: Path) -> None:
    session_dir = tmp_path / "germline-session"
    env = {"PATH": ""}

    run_cli(
        "session-start",
        "--session-dir",
        str(session_dir),
        "--workflow-family",
        "germline-short-variant-discovery",
        "--strategy-profile",
        "bwa-gatk-hardfilter",
        env=env,
    )
    review = json.loads((session_dir / "review.json").read_text(encoding="utf-8"))
    run_cli(
        "session-approve",
        "--session-dir",
        str(session_dir),
        "--plan-id",
        review["recommended_plan_id"],
        env=env,
    )

    run_cli(
        "session-next-stage",
        "--session-dir",
        str(session_dir),
        "--validation",
        "input_paths_exist=passed",
        "--validation",
        "reference_bundle_available=passed",
        env=env,
    )
    run_cli(
        "session-next-stage",
        "--session-dir",
        str(session_dir),
        "--confirm",
        "--validation",
        "analysis_ready_bams_exist=passed",
        "--validation",
        "recalibration_metrics_exist=passed",
        env=env,
    )

    gvcf_bundle = session_dir / "gvcf_bundle.tsv"
    joint_vcf = session_dir / "joint_vcf.tsv"
    filtered_vcf = session_dir / "filtered_vcf.tsv"
    summary_txt = session_dir / "summary.txt"
    gvcf_bundle.write_text("sample_id\tgvcf\nS1\tgvcf/S1.g.vcf.gz\n", encoding="utf-8")
    joint_vcf.write_text("joint_vcf\ncohort/joint.vcf.gz\n", encoding="utf-8")
    filtered_vcf.write_text("filtered_vcf\tvariant_count\ncohort/joint.filtered.vcf.gz\t10\n", encoding="utf-8")
    summary_txt.write_text("callable_sites_fraction: 0.95\n", encoding="utf-8")

    run_cli(
        "session-next-stage",
        "--session-dir",
        str(session_dir),
        "--allow-missing-tools",
        "--validation",
        "gvcf_bundle_exists=passed",
        "--artifact",
        f"{gvcf_bundle}:tsv:gVCF bundle",
        env=env,
    )
    run_cli(
        "session-next-stage",
        "--session-dir",
        str(session_dir),
        "--allow-missing-tools",
        "--validation",
        "joint_vcf_exists=passed",
        "--artifact",
        f"{joint_vcf}:tsv:Joint VCF manifest",
        env=env,
    )
    run_cli(
        "session-next-stage",
        "--session-dir",
        str(session_dir),
        "--validation",
        "filtered_vcf_exists=passed",
        "--validation",
        "summary_exists=passed",
        "--artifact",
        f"{filtered_vcf}:tsv:Filtered VCF manifest",
        "--artifact",
        f"{summary_txt}:txt:Summary notes",
        env=env,
    )

    status = json.loads(run_cli("session-status", "--session-dir", str(session_dir), env=env).stdout)

    assert status["session"]["status"] == "completed"
    assert status["run_review"]["verdict"] == "completed_with_environment_gaps"
    delivery_issue = next(
        item for item in status["run_review"]["delivery_issues"] if item["type"] == "completed_stage_missing_local_tools"
    )
    assert set(delivery_issue["skills"]) == {"gatk-haplotypecaller", "gatk-genotypegvcfs"}


def test_session_start_accepts_workflow_family_and_strategy_profile(tmp_path: Path) -> None:
    session_dir = tmp_path / "family-session"

    run_cli(
        "session-start",
        "--session-dir",
        str(session_dir),
        "--workflow-family",
        "rnaseq-differential-expression",
        "--strategy-profile",
        "salmon-tximport",
    )

    request = json.loads((session_dir / "request.json").read_text(encoding="utf-8"))
    plans = json.loads((session_dir / "plans.json").read_text(encoding="utf-8"))

    assert "strategy-salmon-tximport" in request["request_tags"]
    assert plans["plans"][0]["selected_strategy_profile"] == "salmon-tximport"
    assert plans["plans"][0]["selected_strategy_label"] == "Salmon + tximport"


def test_session_start_rejects_missing_request_text_without_family(tmp_path: Path) -> None:
    session_dir = tmp_path / "invalid-session"

    completed = subprocess.run(
        [sys.executable, str(CLI_SCRIPT), "session-start", "--session-dir", str(session_dir)],
        capture_output=True,
        text=True,
    )

    assert completed.returncode != 0
    assert "request_text" in (completed.stderr + completed.stdout)

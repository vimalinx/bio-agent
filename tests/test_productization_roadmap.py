from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest


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


@pytest.mark.smoke
def test_hero_run_rnaseq_creates_canonical_session_truth_and_repro_bundle(tmp_path: Path) -> None:
    session_dir = tmp_path / "hero-rnaseq"
    payload = json.loads(
        run_cli(
            "hero-run",
            "--session-dir",
            str(session_dir),
            "--workflow-family",
            "rnaseq-differential-expression",
        ).stdout
    )

    assert payload["workflow_family"] == "rnaseq-differential-expression"
    assert payload["session"]["approved_plan_id"] == payload["approved_plan_id"]
    assert payload["run_status"]["status"] == "pending"
    assert payload["run_review"]["verdict"] == "ready_to_continue"

    for name in ("run.json", "run-status.json", "run-review.json", "approved-plan.json"):
        assert (session_dir / name).exists()

    repro_dir = session_dir / "repro"
    for name in ("commands.sh", "environment.json", "checksums.sha256", "provenance.json", "delivery-bundle.json"):
        assert (repro_dir / name).exists()

    delivery_bundle = json.loads((repro_dir / "delivery-bundle.json").read_text(encoding="utf-8"))
    assert delivery_bundle["workflow_family"] == "rnaseq-differential-expression"
    assert delivery_bundle["run_status"] == "pending"
    assert delivery_bundle["canonical_run_artifacts"]["run"].endswith("/run.json")
    assert delivery_bundle["items"]


@pytest.mark.smoke
def test_hero_run_germline_repro_bundle_records_canonical_artifacts(tmp_path: Path) -> None:
    session_dir = tmp_path / "hero-germline"
    payload = json.loads(
        run_cli(
            "hero-run",
            "--session-dir",
            str(session_dir),
            "--workflow-family",
            "germline-short-variant-discovery",
            "--strategy-profile",
            "bwa-gatk-hardfilter",
        ).stdout
    )

    approved_plan = json.loads((session_dir / "approved-plan.json").read_text(encoding="utf-8"))
    provenance = json.loads((session_dir / "repro" / "provenance.json").read_text(encoding="utf-8"))
    checksums = (session_dir / "repro" / "checksums.sha256").read_text(encoding="utf-8")
    commands = (session_dir / "repro" / "commands.sh").read_text(encoding="utf-8")

    assert approved_plan["selected_strategy_profile"] == "bwa-gatk-hardfilter"
    assert payload["repro_bundle"]["canonical_artifacts"]["run"] == str((session_dir / "run.json").resolve())
    assert provenance["workflow_family"] == "germline-short-variant-discovery"
    assert provenance["strategy_profile"] == "bwa-gatk-hardfilter"
    assert provenance["canonical_run_artifacts"]["run_review"] == str((session_dir / "run-review.json").resolve())
    assert "delivery-bundle.json" in checksums
    assert "provenance.json" in checksums
    assert "hero-run" in commands
    assert "session-export-repro-bundle" in commands


def test_hero_run_keeps_skill_crystallization_gated_until_completed(tmp_path: Path) -> None:
    session_dir = tmp_path / "hero-gated"
    run_cli(
        "hero-run",
        "--session-dir",
        str(session_dir),
        "--workflow-family",
        "rnaseq-differential-expression",
    )

    candidate = json.loads(
        run_cli(
            "session-skill-candidate",
            "--session-dir",
            str(session_dir),
        ).stdout
    )

    assert candidate["eligible"] is False
    assert "session run is not completed" in candidate["reasons"]


def test_ci_workflow_separates_stable_and_smoke_lanes() -> None:
    workflow_path = ROOT / ".github" / "workflows" / "ci.yml"
    workflow_text = workflow_path.read_text(encoding="utf-8")

    assert "stable:" in workflow_text
    assert "smoke:" in workflow_text
    assert "scripts/ci/run_stable_tests.sh" in workflow_text
    assert "scripts/ci/run_smoke_tests.sh" in workflow_text

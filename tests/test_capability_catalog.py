from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "skills" / "collect_local_bio_skills.py"


def test_capability_catalog_is_derived_from_registry_and_runtime_metadata() -> None:
    completed = subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "--format",
            "capability-json",
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    payload = json.loads(completed.stdout)

    by_group = payload["summary"]["group_counts"]
    assert by_group["first_party_executable"] >= 2
    assert by_group["bridge_executable"] >= 1
    assert by_group["reference_only"] >= 1

    capability_ids = {item["id"] for item in payload["capabilities"]}
    assert "rnaseq-differential-expression" in capability_ids
    assert "germline-short-variant-discovery" in capability_ids

    hero_entry = next(item for item in payload["capabilities"] if item["id"] == "rnaseq-differential-expression")
    assert hero_entry["execution_tier"] == "first_party_executable"
    assert hero_entry["runtime_mode"] == "session-hero-runner"
    assert hero_entry["verification_level"] == "benchmark_contract"
    assert hero_entry["reproducibility_level"] == "automatic_session_bundle"
    assert hero_entry["source_kind"] == "registry-grounded-workflow"
    assert hero_entry["provenance"]["analysis_flow"] == "registry/analysis_flows.yaml"

    reference_entry = next(item for item in payload["capabilities"] if item["capability_group"] == "reference_only")
    assert reference_entry["runnable"] is False
    assert reference_entry["runtime_mode"] == "planning-reference"

    bridge_entry = next(item for item in payload["capabilities"] if item["capability_group"] == "bridge_executable")
    assert bridge_entry["execution_tier"] == "bridge_executable"
    assert bridge_entry["source_kind"] == "skill-doc"
    assert bridge_entry["provenance"]["skill_path"].endswith("SKILL.md")

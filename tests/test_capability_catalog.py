from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXPORT_SCRIPT = ROOT / "scripts" / "skills" / "export_capability_catalog.py"
DOCS_JSON = ROOT / "docs" / "system" / "data" / "capability-catalog.json"


def run_export() -> dict:
    completed = subprocess.run(
        [sys.executable, str(EXPORT_SCRIPT)],
        check=True,
        capture_output=True,
        text=True,
    )
    return json.loads(completed.stdout)


def test_capability_catalog_export_matches_committed_docs_payload() -> None:
    generated = run_export()
    committed = json.loads(DOCS_JSON.read_text(encoding="utf-8"))

    assert generated == committed


def test_capability_catalog_contains_required_execution_tiers_and_examples() -> None:
    payload = run_export()
    capabilities = payload["capabilities"]
    by_id = {item["id"]: item for item in capabilities}
    tiers = {item["execution_tier"] for item in capabilities}

    assert {"first_party_executable", "bridge_executable", "reference_only"} <= tiers
    assert by_id["request-normalizer"]["execution_tier"] == "first_party_executable"
    assert by_id["request-normalizer"]["runtime_mode"] == "local-agent-control-plane"
    assert by_id["rnaseq-differential-expression"]["execution_tier"] == "bridge_executable"
    assert by_id["rnaseq-differential-expression"]["verification_level"] == "benchmark_contract"
    assert by_id["rnaseq-differential-expression"]["hero_lane"] is True
    reference_entry = by_id["reference:rnaseq-differential-expression:nf-core/rnaseq"]
    assert reference_entry["execution_tier"] == "reference_only"
    assert reference_entry["runnable"] is False


def test_capability_catalog_workflow_entries_expose_required_metadata_fields() -> None:
    payload = run_export()
    workflow_entries = [
        item
        for item in payload["capabilities"]
        if item["capability_kind"] == "workflow_family"
    ]

    assert workflow_entries
    for entry in workflow_entries:
        assert entry["execution_tier"]
        assert entry["runtime_mode"]
        assert entry["verification_level"]
        assert entry["reproducibility_level"]
        assert entry["source_kind"]
        assert entry["delivery_bundle_items"]

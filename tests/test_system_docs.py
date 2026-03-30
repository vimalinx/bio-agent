from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_console_page_exists_and_references_demo_bundle() -> None:
    console_page = ROOT / "docs" / "system" / "bio-skill-console.html"
    html = console_page.read_text(encoding="utf-8")

    assert "Bio Skill System Control Console" in html
    assert 'fetch("data/bio-skill-console-demo.json")' in html
    assert "run-status" in html
    assert "run-review" in html


def test_console_demo_bundle_contains_expected_runtime_shape() -> None:
    demo_path = ROOT / "docs" / "system" / "data" / "bio-skill-console-demo.json"
    payload = json.loads(demo_path.read_text(encoding="utf-8"))

    assert payload["review"]["recommended_plan_id"].endswith("_conservative")
    assert payload["run_status"]["status"] == "paused"
    assert payload["run_status"]["current_stage"] == "s2"
    assert payload["run_status"]["next_action"] == "Confirm and resume stage s2."
    assert payload["run_review"]["verdict"] == "awaiting_confirmation"
    assert any(item["type"] == "future_unresolved_skills" for item in payload["run_review"]["future_issues"])
    assert "pydeseq2" in payload["execution_draft"]["unresolved_skill_ids"]


def test_architecture_page_links_to_console() -> None:
    architecture_page = ROOT / "docs" / "system" / "bio-skill-system.html"
    html = architecture_page.read_text(encoding="utf-8")

    assert "bio-skill-console.html" in html

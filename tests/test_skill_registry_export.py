from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXPORT_SCRIPT = ROOT / "scripts" / "skills" / "export_skill_registry.py"


def write_skill(skill_dir: Path, name: str, description: str) -> None:
    skill_dir.mkdir(parents=True, exist_ok=True)
    (skill_dir / "SKILL.md").write_text(
        "\n".join(
            [
                "---",
                f"name: {name}",
                f"description: {description}",
                "user-invocable: true",
                "---",
                "",
                f"# {name}",
                "",
                "Body",
                "",
            ]
        ),
        encoding="utf-8",
    )


def run_export(skill_root: Path) -> dict:
    completed = subprocess.run(
        [sys.executable, str(EXPORT_SCRIPT), "--skill-root", str(skill_root), "--format", "json"],
        check=True,
        capture_output=True,
        text=True,
    )
    return json.loads(completed.stdout)


def test_export_skill_registry_discovers_layered_skills_recursively(tmp_path: Path) -> None:
    skill_root = tmp_path / ".claude" / "skills"
    write_skill(
        skill_root / "orchestrator" / "request-normalizer",
        "request-normalizer",
        "Use when normalizing a request.",
    )
    write_skill(
        skill_root / "workflow" / "rnaseq-differential-expression",
        "rnaseq-differential-expression",
        "Use when running a workflow.",
    )
    write_skill(
        skill_root / "blastn",
        "blastn",
        "Use when running blastn.",
    )

    payload = run_export(skill_root)
    by_id = {item["id"]: item for item in payload["skills"]}

    assert payload["skill_count"] == 3
    assert by_id["request-normalizer"]["layer"] == "orchestrator"
    assert by_id["rnaseq-differential-expression"]["layer"] == "workflow"
    assert by_id["blastn"]["layer"] == "atomic"


def test_export_skill_registry_applies_workflow_overrides_for_flat_legacy_skills(tmp_path: Path) -> None:
    skill_root = tmp_path / ".claude" / "skills"
    write_skill(
        skill_root / "sequence-analysis",
        "sequence-analysis",
        "Use when running sequence analysis.",
    )

    payload = run_export(skill_root)
    only_skill = payload["skills"][0]

    assert only_skill["id"] == "sequence-analysis"
    assert only_skill["layer"] == "workflow"
    assert only_skill["classification_source"] == "workflow-override"

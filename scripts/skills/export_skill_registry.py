#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_SKILL_ROOT = ROOT / ".claude" / "skills"
LAYER_NAMES = {"atomic", "workflow", "orchestrator", "policy"}
WORKFLOW_OVERRIDES = {
    "bioinformatics-toolkit",
    "biomni",
    "evo2",
    "phage-design",
    "protein-structure",
    "rfdiffusion",
    "rnaseq-pipeline",
    "sequence-analysis",
    "yeast_database",
}


def parse_frontmatter(text: str) -> dict[str, str]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
      return {}

    metadata: dict[str, str] = {}
    for line in lines[1:]:
        if line.strip() == "---":
            break
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        metadata[key.strip()] = value.strip().strip('"').strip("'")
    return metadata


def infer_layer(relative_path: Path, skill_name: str) -> tuple[str, str]:
    parts = relative_path.parts
    if len(parts) >= 3 and parts[0] in LAYER_NAMES and parts[-1] == "SKILL.md":
        return parts[0], "layered-path"
    if skill_name in WORKFLOW_OVERRIDES:
        return "workflow", "workflow-override"
    return "atomic", "default-atomic"


def discover_skill_records(skill_root: Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []

    for skill_path in sorted(skill_root.rglob("SKILL.md")):
        relative_path = skill_path.relative_to(skill_root)
        text = skill_path.read_text(encoding="utf-8", errors="ignore")
        frontmatter = parse_frontmatter(text)
        skill_name = frontmatter.get("name") or skill_path.parent.name
        description = frontmatter.get("description", "")
        layer, classification_source = infer_layer(relative_path, skill_name)
        records.append(
            {
                "id": skill_name,
                "name": skill_name,
                "description": description,
                "layer": layer,
                "classification_source": classification_source,
                "path": str(skill_path),
                "relative_path": str(relative_path),
                "user_invocable": frontmatter.get("user-invocable", "").lower() == "true",
            }
        )

    return records


def build_registry(skill_root: Path = DEFAULT_SKILL_ROOT) -> dict[str, Any]:
    skill_root = skill_root.expanduser().resolve()
    records = discover_skill_records(skill_root)
    layer_counts: dict[str, int] = {}
    for record in records:
        layer = str(record["layer"])
        layer_counts[layer] = layer_counts.get(layer, 0) + 1

    return {
        "skill_root": str(skill_root),
        "skill_count": len(records),
        "layer_counts": layer_counts,
        "skills": records,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Export a recursive skill registry snapshot for the Bio Skill System.")
    parser.add_argument(
        "--skill-root",
        default=str(DEFAULT_SKILL_ROOT),
        help="Skill root to scan recursively.",
    )
    parser.add_argument(
        "--format",
        choices=("json",),
        default="json",
        help="Output format. JSON is the current supported format.",
    )
    parser.add_argument(
        "--output",
        help="Optional output file path. If omitted, prints to stdout.",
    )
    args = parser.parse_args()

    registry = build_registry(Path(args.skill_root))
    payload = json.dumps(registry, indent=2, ensure_ascii=False)

    if args.output:
        output_path = Path(args.output).expanduser()
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(payload + "\n", encoding="utf-8")
    else:
        print(payload)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

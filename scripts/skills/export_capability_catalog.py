#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

import yaml

from scripts.skills.export_skill_registry import build_registry as build_skill_registry


ROOT = Path(__file__).resolve().parents[2]
REGISTRY_DIR = ROOT / "registry"
PROJECT_SKILL_ROOT = ROOT / ".claude" / "skills"


def _load_yaml(path: Path) -> dict[str, Any]:
    payload = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(payload, dict):
        raise ValueError(f"Expected mapping in {path}")
    return payload


def _runtime_mode_for_bridge_modes(modes: set[str]) -> str:
    if not modes:
        return "session-bridged-hybrid"
    if all(mode.startswith("local") for mode in modes):
        return "session-bridged-local"
    return "session-bridged-hybrid"


def _bridge_details_by_workflow(bridges_payload: dict[str, Any]) -> dict[str, dict[str, Any]]:
    details: dict[str, dict[str, Any]] = {}
    for workflow in bridges_payload.get("workflows", []):
        if not isinstance(workflow, dict):
            continue
        workflow_id = str(workflow.get("workflow_id"))
        bridge_modes: set[str] = set()
        required_tools: set[str] = set()
        reproducibility_support: set[str] = set()
        strategy_ids: list[str] = []

        for stage_map in [workflow.get("default_stages", {})]:
            if not isinstance(stage_map, dict):
                continue
            for bridge in stage_map.values():
                if not isinstance(bridge, dict):
                    continue
                bridge_modes.add(str(bridge.get("execution_mode", "")).strip())
                required_tools.update(str(item) for item in bridge.get("required_tools", []) if str(item).strip())
                reproducibility_support.add(str(bridge.get("reproducibility_support", "")).strip())

        strategies = workflow.get("strategies", {})
        if isinstance(strategies, dict):
            for strategy_id, stage_map in strategies.items():
                strategy_ids.append(str(strategy_id))
                if not isinstance(stage_map, dict):
                    continue
                for bridge in stage_map.values():
                    if not isinstance(bridge, dict):
                        continue
                    bridge_modes.add(str(bridge.get("execution_mode", "")).strip())
                    required_tools.update(str(item) for item in bridge.get("required_tools", []) if str(item).strip())
                    reproducibility_support.add(str(bridge.get("reproducibility_support", "")).strip())

        details[workflow_id] = {
            "bridge_execution_modes": sorted(mode for mode in bridge_modes if mode),
            "required_tools": sorted(required_tools),
            "reproducibility_support": sorted(item for item in reproducibility_support if item),
            "strategy_ids": sorted(strategy_ids),
        }
    return details


def _benchmark_ids_by_workflow(benchmarks_payload: dict[str, Any]) -> dict[str, list[str]]:
    mapping: dict[str, set[str]] = defaultdict(set)
    for benchmark in benchmarks_payload.get("benchmarks", []):
        if not isinstance(benchmark, dict):
            continue
        benchmark_id = str(benchmark.get("id"))
        for workflow_id in benchmark.get("target_workflow_ids", []):
            mapping[str(workflow_id)].add(benchmark_id)
    return {workflow_id: sorted(ids) for workflow_id, ids in mapping.items()}


def build_capability_catalog() -> dict[str, Any]:
    catalog_policy = _load_yaml(REGISTRY_DIR / "capability_catalog.yaml")
    seed_skills = _load_yaml(REGISTRY_DIR / "skills.yaml")
    workflows_payload = _load_yaml(REGISTRY_DIR / "workflows.yaml")
    analysis_flows = _load_yaml(REGISTRY_DIR / "analysis_flows.yaml")
    bridges_payload = _load_yaml(REGISTRY_DIR / "execution_bridges.yaml")
    benchmarks_payload = _load_yaml(REGISTRY_DIR / "benchmarks.yaml")
    dynamic_skills = build_skill_registry(PROJECT_SKILL_ROOT)

    dynamic_by_id = {
        str(item.get("id")): dict(item)
        for item in dynamic_skills.get("skills", [])
        if isinstance(item, dict)
    }
    workflow_by_id = {
        str(item.get("id")): dict(item)
        for item in workflows_payload.get("workflows", [])
        if isinstance(item, dict)
    }
    bridge_details = _bridge_details_by_workflow(bridges_payload)
    benchmark_ids = _benchmark_ids_by_workflow(benchmarks_payload)
    hero_ids = {str(item) for item in catalog_policy.get("hero_workflow_ids", [])}

    capabilities: list[dict[str, Any]] = []

    for skill in seed_skills.get("skills", []):
        if not isinstance(skill, dict):
            continue
        skill_id = str(skill.get("id"))
        dynamic_record = dynamic_by_id.get(skill_id, {})
        capabilities.append(
            {
                "id": skill_id,
                "title": str(dynamic_record.get("name") or skill_id),
                "capability_kind": "control_plane_skill",
                "execution_tier": "first_party_executable",
                "runtime_mode": "local-agent-control-plane",
                "verification_level": "registry_backed",
                "reproducibility_level": "canonical_session_truth",
                "source_kind": "seed_skill_registry",
                "runnable": True,
                "summary": str(dynamic_record.get("description") or ""),
                "layer": skill.get("layer"),
                "path": str(skill.get("path")),
                "classification_source": dynamic_record.get("classification_source"),
                "provenance": {
                    "registry": "registry/skills.yaml",
                    "skill_path": str(skill.get("path")),
                    "dynamic_registry": "scripts/skills/export_skill_registry.py",
                },
            }
        )

    for flow in analysis_flows.get("flows", []):
        if not isinstance(flow, dict):
            continue
        workflow_id = str(flow.get("workflow_id"))
        workflow = workflow_by_id.get(workflow_id, {})
        bridge = bridge_details.get(workflow_id, {})
        modes = set(bridge.get("bridge_execution_modes", []))
        capabilities.append(
            {
                "id": workflow_id,
                "title": str(flow.get("title") or workflow.get("summary") or workflow_id),
                "capability_kind": "workflow_family",
                "execution_tier": "bridge_executable",
                "runtime_mode": _runtime_mode_for_bridge_modes(modes),
                "verification_level": "benchmark_contract" if benchmark_ids.get(workflow_id) else "registry_backed",
                "reproducibility_level": "delivery_bundle_defined",
                "source_kind": "analysis_flow_registry",
                "runnable": True,
                "hero_lane": workflow_id in hero_ids,
                "summary": str(flow.get("summary") or ""),
                "stage_count": len(flow.get("stage_flows", [])),
                "delivery_bundle_items": list(flow.get("delivery_bundle", [])),
                "request_tags": list(workflow.get("request_tags", [])),
                "benchmark_ids": benchmark_ids.get(workflow_id, []),
                "bridge_execution_modes": bridge.get("bridge_execution_modes", []),
                "required_tools": bridge.get("required_tools", []),
                "reproducibility_support": bridge.get("reproducibility_support", []),
                "strategy_ids": bridge.get("strategy_ids", []),
                "provenance": {
                    "analysis_flow_registry": "registry/analysis_flows.yaml",
                    "workflow_registry": "registry/workflows.yaml",
                    "execution_bridges": "registry/execution_bridges.yaml",
                    "benchmarks": "registry/benchmarks.yaml",
                },
            }
        )

    reference_entries: dict[str, dict[str, Any]] = {}
    for workflow in workflows_payload.get("workflows", []):
        if not isinstance(workflow, dict):
            continue
        workflow_id = str(workflow.get("id"))
        for source in workflow.get("official_sources", []):
            if not isinstance(source, dict):
                continue
            label = str(source.get("label") or source.get("url") or "").strip()
            url = str(source.get("url") or "").strip()
            reference_id = f"reference:{workflow_id}:{label.lower().replace(' ', '-')}"
            reference_entries[reference_id] = {
                "id": reference_id,
                "title": label,
                "capability_kind": "official_reference",
                "execution_tier": "reference_only",
                "runtime_mode": "external-reference",
                "verification_level": "cited_reference",
                "reproducibility_level": "external_project_contract",
                "source_kind": "official_reference",
                "runnable": False,
                "summary": f"Official grounding source for {workflow_id}.",
                "relates_to": [workflow_id],
                "url": url,
                "provenance": {
                    "workflow_registry": "registry/workflows.yaml",
                },
            }

    capabilities.extend(reference_entries.values())
    capabilities = sorted(
        capabilities,
        key=lambda item: (
            str(item.get("execution_tier")),
            str(item.get("capability_kind")),
            str(item.get("id")),
        ),
    )

    tier_counts = Counter(str(item.get("execution_tier")) for item in capabilities)
    kind_counts = Counter(str(item.get("capability_kind")) for item in capabilities)

    return {
        "catalog_policy": catalog_policy,
        "summary": {
            "total_capabilities": len(capabilities),
            "execution_tier_counts": dict(sorted(tier_counts.items())),
            "capability_kind_counts": dict(sorted(kind_counts.items())),
            "hero_workflow_ids": sorted(hero_ids),
            "project_skill_count": int(dynamic_skills.get("skill_count", 0)),
        },
        "capabilities": capabilities,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Export the bio-agent capability catalog derived from evidence-bearing registries.")
    parser.add_argument("--output", help="Optional output file. Defaults to stdout.")
    args = parser.parse_args()

    payload = build_capability_catalog()
    text = json.dumps(payload, indent=2, ensure_ascii=False) + "\n"
    if args.output:
        output_path = Path(args.output).expanduser()
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(text, encoding="utf-8")
    else:
        print(text, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

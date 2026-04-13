#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[2]

DEFAULT_SKILL_ROOTS = [
    ("project-local", ROOT / ".claude" / "skills"),
    ("global-codex", Path.home() / ".codex" / "skills"),
    ("global-agents", Path.home() / ".agents" / "skills"),
]

CATEGORY_OVERRIDES = {
    "adaptyv": "lab-and-platforms",
    "alphafold-database": "proteins-and-structure",
    "anndata": "single-cell-omics",
    "arboreto": "single-cell-omics",
    "benchling-integration": "lab-and-platforms",
    "blastn": "core-bioinformatics",
    "bgpt-paper-search": "bio-databases-and-literature",
    "bioinformatics-toolkit": "core-bioinformatics",
    "biomni": "bio-databases-and-literature",
    "biopython": "core-bioinformatics",
    "biorxiv-database": "bio-databases-and-literature",
    "bioservices": "bio-databases-and-literature",
    "brenda-database": "bio-databases-and-literature",
    "bowtie2": "core-bioinformatics",
    "bwa": "core-bioinformatics",
    "cellxgene-census": "single-cell-omics",
    "chembl-database": "drug-discovery-and-cheminformatics",
    "clinical-decision-support": "clinical-and-imaging",
    "clinical-reports": "clinical-and-imaging",
    "clinicaltrials-database": "clinical-and-imaging",
    "clinpgx-database": "clinical-and-imaging",
    "clinvar-database": "clinical-and-imaging",
    "cobrapy": "systems-biology",
    "cosmic-database": "clinical-and-imaging",
    "deepchem": "drug-discovery-and-cheminformatics",
    "deeptools": "core-bioinformatics",
    "diffdock": "drug-discovery-and-cheminformatics",
    "dnanexus-integration": "lab-and-platforms",
    "drugbank-database": "drug-discovery-and-cheminformatics",
    "ena-database": "bio-databases-and-literature",
    "ensembl-database": "bio-databases-and-literature",
    "esm": "proteins-and-structure",
    "etetoolkit": "core-bioinformatics",
    "evo2": "proteins-and-structure",
    "fasterq-dump": "core-bioinformatics",
    "fastp": "core-bioinformatics",
    "fda-database": "clinical-and-imaging",
    "gene-database": "bio-databases-and-literature",
    "geniml": "core-bioinformatics",
    "geo-database": "bio-databases-and-literature",
    "gget": "core-bioinformatics",
    "ginkgo-cloud-lab": "lab-and-platforms",
    "gtars": "core-bioinformatics",
    "gwas-database": "bio-databases-and-literature",
    "histolab": "clinical-and-imaging",
    "hmdb-database": "drug-discovery-and-cheminformatics",
    "hmmscan": "core-bioinformatics",
    "hmmsearch": "core-bioinformatics",
    "imaging-data-commons": "clinical-and-imaging",
    "iqtree": "core-bioinformatics",
    "kegg-database": "bio-databases-and-literature",
    "labarchive-integration": "lab-and-platforms",
    "lamindb": "lab-and-platforms",
    "latchbio-integration": "lab-and-platforms",
    "matchms": "drug-discovery-and-cheminformatics",
    "medchem": "drug-discovery-and-cheminformatics",
    "metabolomics-workbench-database": "drug-discovery-and-cheminformatics",
    "neurokit2": "clinical-and-imaging",
    "neuropixels-analysis": "clinical-and-imaging",
    "omero-integration": "clinical-and-imaging",
    "opentargets-database": "drug-discovery-and-cheminformatics",
    "opentrons-integration": "lab-and-platforms",
    "pathml": "clinical-and-imaging",
    "pdb-database": "proteins-and-structure",
    "phage-design": "proteins-and-structure",
    "protein-structure": "proteins-and-structure",
    "protocolsio-integration": "lab-and-platforms",
    "pubchem-database": "drug-discovery-and-cheminformatics",
    "pubmed-database": "bio-databases-and-literature",
    "pydeseq2": "core-bioinformatics",
    "pydicom": "clinical-and-imaging",
    "pyhealth": "clinical-and-imaging",
    "pylabrobot": "lab-and-platforms",
    "pyopenms": "drug-discovery-and-cheminformatics",
    "pysam": "core-bioinformatics",
    "pytdc": "drug-discovery-and-cheminformatics",
    "reactome-database": "bio-databases-and-literature",
    "rdkit": "drug-discovery-and-cheminformatics",
    "rfdiffusion": "proteins-and-structure",
    "rnafold": "proteins-and-structure",
    "samtools": "core-bioinformatics",
    "rnaseq-pipeline": "core-bioinformatics",
    "seqkit": "core-bioinformatics",
    "rowan": "drug-discovery-and-cheminformatics",
    "scanpy": "single-cell-omics",
    "scikit-bio": "core-bioinformatics",
    "scvi-tools": "single-cell-omics",
    "sequence-analysis": "core-bioinformatics",
    "star": "core-bioinformatics",
    "string-database": "bio-databases-and-literature",
    "tiledbvcf": "core-bioinformatics",
    "torchdrug": "drug-discovery-and-cheminformatics",
    "yeast_database": "bio-databases-and-literature",
}

STRONG_BIO_PATTERNS = [
    r"\bbioinformatics\b",
    r"\bbiological\b",
    r"\bbiology\b",
    r"\bbiomedical\b",
    r"\bgenomics?\b",
    r"\bgene\b",
    r"\bgenes\b",
    r"\bgene expression\b",
    r"\bvariant\b",
    r"\bvariants\b",
    r"\bprotein\b",
    r"\bproteins\b",
    r"\brna-seq\b",
    r"\brna seq\b",
    r"\bdna\b",
    r"\bsingle-cell\b",
    r"\bsingle cell\b",
    r"\btranscriptomics\b",
    r"\bproteomics\b",
    r"\bmetabolomics\b",
    r"\bcheminformatics\b",
    r"\bdrug discovery\b",
    r"\bclinical\b",
    r"\bpathology\b",
    r"\bradiology\b",
    r"\bmicroscopy\b",
    r"\bflow cytometry\b",
    r"\bmolecular biology\b",
    r"\bwet-lab\b",
    r"\blab automation\b",
    r"\bphylogen",
    r"\bsequencing\b",
    r"\bwhole-slide\b",
    r"\bscRNA-seq\b",
    r"\bscATAC-seq\b",
    r"\bomics\b",
]


def _parse_frontmatter(text: str) -> dict[str, str]:
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


def _load_yaml(path: Path) -> dict[str, Any]:
    payload = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(payload, dict):
        raise ValueError(f"Expected mapping at {path}")
    return payload


def _now_iso() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def _parse_runtime_metadata(text: str) -> dict[str, str | None]:
    command = ""
    local_executable = ""
    install_hint = ""
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if line.startswith("- **Command"):
            matches = re.findall(r"`([^`]+)`", line)
            if matches:
                command = matches[0].strip()
        elif line.startswith("- **Local executable"):
            matches = re.findall(r"`([^`]+)`", line)
            if matches:
                local_executable = matches[0].strip()
        elif line.startswith("- **Install hint"):
            matches = re.findall(r"`([^`]+)`", line)
            install_hint = matches[0].strip() if matches else line.split(":", 1)[-1].strip()
    return {
        "command": command or None,
        "local_executable": local_executable or None,
        "install_hint": install_hint or None,
    }


def _runtime_status(runtime: dict[str, str | None]) -> tuple[str, bool]:
    local_executable = str(runtime.get("local_executable") or "").strip()
    command = str(runtime.get("command") or "").strip()
    if local_executable:
        return "local-cli", Path(local_executable).expanduser().is_file()
    if command:
        executable = command.split()[0]
        return "local-cli", shutil.which(executable) is not None
    return "prompt-bridge", False


def classify_skill(name: str, description: str) -> dict[str, Any]:
    normalized_name = name.strip().lower()
    description_lower = description.strip().lower()

    if normalized_name in CATEGORY_OVERRIDES:
        return {"is_bio": True, "category": CATEGORY_OVERRIDES[normalized_name]}

    text = f"{normalized_name} {description_lower}"
    if any(re.search(pattern, text, flags=re.IGNORECASE) for pattern in STRONG_BIO_PATTERNS):
        if "single-cell" in text or "single cell" in text or normalized_name in {"scanpy", "anndata", "scvi-tools", "cellxgene-census", "arboreto"}:
            return {"is_bio": True, "category": "single-cell-omics"}
        if any(token in text for token in ["protein", "alphafold", "structure", "phage", "esm"]):
            return {"is_bio": True, "category": "proteins-and-structure"}
        if any(token in text for token in ["drug", "compound", "molecule", "metabol", "cheminformatics", "docking"]):
            return {"is_bio": True, "category": "drug-discovery-and-cheminformatics"}
        if any(token in text for token in ["clinical", "pathology", "radiology", "dicom", "imaging", "microscopy", "flow cytometry", "neuro"]):
            return {"is_bio": True, "category": "clinical-and-imaging"}
        if any(token in text for token in ["lab", "eln", "protocol", "automation", "registry"]):
            return {"is_bio": True, "category": "lab-and-platforms"}
        if any(token in text for token in ["database", "pubmed", "biorxiv", "reactome", "string", "kegg", "ensembl", "gene", "genome"]):
            return {"is_bio": True, "category": "bio-databases-and-literature"}
        return {"is_bio": True, "category": "core-bioinformatics"}

    return {"is_bio": False, "category": None}


def _scope_roots() -> list[tuple[str, Path]]:
    return [(scope, root.expanduser()) for scope, root in DEFAULT_SKILL_ROOTS]


def collect_local_bio_skills() -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []

    for scope, root in _scope_roots():
        if not root.exists():
            continue
        for skill_path in sorted(root.rglob("SKILL.md")):
            text = skill_path.read_text(encoding="utf-8", errors="ignore")
            frontmatter = _parse_frontmatter(text)
            runtime = _parse_runtime_metadata(text)
            runtime_mode, runtime_available = _runtime_status(runtime)
            name = frontmatter.get("name") or skill_path.parent.name
            description = frontmatter.get("description", "")
            classification = classify_skill(name, description)
            if not classification["is_bio"]:
                continue
            records.append(
                {
                    "name": name,
                    "scope": scope,
                    "category": classification["category"],
                    "path": str(skill_path),
                    "description": description,
                    "runtime_mode": runtime_mode,
                    "runtime_available": runtime_available,
                    "command": runtime.get("command"),
                    "local_executable": runtime.get("local_executable"),
                    "install_hint": runtime.get("install_hint"),
                }
            )

    return sorted(records, key=lambda item: (item["scope"], item["category"], item["name"]))


def build_capability_catalog(records: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    records = records if records is not None else collect_local_bio_skills()
    config = _load_yaml(ROOT / "registry" / "capability_catalog.yaml")
    analysis_flows = _load_yaml(ROOT / "registry" / "analysis_flows.yaml")
    benchmark_registry = _load_yaml(ROOT / "registry" / "benchmarks.yaml")

    flows_by_id = {
        str(item.get("workflow_id")): dict(item)
        for item in analysis_flows.get("flows", [])
        if isinstance(item, dict)
    }
    benchmark_ids_by_workflow: dict[str, list[str]] = {}
    for benchmark in benchmark_registry.get("benchmarks", []):
        if not isinstance(benchmark, dict):
            continue
        benchmark_id = str(benchmark.get("id"))
        for workflow_id in benchmark.get("target_workflow_ids", []):
            benchmark_ids_by_workflow.setdefault(str(workflow_id), []).append(benchmark_id)

    capabilities: list[dict[str, Any]] = []
    hero_ids = {str(item.get("workflow_id")) for item in config.get("hero_workflows", [])}

    for hero in config.get("hero_workflows", []):
        workflow_id = str(hero.get("workflow_id"))
        flow = flows_by_id.get(workflow_id, {})
        capabilities.append(
            {
                "id": workflow_id,
                "name": hero.get("title") or flow.get("title") or workflow_id,
                "capability_group": "first_party_executable",
                "execution_tier": "first_party_executable",
                "runtime_mode": "session-hero-runner",
                "verification_level": hero.get("verification_level", "benchmark_contract"),
                "reproducibility_level": hero.get("reproducibility_level", "automatic_session_bundle"),
                "source_kind": "registry-grounded-workflow",
                "summary": flow.get("summary") or hero.get("summary") or "",
                "runnable": True,
                "provenance": {
                    "catalog_config": "registry/capability_catalog.yaml",
                    "analysis_flow": "registry/analysis_flows.yaml",
                    "benchmark_registry": "registry/benchmarks.yaml",
                    "benchmark_ids": benchmark_ids_by_workflow.get(workflow_id, []),
                },
            }
        )

    for workflow_id, flow in flows_by_id.items():
        if workflow_id in hero_ids:
            continue
        capabilities.append(
            {
                "id": workflow_id,
                "name": flow.get("title") or workflow_id,
                "capability_group": "reference_only",
                "execution_tier": "reference_only",
                "runtime_mode": "planning-reference",
                "verification_level": "registry_modeled",
                "reproducibility_level": "not_packaged",
                "source_kind": "analysis-flow-registry",
                "summary": flow.get("summary") or "",
                "runnable": False,
                "provenance": {
                    "analysis_flow": "registry/analysis_flows.yaml",
                    "benchmark_registry": "registry/benchmarks.yaml",
                    "benchmark_ids": benchmark_ids_by_workflow.get(workflow_id, []),
                },
            }
        )

    seen_bridge_ids: set[str] = set()
    for record in records:
        capability_id = str(record["name"])
        if capability_id in seen_bridge_ids:
            continue
        seen_bridge_ids.add(capability_id)
        capabilities.append(
            {
                "id": capability_id,
                "name": record["name"],
                "capability_group": "bridge_executable",
                "execution_tier": "bridge_executable",
                "runtime_mode": record["runtime_mode"],
                "verification_level": "machine_detected" if record["runtime_available"] else "declared_only",
                "reproducibility_level": "manual_bridge",
                "source_kind": "skill-doc",
                "summary": record["description"],
                "runnable": bool(record["runtime_available"]),
                "category": record["category"],
                "provenance": {
                    "scope": record["scope"],
                    "skill_path": record["path"],
                    "command": record.get("command"),
                    "local_executable": record.get("local_executable"),
                },
            }
        )

    group_counts: dict[str, int] = {}
    for item in capabilities:
        group = str(item["capability_group"])
        group_counts[group] = group_counts.get(group, 0) + 1

    return {
        "generated_at": _now_iso(),
        "catalog_version": config.get("version", 1),
        "vocabulary": dict(config.get("vocabulary", {})),
        "summary": {
            "capability_count": len(capabilities),
            "group_counts": group_counts,
        },
        "capabilities": sorted(
            capabilities,
            key=lambda item: (
                str(item["capability_group"]),
                str(item.get("category") or ""),
                str(item["name"]).lower(),
            ),
        ),
    }


def write_inventory_doc(output_path: Path, records: list[dict[str, Any]]) -> Path:
    output_path.parent.mkdir(parents=True, exist_ok=True)

    scope_order = ["project-local", "global-codex", "global-agents"]
    lines = [
        "# Local Bio Skill Inventory",
        "",
        "Generated by `scripts/skills/collect_local_bio_skills.py`.",
        "",
        f"- Total collected bio skills: {len(records)}",
        "",
        "## Scope Summary",
        "",
        "| Scope | Count |",
        "| --- | --- |",
    ]

    for scope in scope_order:
        count = sum(1 for item in records if item["scope"] == scope)
        lines.append(f"| {scope} | {count} |")

    for scope in scope_order:
        scoped = [item for item in records if item["scope"] == scope]
        if not scoped:
            continue
        lines.extend(
            [
                "",
                f"## {scope}",
                "",
                "| Skill | Category | Path | Description |",
                "| --- | --- | --- | --- |",
            ]
        )
        for item in scoped:
            lines.append(
                f"| {item['name']} | {item['category']} | `{item['path']}` | {item['description']} |"
            )

    lines.append("")
    output_path.write_text("\n".join(lines), encoding="utf-8")
    return output_path


def main() -> int:
    parser = argparse.ArgumentParser(description="Collect locally available bioinformatics-related skills.")
    parser.add_argument(
        "--output",
        help="Markdown inventory output path.",
    )
    parser.add_argument("--format", choices=("markdown", "json", "capability-json"), default="markdown")
    args = parser.parse_args()

    records = collect_local_bio_skills()
    output_path = Path(args.output).expanduser() if args.output else None
    if args.format == "json":
        print(json.dumps(records, indent=2, ensure_ascii=False))
        return 0
    if args.format == "capability-json":
        payload = build_capability_catalog(records)
        if output_path is not None:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        else:
            print(json.dumps(payload, indent=2, ensure_ascii=False))
        return 0

    output_path = output_path or (ROOT / "docs" / "skills" / "local-bio-skill-inventory.md")
    write_inventory_doc(output_path, records)
    print(output_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

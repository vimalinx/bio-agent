#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


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
                }
            )

    return sorted(records, key=lambda item: (item["scope"], item["category"], item["name"]))


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
        default=str(ROOT / "docs" / "skills" / "local-bio-skill-inventory.md"),
        help="Markdown inventory output path.",
    )
    parser.add_argument("--format", choices=("markdown", "json"), default="markdown")
    args = parser.parse_args()

    records = collect_local_bio_skills()
    output_path = Path(args.output).expanduser()
    if args.format == "json":
        print(json.dumps(records, indent=2, ensure_ascii=False))
        return 0

    write_inventory_doc(output_path, records)
    print(output_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

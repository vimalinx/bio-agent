#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path
from shutil import which
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from lib.workspace_env import ensure_workspace_path, resolve_workspace_python


KNOWN_DOMAIN_SKILLS = [
    "bioinformatics-toolkit",
    "biomni",
    "evo2",
    "phage-design",
    "protein-structure",
    "rfdiffusion",
    "rnaseq-pipeline",
    "sequence-analysis",
    "yeast_database",
]

GENERIC_BIOCONDA_PACKAGE_PREFIXES = ("perl-",)
IGNORED_BIN_SUFFIXES = (".ini", ".json", ".md", ".txt", ".pm")

INSTALLER_TOOL_MAP: dict[str, list[dict[str, str]]] = {
    "multiqc": [
        {
            "command": "multiqc",
            "summary": "Aggregate quality control reports from multiple bioinformatics tools.",
        }
    ],
    "seqkit": [
        {
            "command": "seqkit",
            "summary": "FASTA and FASTQ toolkit for statistics, filtering, and conversion.",
        }
    ],
    "mafft": [
        {
            "command": "mafft",
            "summary": "Multiple sequence alignment for nucleotide or protein sequences.",
        }
    ],
    "iqtree": [
        {
            "command": "iqtree",
            "aliases": ["iqtree2"],
            "summary": "Maximum likelihood phylogeny inference for aligned sequences.",
        }
    ],
    "star": [
        {
            "command": "STAR",
            "summary": "Spliced RNA-seq read alignment against a genome index.",
        }
    ],
    "hisat2": [
        {
            "command": "hisat2",
            "summary": "Fast RNA-seq read alignment with graph-based indexing.",
        }
    ],
    "subread": [
        {
            "command": "featureCounts",
            "summary": "Assign aligned reads to genes or genomic features.",
        }
    ],
    "fastp": [
        {
            "command": "fastp",
            "summary": "FASTQ quality control, filtering, and adapter trimming.",
        }
    ],
    "sra-tools": [
        {
            "command": "fasterq-dump",
            "aliases": ["fastq-dump"],
            "summary": "Download FASTQ reads from the NCBI SRA archive.",
        }
    ],
}

TOOL_REFERENCE_SECTION_MAP: dict[str, list[dict[str, str]]] = {
    "BLAST": [
        {
            "command": "blastn",
            "summary": "Nucleotide sequence similarity search with BLAST.",
        }
    ],
    "HMMER": [
        {
            "command": "hmmscan",
            "summary": "Search sequences against profile hidden Markov models.",
        },
        {
            "command": "hmmsearch",
            "summary": "Search profile hidden Markov models against sequence databases.",
        },
    ],
    "bowtie2": [
        {
            "command": "bowtie2",
            "summary": "Short-read alignment against indexed references.",
        }
    ],
    "bwa": [
        {
            "command": "bwa",
            "summary": "Burrows-Wheeler aligner for low-divergence sequence reads.",
        }
    ],
    "samtools": [
        {
            "command": "samtools",
            "summary": "Utilities for SAM, BAM, and CRAM alignment files.",
        }
    ],
    "prodigal": [
        {
            "command": "prodigal",
            "summary": "Gene prediction for prokaryotic genomes.",
        }
    ],
    "ViennaRNA": [
        {
            "command": "RNAfold",
            "summary": "Predict RNA secondary structure and minimum free energy folds.",
        }
    ],
}


def normalize_skill_name(value: str) -> str:
    text = value.strip()
    text = re.sub(r"([a-z0-9])([A-Z])", r"\1-\2", text)
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    text = re.sub(r"-+", "-", text).strip("-")
    return text


def _merge_tool(registry: dict[str, dict[str, Any]], candidate: dict[str, Any]) -> None:
    name = normalize_skill_name(str(candidate["name"]))
    record = registry.setdefault(
        name,
        {
            "name": name,
            "command": candidate.get("command") or candidate["name"],
            "aliases": [],
            "summary": "",
            "path": None,
            "sources": [],
            "domain_skills": [],
            "package_names": [],
        },
    )

    summary = str(candidate.get("summary", "")).strip()
    if summary and (
        not record["summary"]
        or record["summary"].startswith("CLI installed by bioconda package ")
    ):
        record["summary"] = summary

    command = str(candidate.get("command", "")).strip()
    if command and not record["command"]:
        record["command"] = command

    for alias in candidate.get("aliases", []):
        alias_text = str(alias).strip()
        if alias_text and alias_text not in record["aliases"]:
            record["aliases"].append(alias_text)

    path = candidate.get("path")
    if path and not record["path"]:
        record["path"] = str(path)

    for source in candidate.get("sources", []):
        if source not in record["sources"]:
            record["sources"].append(source)

    for skill_name in candidate.get("domain_skills", []):
        if skill_name not in record["domain_skills"]:
            record["domain_skills"].append(skill_name)

    for package_name in candidate.get("package_names", []):
        package_text = str(package_name).strip()
        if package_text and package_text not in record["package_names"]:
            record["package_names"].append(package_text)


def _parse_install_script_tools(script_path: Path) -> list[dict[str, Any]]:
    if not script_path.exists():
        return []

    tools: list[dict[str, Any]] = []
    in_block = False
    for raw_line in script_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if line.startswith("TOOLS=("):
            in_block = True
            continue
        if in_block and line == ")":
            break
        if not in_block:
            continue
        match = re.search(r'"([^"]+)"', line)
        if not match:
            continue
        package_name = match.group(1)
        mapped = INSTALLER_TOOL_MAP.get(package_name, [{"command": package_name, "summary": ""}])
        for item in mapped:
            tools.append(
                {
                    "name": normalize_skill_name(item["command"]),
                    "command": item["command"],
                    "aliases": item.get("aliases", []),
                    "summary": item.get("summary", ""),
                    "sources": ["install_script"],
                }
            )
    return tools


def _parse_tool_reference(tool_reference_path: Path) -> list[dict[str, Any]]:
    if not tool_reference_path.exists():
        return []

    tools: list[dict[str, Any]] = []
    for heading in re.findall(r"^##\s+(.+?)\s*$", tool_reference_path.read_text(encoding="utf-8"), re.MULTILINE):
        for item in TOOL_REFERENCE_SECTION_MAP.get(heading, []):
            tools.append(
                {
                    "name": normalize_skill_name(item["command"]),
                    "command": item["command"],
                    "summary": item.get("summary", ""),
                    "sources": ["tool_reference"],
                    "domain_skills": ["bioinformatics-toolkit"],
                }
            )
    return tools


def resolve_workspace_env_root() -> Path | None:
    python_path = resolve_workspace_python()
    env_root = python_path.parent.parent
    if env_root.is_dir():
        return env_root
    return None


def discover_conda_bio_tools(conda_meta_dir: Path, env_bin_dir: Path) -> list[dict[str, Any]]:
    registry: dict[str, dict[str, Any]] = {}
    if not conda_meta_dir.exists() or not env_bin_dir.exists():
        return []

    for meta_path in sorted(conda_meta_dir.glob("*.json")):
        try:
            metadata = json.loads(meta_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            continue

        channel = str(metadata.get("channel", "")).lower()
        url = str(metadata.get("url", "")).lower()
        if "bioconda" not in channel and "bioconda" not in url:
            continue

        package_name = str(metadata.get("name", "")).strip()
        if package_name.startswith(GENERIC_BIOCONDA_PACKAGE_PREFIXES):
            continue
        for file_name in metadata.get("files") or []:
            relative_path = Path(str(file_name))
            if relative_path.parts[:1] != ("bin",) or len(relative_path.parts) < 2:
                continue
            command_name = relative_path.name
            if command_name.startswith(".") or command_name.endswith(IGNORED_BIN_SUFFIXES):
                continue
            executable_path = env_bin_dir / command_name
            if not executable_path.is_file() or not os.access(executable_path, os.X_OK):
                continue
            _merge_tool(
                registry,
                {
                    "name": normalize_skill_name(command_name),
                    "command": command_name,
                    "path": str(executable_path),
                    "summary": f"CLI installed by bioconda package {package_name}.",
                    "sources": ["conda_bioconda"],
                    "package_names": [package_name],
                },
            )

    discovered = sorted(registry.values(), key=lambda item: item["name"])
    for item in discovered:
        item["aliases"] = sorted(item["aliases"])
        item["sources"] = sorted(item["sources"])
        item["domain_skills"] = sorted(item["domain_skills"])
        item["package_names"] = sorted(item["package_names"])
    return discovered


def discover_existing_domain_skills(repo_root: Path) -> list[str]:
    skills_root = repo_root / ".claude" / "skills"
    return [name for name in KNOWN_DOMAIN_SKILLS if (skills_root / name / "SKILL.md").exists()]


def discover_curated_tools(repo_root: Path) -> list[dict[str, Any]]:
    repo_root = repo_root.resolve()
    registry: dict[str, dict[str, Any]] = {}

    installer_path = repo_root / "scripts" / "maintenance" / "install_bio_tools.sh"
    tool_reference_path = repo_root / ".claude" / "skills" / "bioinformatics-toolkit" / "TOOLS.md"

    for candidate in _parse_install_script_tools(installer_path):
        _merge_tool(registry, candidate)

    for candidate in _parse_tool_reference(tool_reference_path):
        _merge_tool(registry, candidate)

    ensure_workspace_path()
    for record in list(registry.values()):
        candidates = [str(record.get("command", "")).strip(), *[str(item).strip() for item in record.get("aliases", [])]]
        for executable in [item for item in candidates if item]:
            resolved_path = which(executable)
            if not resolved_path:
                continue
            _merge_tool(
                registry,
                {
                    "name": record["name"],
                    "command": executable,
                    "path": resolved_path,
                    "sources": ["path"],
                },
            )
            break

    discovered = sorted(registry.values(), key=lambda item: item["name"])
    for item in discovered:
        item["aliases"] = sorted(item["aliases"])
        item["sources"] = sorted(item["sources"])
        item["domain_skills"] = sorted(item["domain_skills"])
        item["package_names"] = sorted(item["package_names"])
    return discovered


def discover_tools(repo_root: Path, source: str = "combined") -> list[dict[str, Any]]:
    source_mode = source.strip().lower()
    if source_mode not in {"curated", "linux-all", "combined"}:
        raise ValueError(f"Unsupported discovery source: {source}")

    registry: dict[str, dict[str, Any]] = {}

    if source_mode in {"curated", "combined", "linux-all"}:
        for item in discover_curated_tools(repo_root):
            _merge_tool(registry, item)

    if source_mode in {"linux-all", "combined"}:
        env_root = resolve_workspace_env_root()
        if env_root is not None:
            conda_tools = discover_conda_bio_tools(env_root / "conda-meta", env_root / "bin")
            for item in conda_tools:
                _merge_tool(registry, item)

    discovered = sorted(registry.values(), key=lambda item: item["name"])
    for item in discovered:
        item["aliases"] = sorted(item["aliases"])
        item["sources"] = sorted(item["sources"])
        item["domain_skills"] = sorted(item["domain_skills"])
        item["package_names"] = sorted(item["package_names"])
    return discovered


def main() -> int:
    parser = argparse.ArgumentParser(description="Discover local bioinformatics tools for skill generation.")
    parser.add_argument("--repo-root", default=".", help="Repository root to scan.")
    parser.add_argument(
        "--format",
        choices=("json", "markdown"),
        default="json",
        help="Output format.",
    )
    parser.add_argument(
        "--source",
        choices=("curated", "linux-all", "combined"),
        default="combined",
        help="Discovery source.",
    )
    args = parser.parse_args()

    discovered = discover_tools(Path(args.repo_root), source=args.source)
    if args.format == "json":
        print(json.dumps(discovered, indent=2, ensure_ascii=False))
        return 0

    print("| Tool | Command | Sources | Path |")
    print("| --- | --- | --- | --- |")
    for item in discovered:
        print(
            f"| {item['name']} | {item.get('command', '')} | "
            f"{', '.join(item.get('sources', []))} | {item.get('path', '') or '-'} |"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

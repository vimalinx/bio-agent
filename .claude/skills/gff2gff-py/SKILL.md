---
name: gff2gff-py
description: Use when converting GenBank-derived GFF into bcftools/csq-friendly Ensembl-like GFF3 with the legacy `gff2gff.py` helper.
disable-model-invocation: true
user-invocable: true
---

# gff2gff-py

## Quick Start

- **Command:** `/home/vimalinx/miniforge3/envs/bio/bin/gff2gff.py input.gff scratch.db > output.gff3`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/gff2gff.py`
- **Full reference:** See `references/help.md` for complete options and usage

## When To Use This Tool

- Salvage certain GenBank-style GFF inputs for downstream `bcftools csq` use.
- Build a temporary `gffutils` database and emit a simplified gene / transcript / CDS hierarchy to stdout.
- Use only when the input flavor matches the script's assumptions about `gene`, `mRNA`, `CDS`, `ncRNA`, `Name`, and `locus_tag` attributes.

## Common Patterns

```bash
# 1) Convert a GenBank-derived GFF and keep the intermediate gffutils DB
/home/vimalinx/miniforge3/envs/bio/bin/gff2gff.py \
  input.gff \
  scratch.db \
  > output.gff3
```

```bash
# 2) Write the scratch DB to a temporary location
tmp_db=$(mktemp /tmp/gffutils.XXXXXX.db)
/home/vimalinx/miniforge3/envs/bio/bin/gff2gff.py input.gff "$tmp_db" > output.gff3
```

## Recommended Workflow

1. Confirm that the Python environment actually provides `gffutils`; this script imports it before any argument parsing.
2. Use a disposable path for the second argument, because the script creates a `gffutils` database there with `force=True`.
3. Redirect stdout to your desired output GFF3 file.
4. Inspect the result for expected `###` separators plus `gene`, `transcript`, and `CDS` records before trusting it in annotation workflows.

## Guardrails

- In this environment `gff2gff.py --help` and `--version` both fail immediately with `ModuleNotFoundError: No module named 'gffutils'`.
- The second positional argument is a database path, not the converted GFF output path; converted records are printed to stdout.
- Source inspection shows it skips `ncRNA` feature groups and prints only `gene`, `transcript`, and `CDS` records.
- The script assumes attributes such as `Name` and `locus_tag`; mismatched GFF flavors can crash or assert instead of degrading gracefully.

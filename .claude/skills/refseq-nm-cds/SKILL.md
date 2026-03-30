---
name: refseq-nm-cds
description: Use when retrieving RefSeq NM coding sequences for supported species (cow, frog, human, mouse, pig, rat, zebrafish) via the entrez-direct toolkit.
disable-model-invocation: true
user-invocable: true
---

# refseq-nm-cds

Operational EDirect workflow for downloading RefSeq mRNA GenBank flatfiles by species and extracting NM_* CDS intervals/sequences into `<species>_cds.txt`.

## Quick Start

- **Command:** `refseq-nm-cds <species>`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/refseq-nm-cds`
- **Supported species/aliases:** `human|man`, `mouse|mice`, `rat`, `pig`, `cow`, `frog`, `fish|zebrafish`, or `all`

## When To Use This Tool

Retrieving NCBI RefSeq NM (mRNA) coding sequences for model organisms. Accepts species name as the sole argument and outputs CDS records. Installed as part of the bioconda `entrez-direct` package.

## Common Patterns

```bash
# 1) Download and process the default human set
refseq-nm-cds human
```

```bash
# 2) Use an accepted alias
refseq-nm-cds man
refseq-nm-cds zebrafish
```

```bash
# 3) Process all supported species
refseq-nm-cds all
```

## Recommended Workflow

1. Pick one species first to estimate runtime, disk growth, and network behavior.
2. Let the script finish both its download and processing phases.
3. Collect the resulting `<species>_cds.txt` files and inspect a few rows before downstream use.
4. Only then scale out to `all` if you really need every supported species.

## Guardrails

- This script is not a light query helper. By default it both downloads many `*.rna.gbff.gz` files and processes them.
- If no species is supplied, source inspection shows it defaults to `human`.
- Unsupported arguments such as `--help` or `--version` are treated as species names. In local testing that path also emitted a shell error from a stray `break` before printing the species warning.
- The workflow depends on many sibling tools being on `PATH`, including `nquire`, `skip-if-file-exists`, `gbf2xml`, and `xtract`.
- Output is written to files such as `human_cds.txt`, `mouse_cds.txt`, and `zebrafish_cds.txt`; it is not primarily a stdout-streaming tool.

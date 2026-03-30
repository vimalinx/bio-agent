---
name: download-ncbi-data
description: Use when downloading static NCBI reference datasets such as taxonomy, MeSH tree, bioconcepts, generif, journals, serials, or PMC open access files via CLI.
disable-model-invocation: true
user-invocable: true
---

# download-ncbi-data

## Quick Start
- **Command:** `download-ncbi-data <dataset> [extra-arg]`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/download-ncbi-data`
- **Full reference:** See `references/help.md`

## When To Use This Tool

- Download curated NCBI side datasets such as taxonomy tables, GeneRIF summaries, journal lists, MeSH resources, PMC OA bundles, or NIH Open Citation Collection files.
- Build local lookup tables without manually browsing NCBI FTP trees.
- Grab sample/demo payloads like `carotene`, `globin`, `human`, or `smear` for testing downstream EDirect tooling.

## Common Patterns

```bash
# 1) Download taxonomy name and lineage tables
download-ncbi-data taxnames
```

```bash
# 2) Build MeSH helper tables in the current directory
download-ncbi-data meshtree
```

```bash
# 3) Mirror PubMed journal metadata or the NIH Open Citation Collection
download-ncbi-data journals
download-ncbi-data nihocc
```

```bash
# 4) Download a specific OA book bundle after discovering its accession
download-ncbi-data oa-book NBKXXXXXX
```

## Recommended Workflow

1. Choose a dedicated output directory before running the command because many subcommands emit multiple derived files.
2. Pick the dataset subcommand deliberately: `taxnames`/`taxoninfo` for taxonomy, `meshtree` for MeSH, `serials`/`journals` for literature metadata, `pmc-oa` or `pmc-bioc` for large content bundles.
3. Let the script finish its side products, such as `taxnames.txt`, `lineages.txt`, `meshconv.xml`, `meshtree.txt`, or journal lookup tables.
4. Treat the generated files as reusable local resources for later pipelines instead of re-downloading them each run.

## Guardrails

- This tool writes into the current directory and may create several companion files in addition to the primary download.
- `oa-book` expects an accession argument after the subcommand; most other modes do not.
- Some options are real datasets, while `carotene`, `globin`, `human`, and `smear` are sample payloads meant for testing.
- The local script has no meaningful `--version` mode and depends heavily on live network access.
- In this local install, the `human` sample branch appears to contain a filename typo in the wrapper script, so verify that mode manually before depending on it.

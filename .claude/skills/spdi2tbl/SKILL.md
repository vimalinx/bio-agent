---
name: spdi2tbl
description: Use when flattening SPDI XML records into sorted, deduplicated tabular rows for downstream variant pipelines.
disable-model-invocation: true
user-invocable: true
---

# spdi2tbl

Tiny Bash wrapper around `xtract` plus a final `sort-table | cut | uniq` cleanup. It reads `<SPDI>` XML, emits variant rows with rsID, accession, position, deleted/inserted sequence, class, type, and gene, then sorts and deduplicates the result.

## Quick Start

- **Command:** `... | spdi2tbl`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/spdi2tbl`
- **Typical upstream:** `efetch -db snp ... | snp2hgvs | hgvs2spdi`

## When To Use This Tool

- Flattening SPDI XML into plain tabular rows
- Bridging from `hgvs2spdi` into shell-friendly TSV output
- Producing deduplicated variant tables for later ranking, filtering, or product-sequence generation
- Normalizing dbSNP-derived variant classes into a stable sort order

## Common Patterns

```bash
# Canonical dbSNP pipeline into a flat table
efetch -db snp -id 104894914 -format docsum | snp2hgvs | hgvs2spdi | spdi2tbl
```

```bash
# Save flattened SPDI rows for downstream use
some_spdi_xml_generator | spdi2tbl > variants.tsv
```

```bash
# Feed directly into tbl2prod
efetch -db snp -id 104894914 -format docsum | snp2hgvs | hgvs2spdi | spdi2tbl | tbl2prod
```

## Recommended Workflow

1. Generate real `<SPDI>` XML upstream, typically from `hgvs2spdi`.
2. Pipe the XML into `spdi2tbl`.
3. Inspect the resulting 8-column rows before using them downstream.
4. Chain into `tbl2prod` or other shell filters only after confirming the accession/class mix is what you expect.

## Guardrails

- There is no safe local help/version path: both `-h` and `--version` fell through to `xtract` and failed with `No data supplied to xtract from stdin or file`.
- Source inspection shows the class ordering is explicitly transformed as `Genomic=1`, `Coding=2`, `Protein=3` before sorting.
- The wrapper depends on `sort-table` being available on `PATH`.
- In live testing on rs104894914, the output rows looked like `rs104894914  NC_000023.11  154191715  T  C  Genomic  Substitution  OPN1MW`.
- Final output is deduplicated with `uniq` after sorting, so repeated equivalent rows are collapsed silently.

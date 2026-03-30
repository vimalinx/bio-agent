---
name: extract-splice-sites-py
description: Use when extracting splice junction sites from GTF annotation files for HISAT2 genome indexing or RNA-seq alignment workflows.
disable-model-invocation: true
user-invocable: true
---

# extract-splice-sites-py

## Quick Start

- **Command:** `extract_splice_sites.py [gtf_file]`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/extract_splice_sites.py`
- **Full reference:** See `references/help.md`

## When To Use This Tool

- Extract unique splice junction coordinates from a GTF annotation.
- Prepare splice-site lists for HISAT2 index building and splice-aware alignment workflows.
- Summarize transcript exon structures into one junction set per genome annotation.

## Common Patterns

```bash
# 1) Extract splice junctions from a GTF file
extract_splice_sites.py genes.gtf > splice_sites.tsv
```

```bash
# 2) Stream a compressed GTF through stdin
zcat genes.gtf.gz | extract_splice_sites.py - > splice_sites.tsv
```

```bash
# 3) Emit junctions and summary statistics together
extract_splice_sites.py -v genes.gtf > splice_sites.tsv
```

## Recommended Workflow

1. Prepare a valid GTF annotation file for your reference genome.
2. Run `extract_splice_sites.py [gtf_file]` to extract splice sites (use `-` to read from stdin).
3. Add `-v` flag if you want statistics printed to stderr.
4. Use output as input for HISAT2 index building.

## Guardrails

- Input must be a GTF file; other formats are not supported.
- Use `-` as the gtf_file argument when piping via stdin.
- No `--version` flag available; check installation via bioconda/hisat2 package.
- Output coordinates are zero-based donor/acceptor boundaries (`left-1`, `right-1`) plus strand.
- Exons separated by 5 bp or less are merged before junction extraction, so tiny gaps do not become splice sites.
- With `-v`, the script prints transcript/exon/intron summary statistics to stderr while still writing splice sites to stdout.

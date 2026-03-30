---
name: extract-exons-py
description: Use when extracting exon coordinates from GTF annotation files for HISAT2 index building or transcriptome analysis.
disable-model-invocation: true
user-invocable: true
---

# extract-exons-py

## Quick Start

- **Command**: `extract_exons.py [gtf_file]`
- **Local executable**: `/home/vimalinx/miniforge3/envs/bio/bin/extract_exons.py`
- **Full reference**: See [references/help.md](references/help.md)

## When To Use This Tool

- Extract nonredundant exon intervals from a GTF annotation.
- Prepare exon lists for HISAT2 index building or transcriptome-aware downstream tooling.
- Collapse transcript-specific exon redundancy into a unique coordinate set.

## Common Patterns

```bash
# 1) Extract exons from a GTF file
extract_exons.py genes.gtf > exons.tsv
```

```bash
# 2) Stream a GTF through stdin
zcat genes.gtf.gz | extract_exons.py - > exons.tsv
```

```bash
# 3) Inspect the first zero-based exon intervals
extract_exons.py genes.gtf | sed -n '1,20p'
```

## Recommended Workflow

1. Obtain a valid GTF annotation file for your reference genome
2. Run `extract_exons.py gtf_file` to extract exon coordinates (use `-` for stdin)
3. Add `-v` flag to print statistics to stderr for validation
4. Use output as input for downstream HISAT2 index building workflows

## Guardrails

- Input must be a valid GTF file or `-` for stdin
- Verify GTF format compatibility before processing large files
- Review stderr output when using verbose mode to validate extraction statistics
- Output coordinates are zero-based (`left-1`, `right-1`) and include strand as the fourth column.
- Adjacent exons separated by 5 bp or less are merged before output, so the result is not a raw exon-by-exon dump from the source GTF.
- `--help` works, but `--version` is not implemented and exits with an argparse error.

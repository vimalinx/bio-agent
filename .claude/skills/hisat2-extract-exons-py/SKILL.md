---
name: hisat2-extract-exons-py
description: Use when extracting exon coordinates from GTF annotation files for HISAT2 index building or splice-aware alignment preparation.
disable-model-invocation: true
user-invocable: true
---

# hisat2-extract-exons-py

## Quick Start

- **Command**: `hisat2_extract_exons.py [gtf_file]`
- **Local executable**: `/home/vimalinx/miniforge3/envs/bio/bin/hisat2_extract_exons.py`
- **Full reference**: See `references/help.md`

## When To Use This Tool

- Use `hisat2_extract_exons.py` when you need exon coordinates from a GTF to feed into HISAT2 graph/index construction.
- It is the appropriate companion script for generating the `--exon` input consumed by `hisat2-build`.
- Use it when your annotation source is GTF and you want a lightweight extractor rather than a general-purpose annotation parser.
- It also works in streaming workflows because `-` can be used to read the GTF from stdin.

## Common Patterns

```bash
# Extract exons from a GTF annotation file
hisat2_extract_exons.py annotation.gtf > exons.txt

# Emit progress/statistics to stderr while writing exon coordinates to stdout
hisat2_extract_exons.py -v annotation.gtf > exons.txt

# Stream a compressed GTF through stdin
gzip -cd annotation.gtf.gz | hisat2_extract_exons.py - > exons.txt

# Use the result during HISAT2 index building
hisat2-build-s genome.fa genome --exon exons.txt
```

## Recommended Workflow

1. Prepare or obtain a valid GTF annotation file for your reference genome
2. Run `hisat2_extract_exons.py annotation.gtf > exons.txt` to extract exon coordinates
3. Add the `-v` flag to print extraction statistics to stderr if needed
4. Use the output file in downstream HISAT2 index building or alignment steps

## Guardrails

- Input must be a valid GTF file; other annotation formats are not supported
- Use `-` as the gtf_file argument to read from stdin rather than shell piping alone
- Redirect stdout explicitly to save output; statistics with `-v` go to stderr
- This helper does not implement `--version`; use `-h/--help` for a quick installation check

---
name: hisat2-extract-splice-sites-py
description: Use when extracting splice junctions from GTF annotation files for HISAT2 splice-aware alignment.
disable-model-invocation: true
user-invocable: true
---

# hisat2-extract-splice-sites-py

## Quick Start
- Command: `hisat2_extract_splice_sites.py [gtf_file]`
- Local executable: `/home/vimalinx/miniforge3/envs/bio/bin/hisat2_extract_splice_sites.py`
- Reference: [references/help.md](references/help.md)

## When To Use This Tool

- Use `hisat2_extract_splice_sites.py` when you need known splice junctions from a GTF for splice-aware HISAT2 workflows.
- It is the canonical helper for generating the file consumed by `hisat2-build --ss` or by aligners via `--known-splicesite-infile`.
- Use it when you want a minimal extractor focused on splice junction coordinates rather than a general annotation conversion tool.
- It also supports streaming input via `-`, so it fits compressed or piped annotation workflows.

## Common Patterns

```bash
# Extract splice junctions from a GTF file
hisat2_extract_splice_sites.py annotation.gtf > splicesites.txt

# Print progress/statistics to stderr
hisat2_extract_splice_sites.py -v annotation.gtf > splicesites.txt

# Stream a compressed GTF via stdin
gzip -cd annotation.gtf.gz | hisat2_extract_splice_sites.py - > splicesites.txt

# Reuse the result during HISAT2 index building
hisat2-build-s genome.fa genome --ss splicesites.txt
```

## Recommended Workflow
1. Obtain a valid GTF annotation file for your reference organism
2. Run `hisat2_extract_splice_sites.py annotation.gtf > splice_sites.txt`
3. Pass the output file to HISAT2 index building via `--ss` option
4. Add `-v` flag if you want diagnostic statistics printed to stderr

## Guardrails
- Input must be a valid GTF file or "-" to read from stdin
- Output writes to stdout; redirect to a file to save results
- Use `-v` only when you want progress/statistics reported to stderr
- This helper does not implement `--version`; use `-h/--help` for availability checks

---
name: fasterq-dump
description: Use when extracting FASTQ or FASTA files from NCBI SRA run accessions, especially after staging runs locally with prefetch.
disable-model-invocation: true
user-invocable: true
---

# fasterq-dump

## Quick Start
- **Command:** `fasterq-dump`
- **Local executable:** Not installed in this workspace
- **Full reference:** See `references/help.md`

## When To Use This Tool

- Convert an SRA run accession into FASTQ files for alignment, QC, or assembly.
- Prefer this over legacy `fastq-dump` for large public SRA runs when you have enough scratch space.
- Use it after `prefetch` when you want conversion to read from a local accession cache instead of streaming from NCBI.

## Common Patterns

```bash
# 1) Convert a run accession into paired FASTQ files in a dedicated output directory
fasterq-dump SRR000001 --split-files -e 8 -O fastq -t /scratch
```

```bash
# 2) Best practice for larger runs: prefetch first, then convert from the local accession directory
prefetch SRR000001
fasterq-dump ~/ncbi/public/sra/SRR000001 --split-files -e 8 -O fastq -t /scratch
```

```bash
# 3) Stream a single split-spot FASTQ to stdout for ad hoc processing
fasterq-dump SRR000001 --split-spot -Z | gzip > SRR000001.fastq.gz
```

## Recommended Workflow

1. Resolve the exact run accession and, for large jobs, download it locally with `prefetch` first.
2. Set an output directory with `-O` and a roomy scratch directory with `-t`, ideally on different filesystems.
3. Pick the output mode deliberately: `--split-files` for paired-end files, `--split-spot` for a single stream, or `--fasta-unsorted` when FASTA is enough.
4. Validate the resulting FASTQ filenames and sizes, then compress afterward with `gzip` or `pigz` if needed.

## Guardrails

- This tool is not installed locally right now, so these patterns are based on upstream SRA Toolkit behavior rather than a live binary in this workspace.
- `fasterq-dump` takes one accession at a time and writes output into the current directory unless `-O` is supplied.
- The tool also creates a temporary `fasterq.tmp.*` directory and can require very large scratch space, with worst-case usage on the order of multiple times the final FASTQ size.
- `--stdout` does not work with the default split-3 behavior or with `--split-files`; use `--split-spot` or another single-stream mode when redirecting output.
- There is no built-in gzip output mode; compress files explicitly after conversion.

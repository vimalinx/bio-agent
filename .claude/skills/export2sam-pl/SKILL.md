---
name: export2sam-pl
description: Use when converting legacy Illumina GERALD export files into SAM for downstream alignment analysis.
disable-model-invocation: true
user-invocable: true
---

# export2sam-pl

## Quick Start

- **Command:** `export2sam.pl --read1=lane1_export.txt [options] > alignments.sam`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/export2sam.pl`
- **Reference:** See [references/help.md](references/help.md)

## When To Use This Tool

- Convert Illumina GERALD / CASAVA export files into standard SAM.
- Handle single-end or paired-end export files with `--read1` and optional `--read2`.
- Keep failed-purity-filter reads with `--nofilter` when you need full raw export coverage.
- Interpret older Solexa log-odds qualities correctly with `--qlogodds`.

## Common Patterns

```bash
# 1) Convert a single-end export file
export2sam.pl \
  --read1=s_1_export.txt > alignments.sam
```

```bash
# 2) Convert paired-end export files
export2sam.pl \
  --read1=s_1_1_export.txt \
  --read2=s_1_2_export.txt > paired.sam
```

```bash
# 3) Include failed-filter reads and interpret old log-odds qualities
export2sam.pl \
  --read1=s_1_export.txt.gz \
  --nofilter \
  --qlogodds > legacy.sam
```

## Recommended Workflow

1. Confirm the inputs are GERALD export files and not FASTQ, ELAND, or ordinary SAM.
2. Supply `--read1` first, then add `--read2` only when the files form a true read pair.
3. Decide whether the run predates OLB/Pipeline 1.3; only then enable `--qlogodds`.
4. Convert, then inspect flags and optional fields before folding the output into later BAM-based steps.

## Guardrails

- `--read1` is mandatory; this script does not do anything useful without it.
- `--nofilter` changes the dataset by retaining reads that failed the basecaller purity filter; those reads are marked with SAM flag `0x0200`.
- `--qlogodds` is only for old Solexa-style export qualities; do not enable it on newer phred-style exports.
- Gzipped inputs are supported via `.gz`, and `-` can be used for stdin input, but this is still a legacy GERALD-specific converter rather than a general FASTQ-to-SAM tool.

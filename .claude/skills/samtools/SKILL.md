---
name: samtools
description: Use when working with SAM, BAM, or CRAM alignment files to sort, index, view, convert, or compute statistics.
disable-model-invocation: true
user-invocable: true
---

# samtools

## Quick Start
- **Command:** `samtools`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/samtools`
- **Version:** 1.22.1
- **Reference:** See `references/help.md` for full command documentation and options

## When To Use This Tool

- Inspect, convert, sort, index, and summarize SAM/BAM/CRAM files.
- It is the default plumbing tool around almost every alignment workflow.
- Use it immediately after aligners and before most downstream coverage or variant workflows.
- Prefer subcommand-oriented usage; `samtools` is a dispatcher, not a single operation.

## Common Patterns

```bash
# 1) Convert SAM to BAM
samtools view -b -o sample.bam sample.sam
```

```bash
# 2) Sort and index a BAM
samtools sort -@ 8 -o sample.sorted.bam sample.bam
samtools index sample.sorted.bam
```

```bash
# 3) Inspect basic mapping statistics
samtools flagstat sample.sorted.bam
samtools stats sample.sorted.bam > sample.stats.txt
```

```bash
# 4) Extract one region
samtools view sample.sorted.bam chr1:100000-110000
```

## Recommended Workflow

1. Convert aligner output into BAM or CRAM as needed.
2. Sort the file before indexing or region-based access.
3. Run `flagstat`, `stats`, `coverage`, or `depth` to sanity-check the alignment.
4. Use specialized subcommands like `fastq`, `fasta`, `faidx`, or `dict` only when the workflow specifically needs them.

## Guardrails

- Region-based operations require sorted and indexed files.
- `samtools quickcheck` is a cheap integrity test before burning compute on a broken BAM/CRAM.
- Use `-@` for thread-aware subcommands, but do not assume every subcommand parallelizes the same way.
- Be explicit about output format and destination; many subcommands default to stdout.

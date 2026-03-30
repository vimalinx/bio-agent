---
name: bam-to-fastq
description: Use when converting BAM alignment files to FASTQ format, including paired-end data requiring separate or interleaved output.
disable-model-invocation: true
user-invocable: true
---

# bam-to-fastq

## Quick Start
- **Command:** `bamToFastq -i input.bam -fq reads.fq [options]`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/bamToFastq`
- **Full reference:** See `references/help.md`

## When To Use This Tool

- Recover FASTQ from BAM alignments for remapping, QC, or archival export.
- Split paired-end BAM into `R1` and `R2` FASTQ files with `-fq` and `-fq2`.
- Emit a single interleaved FASTQ stream by directing both mates to stdout.
- Reconstruct reads from mate tags with `-tags` when the BAM carries `R2` / `Q2` tags.

## Common Patterns

```bash
# 1) Single-end BAM to FASTQ
bamToFastq \
  -i reads.bam \
  -fq reads.fq
```

```bash
# 2) Paired-end BAM to two FASTQ files
bamToFastq \
  -i reads.qname.bam \
  -fq reads_R1.fq \
  -fq2 reads_R2.fq
```

```bash
# 3) Interleaved paired-end FASTQ
bamToFastq \
  -i reads.qname.bam \
  -fq /dev/stdout \
  -fq2 /dev/stdout > reads.interleaved.fq
```

## Recommended Workflow

1. Decide whether the BAM is single-end, paired-end, or tag-based (`-tags`) before selecting output mode.
2. For paired-end export, query-name sort or collate the BAM first so mates stay synchronized.
3. Write to fresh FASTQ files and validate mate counts if the output will feed a new aligner.
4. If you need more filtering and flag control, compare against `samtools fastq` before standardizing the pipeline.

## Guardrails

- `-i` and `-fq` are required.
- Paired-end export with `-fq2` assumes the BAM is grouped or sorted by query name.
- `-tags` is specialized behavior for BAMs that carry mate sequence / quality in `R2` and `Q2`; it is not a generic paired-end fix.
- The interleaved `/dev/stdout` pattern is convenient but easy to misuse in shells and pipelines, so redirect carefully.
- Prefer `-h` for help; the wrapper does not support clean GNU-style `--help` / `--version`.

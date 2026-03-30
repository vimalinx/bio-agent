---
name: bed-to-bam
description: Use when converting BED/GFF/VCF feature records to BAM format for visualization or downstream analysis.
disable-model-invocation: true
user-invocable: true
---

# bed-to-bam

## Quick Start
- **Command:** `bedToBam -i intervals.bed -g genome.txt [options] > output.bam`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/bedToBam`
- **Full reference:** See `references/help.md`

## When To Use This Tool

- Convert interval-like features into BAM for browser display or BAM-based tooling.
- Emit BAM records with a chosen mapping quality.
- Preserve BED12 block structure as BAM CIGAR operations.
- Produce compressed or uncompressed BAM output for downstream integration.

## Common Patterns

```bash
# 1) Convert BED to BAM
bedToBam \
  -i peaks.bed \
  -g genome.txt > peaks.bam
```

```bash
# 2) Set a custom mapping quality
bedToBam \
  -i peaks.bed \
  -g genome.txt \
  -mapq 60 > peaks.mapq60.bam
```

```bash
# 3) Preserve BED12 blocks in CIGAR strings
bedToBam \
  -i transcripts.bed12 \
  -g genome.txt \
  -bed12 > transcripts.bam
```

## Recommended Workflow

1. Build a correct genome file matching the interval coordinate system.
2. Confirm BED inputs are at least BED4 if you expect robust BAM conversion.
3. Add `-bed12` only for true BED12 input where block-aware CIGAR is desired.
4. Validate the BAM with `samtools view` or a genome browser before relying on it downstream.

## Guardrails

- `-i` and `-g` are required.
- BED input should be BED4 or higher because the BAM record needs a name field.
- `-bed12` assumes BED12 semantics; using it on non-BED12 input gives misleading BAM structure.
- Default mapping quality is `255`, which is a placeholder-like value rather than an empirical alignment score.
- Prefer `-h` for help; GNU-style `--help` / `--version` calls on these wrappers are noisy.

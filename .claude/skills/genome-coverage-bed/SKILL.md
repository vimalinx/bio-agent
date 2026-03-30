---
name: genome-coverage-bed
description: Use when computing genome-wide coverage from BED/GFF/VCF or BAM files, generating coverage histograms, BedGraph tracks, or per-position depth reports.
disable-model-invocation: true
user-invocable: true
---

# genome-coverage-bed

## Quick Start
- **Command:** `genomeCoverageBed -i features.bed -g genome.txt [options]` or `genomeCoverageBed -ibam reads.bam [options]`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/genomeCoverageBed`
- **Full reference:** See `references/help.md`

## When To Use This Tool

- Compute genome-wide coverage histograms from interval or BAM input.
- Generate BedGraph tracks with `-bg` or `-bga` for browser visualization.
- Emit per-base depth with `-d` or sparse zero-based depth with `-dz`.
- Normalize coverage by scale factor, strand, fragment model, or split alignment behavior.

## Common Patterns

```bash
# 1) Default genome-wide histogram from BED intervals
genomeCoverageBed \
  -i reads.bed \
  -g genome.txt
```

```bash
# 2) BedGraph including zero-coverage intervals
genomeCoverageBed \
  -ibam reads.sorted.bam \
  -bga > coverage.bedgraph
```

```bash
# 3) Zero-based depth for non-zero positions only
genomeCoverageBed \
  -ibam reads.sorted.bam \
  -dz
```

## Recommended Workflow

1. Choose the reporting mode first: histogram (`default`), BedGraph (`-bg` / `-bga`), or depth (`-d` / `-dz`).
2. For BED-like input, provide a valid genome file; for BAM input, position-sort the BAM before running coverage.
3. Use `-split` when spliced or blocked intervals should contribute as separate covered blocks.
4. Add `-scale`, `-strand`, `-pc`, `-5`, or `-3` only when the biological interpretation of coverage depends on those choices.

## Guardrails

- `-g` is required unless you use `-ibam`.
- BAM input must be position-sorted; BED input must be grouped by chromosome.
- `-bga` includes zero-coverage intervals, whereas `-bg` omits them.
- `-d` is one-based and reports every genomic position; `-dz` is zero-based and reports only non-zero positions.
- `-trackline` is convenient for browser upload, but that first line must be removed before BedGraph-to-BigWig conversion.

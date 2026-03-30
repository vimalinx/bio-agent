---
name: coverage-bed
description: Use when computing coverage depth and breadth of features from one interval file overlapping intervals in another. Applies to BED, GFF, or VCF inputs requiring overlap counts, covered bases, and coverage fractions.
disable-model-invocation: true
user-invocable: true
---

# coverage-bed

## Quick Start
- **Command:** `coverageBed -a targets.bed -b features.bed [options]`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/coverageBed`
- **Full reference:** See `references/help.md`

## When To Use This Tool

- Measure how much of each A interval is covered by features in B.
- Report per-interval overlap count, covered bases, and coverage fraction.
- Emit mean depth, histograms, or per-position depth over A intervals.
- Add strand-aware and overlap-fraction constraints before summarizing coverage.

## Common Patterns

```bash
# 1) Default per-interval coverage summary
coverageBed \
  -a exons.bed \
  -b reads.bed
```

```bash
# 2) Report mean depth per target interval
coverageBed \
  -a exons.bed \
  -b reads.bed \
  -mean
```

```bash
# 3) Emit a coverage histogram per interval
coverageBed \
  -a exons.bed \
  -b reads.bed \
  -hist
```

## Recommended Workflow

1. Decide whether you need the default summary, `-counts`, `-mean`, `-hist`, or per-position `-d` output before wiring this into a pipeline.
2. Treat A as the reporting frame: every result is anchored to intervals in A, not B.
3. Add `-s` / `-S`, `-f` / `-F`, `-r`, or `-e` only when you mean to constrain which B overlaps count toward coverage.
4. Use `-sorted` plus `-g` for large sorted files when performance matters.

## Guardrails

- Both `-a` and `-b` are required.
- The default output appends four fields to each A record: overlap count, covered bases in A, A length, and covered fraction.
- `-d` reports one-based positions after each full A record, which changes the output shape substantially.
- `-hist` emits per-feature histograms plus a global summary histogram, so downstream parsers must be histogram-aware.
- Prefer `-h` for help; GNU-style `--help` / `--version` calls on these wrappers are noisy.

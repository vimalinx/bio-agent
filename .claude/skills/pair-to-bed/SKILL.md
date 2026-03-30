---
name: pair-to-bed
description: Use when you need to find overlaps between paired-end read intervals (BEDPE or BAM) and genomic features in BED, GFF, or VCF format.
disable-model-invocation: true
user-invocable: true
---

# pair-to-bed

## Quick Start
- **Command:** `pairToBed -a pairs.bedpe -b features.bed [options]`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/pairToBed`
- **Full reference:** See `references/help.md`

## When To Use This Tool

- Test whether paired-end intervals overlap annotation features.
- Filter BEDPE pairs by logic such as `either`, `both`, `xor`, `neither`, or `notboth`.
- Evaluate span-based overlap using the inner span (`ispan`) or outer span (`ospan`) of a pair.
- Work directly from BAM pairs with `-abam` when you have not materialized BEDPE.

## Common Patterns

```bash
# 1) Report pairs where either end overlaps a feature
pairToBed \
  -a pairs.bedpe \
  -b peaks.bed \
  -type either
```

```bash
# 2) Keep only pairs where both ends overlap annotation
pairToBed \
  -a pairs.bedpe \
  -b exons.bed \
  -type both
```

```bash
# 3) Test whether the outer span of each pair overlaps a region set
pairToBed \
  -a pairs.bedpe \
  -b blacklist.bed \
  -type ospan
```

## Recommended Workflow

1. Decide whether the biology is about pair ends separately (`either`, `both`, `xor`) or about the fragment span (`ispan`, `ospan`).
2. Use BEDPE if you already have pair geometry extracted; otherwise consider `-abam` with query-grouped BAM input.
3. Add `-f` only when a minimal fractional overlap is biologically justified.
4. Apply strand constraints only for end-wise overlap modes where strand meaningfully applies.

## Guardrails

- `-a` or `-abam` plus `-b` is required.
- `-abam` requires BAM grouped or sorted by query name.
- `ispan`, `ospan`, `notispan`, and `notospan` ignore records whose mates are on different chromosomes.
- `-s` and `-S` do not apply to `ispan` / `ospan` modes.
- With BAM input, the default output stays BAM unless you request `-bedpe` or `-ubam`.

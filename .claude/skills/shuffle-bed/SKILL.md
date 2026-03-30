---
name: shuffle-bed
description: Use when you need to randomly permute feature locations across a genome for statistical testing or generating null distributions.
disable-model-invocation: true
user-invocable: true
---

# shuffle-bed

## Quick Start
- **Command:** `shuffleBed -i intervals.bed -g genome.txt [options]`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/shuffleBed`
- **Full reference:** See `references/help.md`

## When To Use This Tool

- Randomize interval locations to build null models for enrichment or overlap testing.
- Preserve original interval lengths while relocating them within a genome.
- Restrict random placement with inclusion or exclusion masks.
- Keep intervals on the same chromosome or enforce non-overlap among shuffled results.

## Common Patterns

```bash
# 1) Basic genome-wide shuffle
shuffleBed \
  -i peaks.bed \
  -g genome.txt > peaks.shuffled.bed
```

```bash
# 2) Reproducible same-chromosome shuffle excluding blacklist regions
shuffleBed \
  -i peaks.bed \
  -g genome.txt \
  -chrom \
  -excl blacklist.bed \
  -seed 42 > peaks.shuffled.bed
```

```bash
# 3) Shuffle only within allowed regions
shuffleBed \
  -i peaks.bed \
  -g genome.txt \
  -incl accessible_regions.bed \
  -maxTries 10000
```

## Recommended Workflow

1. Decide whether the null model should preserve chromosome identity (`-chrom`) or allow genome-wide relocation.
2. Add `-seed` whenever the shuffled set must be reproducible.
3. Use `-incl`, `-excl`, `-noOverlapping`, and `-maxTries` to match the biological constraints of the null model.
4. Check that the shuffled output preserved record count and interval length distribution before using it for inference.

## Guardrails

- `-i` and `-g` are required.
- `-incl` disables `-chromFirst`.
- `-f` can be used with `-excl` but not with `-incl`.
- `-chrom` forces same-chromosome placement and also forces `-chromFirst`.
- `-allowBeyondChromEnd` changes the interval-length preservation rule near chromosome ends, so only use it intentionally.

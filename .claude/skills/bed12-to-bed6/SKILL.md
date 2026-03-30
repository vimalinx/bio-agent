---
name: bed12-to-bed6
description: Use when you need to explode BED12 transcript or block annotations into one BED6 interval per block, such as converting multi-exon records into simple exon intervals for downstream interval analysis.
disable-model-invocation: true
user-invocable: true
---

# bed12-to-bed6

## Quick Start
- **Command:** `bed12ToBed6 -i transcripts.bed12 [options]`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/bed12ToBed6`
- **Full reference:** See `references/help.md`

## When To Use This Tool

- Split BED12 transcript or gene models into one BED6 record per block.
- Convert exon-style annotations into simple intervals for downstream `intersect`, `coverage`, or `map` workflows.
- Preserve block order in the score column with `-n` when downstream code needs exon numbering.
- Simplify BED12 inputs before using tools that only expect BED3/BED6-style intervals.

## Common Patterns

```bash
# 1) Expand BED12 transcripts into BED6 exon intervals
bed12ToBed6 \
  -i transcripts.bed12 \
  > exons.bed
```

```bash
# 2) Write the 1-based block number into the BED score column
bed12ToBed6 \
  -i transcripts.bed12 \
  -n \
  > exons-numbered.bed
```

## Recommended Workflow

1. Confirm the input is true BED12 with consistent `blockCount`, `blockSizes`, and `blockStarts` fields.
2. Decide whether the BED score should stay as the original score or be overwritten with the 1-based block number via `-n`.
3. Run the conversion and redirect to a new BED6 file for downstream interval work.
4. Spot-check that the output record count matches the total number of blocks you expected from the source annotation.

## Guardrails

- Each BED12 block becomes its own BED6 record; the original block arrays are consumed and not carried forward.
- `-n` overwrites the BED score field, so do not use it if the original score must be preserved.
- Invalid BED12 rows can silently produce misleading output; validate block counts and array lengths upstream.
- Prefer `-h` for help; GNU-style `--help` and `--version` emit wrapper errors before showing usage text.

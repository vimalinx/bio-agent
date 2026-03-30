---
name: window-maker
description: Use when you need to create adjacent or sliding windows across a genome or BED file for binning genomic regions into fixed-size or fixed-count intervals.
disable-model-invocation: true
user-invocable: true
---

# window-maker

## Quick Start
- **Command:** `windowMaker [-g genome.txt | -b intervals.bed] [-w size | -n count] [options]`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/windowMaker`
- **Full reference:** See `references/help.md`

## When To Use This Tool

- Tile a genome or interval set into fixed-width windows.
- Create sliding windows by combining `-w` with `-s`.
- Split each source interval into a fixed number of windows with `-n`.
- Add window identifiers for downstream joins, coverage summaries, or matrix construction.

## Common Patterns

```bash
# 1) Make non-overlapping 1 Mb genome windows
windowMaker \
  -g genome.txt \
  -w 1000000
```

```bash
# 2) Make sliding 10 kb windows with 5 kb step
windowMaker \
  -g genome.txt \
  -w 10000 \
  -s 5000
```

```bash
# 3) Split each BED interval into 20 windows and label by window number
windowMaker \
  -b regions.bed \
  -n 20 \
  -i winnum
```

## Recommended Workflow

1. Choose the source domain first: whole-genome tiling with `-g` or per-interval tiling with `-b`.
2. Choose fixed width (`-w`) versus fixed count (`-n`) based on the downstream statistical design.
3. Add `-s` only when you intentionally want overlapping sliding windows.
4. Use `-i` and optionally `-reverse` when downstream tools need stable window IDs rather than anonymous coordinates.

## Guardrails

- You must provide one interval source: `-g` or `-b`.
- You must provide one windowing mode: `-w` or `-n`.
- `-s` is meaningful with `-w` window-size mode, not as a replacement for `-n`.
- The genome file is tab-delimited chromosome name plus size; a FASTA `.fai` works because bedtools reads only the first two columns.
- Prefer `-h` for help; GNU-style `--version` on this wrapper emits errors before exiting.

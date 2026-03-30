---
name: union-bed-graphs
description: Use when you need to align multiple bedGraph tracks onto a shared interval segmentation so their values can be compared side by side.
disable-model-invocation: true
user-invocable: true
---

# union-bed-graphs

## Quick Start
- **Command**: `unionBedGraphs -i sample1.bg sample2.bg [options]`
- **Local executable**: `/home/vimalinx/miniforge3/envs/bio/bin/unionBedGraphs`
- **Full reference**: See `references/help.md`

## When To Use This Tool

- Combine multiple bedGraph tracks into one interval-by-track matrix.
- Compare per-region coverage or signal values across replicates, conditions, or assays.
- Emit explicit empty intervals across a genome with `-empty` plus `-g`.
- Add headers and custom sample names for downstream plotting or statistics.

## Common Patterns

```bash
# 1) Merge two bedGraph tracks onto shared intervals
unionBedGraphs \
  -i tumor.bg normal.bg \
  > tumor-normal.union.bg
```

```bash
# 2) Add a header with explicit sample names
unionBedGraphs \
  -i rep1.bg rep2.bg rep3.bg \
  -header \
  -names WT1 WT2 KO1 \
  > signal-matrix.tsv
```

```bash
# 3) Include empty genomic regions and use a custom missing-value filler
unionBedGraphs \
  -i sample1.bg sample2.bg \
  -g genome.sizes \
  -empty \
  -filler N/A \
  -header \
  > signal-with-gaps.tsv
```

## Recommended Workflow

1. Ensure every input bedGraph is sorted by chromosome/start and contains non-overlapping intervals within each file.
2. Decide whether you want a plain numeric matrix, a labeled header via `-header` / `-names`, or explicit empty regions via `-empty -g`.
3. Choose the missing-value representation with `-filler` so downstream code does not confuse absent signal with a real zero unless that is intended.
4. Import the resulting unioned matrix into downstream QC, visualization, or statistical comparison workflows.

## Guardrails

- `-i` is required and must be followed by one or more bedGraph files.
- Each input bedGraph must already be sorted by `chrom,start` and must not contain overlapping intervals within the same file.
- `-empty` requires `-g` so bedtools knows the chromosome extents.
- `-names` should provide one name per input file.
- Default filler text is `0`; use `-filler` if a literal zero would be biologically misleading in your downstream analysis.
- Prefer `-h` or `-examples` for help; GNU-style `--help` and `--version` without `-i` only complain about missing input files.

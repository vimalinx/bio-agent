---
name: get-overlap
description: Use when you need to append the overlap size or gap distance between two intervals that already appear on the same line, such as paired output from `bedtools window`.
disable-model-invocation: true
user-invocable: true
---

# get-overlap

## Quick Start
- **Command**: `getOverlap -i <input> -cols start1,end1,start2,end2`
- **Local executable**: `/home/vimalinx/miniforge3/envs/bio/bin/getOverlap`
- **Full reference**: See [references/help.md](references/help.md)

## When To Use This Tool

- Quantify how much two intervals overlap after another tool has already paired them on the same row.
- Turn `bedtools window`-style output into a table with a final numeric overlap or distance column.
- Score candidate interval pairs before thresholding or ranking them downstream.
- Add a simple overlap metric without rerunning a full interval join.

## Common Patterns

```bash
# 1) Measure overlap or gap after bedtools window
windowBed \
  -a A.bed \
  -b B.bed \
  -w 10 \
  | getOverlap -i stdin -cols 2,3,6,7
```

```bash
# 2) Append overlap to a precomputed paired table
getOverlap \
  -i paired-intervals.tsv \
  -cols 2,3,6,7
```

## Recommended Workflow

1. Generate or prepare a table where each row already contains the two intervals you want to compare.
2. Determine the exact 1-based column numbers for `start1,end1,start2,end2` in that table.
3. Run `getOverlap` on the file or use the literal input name `stdin` when streaming from a pipe.
4. Interpret the appended value before downstream filtering: positive means overlap, negative means separation, and zero means the intervals touch without overlapping.

## Guardrails

- `-cols` must be given in the exact order `start1,end1,start2,end2`; swapping them changes the result.
- This tool does not pair records for you; it only computes a metric from coordinates already present on the same line.
- Use the literal token `stdin` with `-i` when piping from another command.
- Prefer `-h` for help; GNU-style `--help` and `--version` emit wrapper errors before usage text.

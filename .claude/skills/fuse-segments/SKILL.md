---
name: fuse-segments
description: Use when you need to merge simple tabular start/end segments into non-overlapping intervals inside EDirect-style pipelines.
disable-model-invocation: true
user-invocable: true
---

# fuse-segments

## Quick Start

- **Command:** `printf '10\t20\tx\n18\t25\ty\n40\t35\tz\n' | PATH=/home/vimalinx/miniforge3/envs/bio/bin:$PATH /home/vimalinx/miniforge3/envs/bio/bin/fuse-segments`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/fuse-segments`
- **Full reference:** See [references/help.md](references/help.md) for complete documentation

## When To Use This Tool

- Normalize start / end pairs where coordinates may be reversed.
- Merge overlapping or directly adjacent segments into larger blocks.
- Compute merged interval length as a final third column for downstream reporting.

## Common Patterns

```bash
# 1) Fuse simple segments from a tab-delimited stream
printf '10\t20\tx\n18\t25\ty\n40\t35\tz\n' | \
  PATH=/home/vimalinx/miniforge3/envs/bio/bin:$PATH \
  /home/vimalinx/miniforge3/envs/bio/bin/fuse-segments
```

```text
10  25  16
35  40  6
```

```bash
# 2) Use as a cleanup step after generating interval tables elsewhere
upstream_command | \
  PATH=/home/vimalinx/miniforge3/envs/bio/bin:$PATH \
  /home/vimalinx/miniforge3/envs/bio/bin/fuse-segments \
  > fused_segments.tsv
```

## Recommended Workflow

1. Prepare a table whose first two columns are integer segment bounds.
2. Put the EDirect bin directory on `PATH` so `sort-table` can be resolved.
3. Pipe the segment table through `fuse-segments` and capture the merged output.
4. Confirm that reversed coordinates were normalized and that adjacent segments were intentionally collapsed.

## Guardrails

- This wrapper requires sibling EDirect helpers, especially `sort-table`; absolute-path invocation alone is not enough in a shell without the bio env on `PATH`.
- It prefilters with `grep '^[1-9]'`, so leading whitespace, zero, and non-digit first columns are silently ignored.
- Only the first two columns matter after filtering; any third column is ignored.
- Empty or filtered-away input can still emit the bogus sentinel row `0\t0\t1`, so do not treat any output as automatically valid.

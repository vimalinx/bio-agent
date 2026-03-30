---
name: fuse-ranges
description: Use when you need to merge overlapping or adjacent strand-specific alignment ranges encoded as comma-separated `start..end` lists in EDirect tables.
disable-model-invocation: true
user-invocable: true
---

# fuse-ranges

CLI tool from the Entrez Direct (EDirect) package for fusing overlapping or adjacent ranges.

## Quick Start

- **Command:** `printf '5\t1\t+\t3..8,8..10,15..13\n' | PATH=/home/vimalinx/miniforge3/envs/bio/bin:$PATH /home/vimalinx/miniforge3/envs/bio/bin/fuse-ranges`
- Local executable: `/home/vimalinx/miniforge3/envs/bio/bin/fuse-ranges`
- Reference: See [references/help.md](references/help.md) for full documentation

## When To Use This Tool

- Expand comma-separated `start..end` range lists and fuse overlaps per strand.
- Collapse adjacent intervals too, not just strict overlaps.
- Turn EDirect-style alignment summaries into strand / start / end / length blocks for later filtering or reporting.

## Common Patterns

```bash
# 1) Fuse a single row containing multiple strand-specific ranges
printf '5\t1\t+\t3..8,8..10,15..13\n' | \
  PATH=/home/vimalinx/miniforge3/envs/bio/bin:$PATH \
  /home/vimalinx/miniforge3/envs/bio/bin/fuse-ranges
```

```text
+   3   10  8
+   13  15  3
```

```bash
# 2) Use in a larger EDirect table pipeline
some_edirect_command | \
  PATH=/home/vimalinx/miniforge3/envs/bio/bin:$PATH \
  /home/vimalinx/miniforge3/envs/bio/bin/fuse-ranges \
  > fused.tsv
```

## Recommended Workflow

1. Generate a four-column table where column 3 is strand and column 4 is a comma-separated range list like `3..8,8..10,15..13`.
2. Put the EDirect bin directory on `PATH` so `sort-table` is available to the wrapper.
3. Pipe the table through `fuse-ranges` and capture the merged strand / start / end / length output.
4. Spot-check that adjacent intervals were merged the way you expect.

## Guardrails

- This wrapper depends on sibling EDirect tools such as `sort-table`; calling the absolute path alone can still fail with `command not found`.
- It prefilters with `grep '^[1-9]'`, so rows starting with `0`, whitespace, or non-digits are silently dropped.
- After that filter, only the strand column and the comma-separated range-list column are used; the first two fields are effectively ignored.
- Empty or non-matching input can yield a bogus `0 0 1` row instead of a clean error, so validate outputs before using them downstream.

---
name: expand-cols
description: Use when you need to expand comma-separated values in file columns into individual lines, replicating each line for every value in the specified columns.
disable-model-invocation: true
user-invocable: true
---

# expand-cols

## Quick Start
- **Command:** `expandCols -i <input> -c <cols>`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/expandCols`
- **Full reference:** `references/help.md`

## When To Use This Tool

- Expand comma-separated values in one or more columns into one row per element.
- Normalize bedtools or annotation outputs where a single field stores multiple values.
- Convert compact list-like cells into row-wise tabular form for downstream joins, filters, or summaries.
- Expand multiple columns in parallel when their comma-separated entries are aligned by position.

## Common Patterns

```bash
# 1) Expand one comma-separated column into multiple rows
expandCols \
  -i test.txt \
  -c 5
```

```bash
# 2) Expand two aligned comma-separated columns in lockstep
expandCols \
  -i test.txt \
  -c 4,5
```

```bash
# 3) Read from stdin and expand a list-valued annotation column
cat annotations.tsv | expandCols \
  -c 7
```

## Recommended Workflow

1. Identify which 1-based columns contain comma-separated payloads that should be expanded.
2. If expanding more than one column, confirm the comma-separated lists are aligned positionally within each row.
3. Run `expandCols` on the file or stdin and redirect the normalized output into downstream processing.
4. Spot-check a few rows to confirm the replicated row count matches the number of values you expected to unpack.

## Guardrails

- `-c` is required.
- If multiple columns are expanded together, they should have the same number of comma-separated values per row.
- Non-expanded columns are simply replicated across the emitted rows.
- If `-i` is omitted, input is read from stdin.
- Prefer `-h` for help; GNU-style `--help` and `--version` emit wrapper errors before usage text.

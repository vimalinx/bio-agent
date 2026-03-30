---
name: reorder-columns
description: Use when you need to reorder columns in tabular bioinformatics data files while preserving row content.
disable-model-invocation: true
user-invocable: true
---

# reorder-columns

Tiny EDirect shell helper that rewrites tab-delimited stdin through `awk`, printing the requested column order. It is a field selector, not a schema-aware table transformer.

## Quick Start

- **Command:** `reorder-columns`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/reorder-columns`
- **Actual contract:** pass 1-based column numbers as positional arguments and feed data on stdin

## When To Use This Tool

- Reordering columns in tab-delimited data files
- Preparing output formats for downstream bioinformatics tools
- Adjusting column order from entrez-direct pipeline outputs

## Common Patterns

```bash
# 1) Move column 3 to the front
printf 'a\tb\tc\n1\t2\t3\n' | reorder-columns 3 1 2
```

```bash
# 2) Keep only a subset of fields
cat table.tsv | reorder-columns 1 4 7
```

```bash
# 3) Duplicate a field intentionally
cat table.tsv | reorder-columns 2 2 1
```

## Recommended Workflow

1. Confirm the input is actually tab-delimited.
2. Decide the 1-based field order you need.
3. Pipe the table through `reorder-columns` and write the result to a new file.
4. Spot-check the first few rows before using the reordered table downstream.

## Guardrails

- `reorder-columns -h` is silent; there is no real help or version path.
- Source inspection shows the script hard-codes `awk -F '\t'`, so space-delimited data will not behave correctly.
- Column indices are positional and 1-based because the script emits `$1`, `$2`, and so on.
- Duplicate indices are allowed and repeat the same source column in the output.
- Missing indices beyond the end of a row follow plain `awk` behavior and expand to empty fields.

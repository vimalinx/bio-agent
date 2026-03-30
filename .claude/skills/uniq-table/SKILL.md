---
name: uniq-table
description: Use when removing invariant columns from a tab-delimited table, especially in EDirect or bioinformatics comparison pipelines.
disable-model-invocation: true
user-invocable: true
---

# uniq-table

Small AWK filter that keeps only tab-separated columns whose values change somewhere after row 2. It is a column-pruning tool, not a row-deduplication tool: constant columns disappear, while varying columns are preserved for every row.

## Quick Start

- **Command:** `uniq-table`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/uniq-table`
- **Input format:** Tab-delimited text on stdin

## When To Use This Tool

- Stripping columns that are constant across the compared rows
- Reducing wide comparison tables down to only informative fields
- Cleaning tabular output from EDirect text pipelines before manual review
- Highlighting which columns actually vary across records

## Common Patterns

```bash
# Keep only columns that vary after row 2
printf 'sample\tgroup\tconst\n1\tA\tkeep\n2\tA\tkeep\n3\tB\tkeep\n4\tB\tkeep\n' | uniq-table
```

```text
Output from local testing:
sample    group
1         A
2         A
3         B
4         B
```

```bash
# Use inside a pipeline
some-tab-producing-command | uniq-table > informative-columns.tsv
```

## Recommended Workflow

1. Feed `uniq-table` a tab-delimited table with a stable header and representative early rows.
2. Run it after a step that produces comparison-style columns you want to trim.
3. Inspect the output headers to confirm only meaningful columns remain.
4. Save or pass the reduced table downstream for reporting or manual review.

## Guardrails

- `uniq-table` does not deduplicate rows. It drops columns that never change after row 2.
- The script hard-codes `FS = "\t"`, so whitespace-separated tables are not handled correctly.
- Because the executable is just an AWK script, `uniq-table -help` shows the generic `gawk` help text, not tool-specific usage.
- Source inspection shows row 2 is used as the baseline for deciding whether later rows make a column “interesting”.
- If a column is constant from row 2 onward, it is removed even if row 1 is a header with a different string value.

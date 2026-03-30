---
name: filter-columns
description: Use when filtering or manipulating columns in tabular data files from bioinformatics workflows.
disable-model-invocation: true
user-invocable: true
---

# filter-columns

## Quick Start

- **Command**: `filter-columns 'awk_expression' < input.tsv`
- **Local executable**: `/home/vimalinx/miniforge3/envs/bio/bin/filter-columns`
- **Full reference**: See [references/help.md](references/help.md)

## When To Use This Tool

- Filter tab-delimited streams with an inline `awk` condition over `$1`, `$2`, and so on.
- Keep or discard rows from lightweight EDirect or bioinformatics tables without opening a spreadsheet.
- Apply simple numeric/date/string predicates inside a shell pipeline.

## Common Patterns

```bash
# 1) Keep rows whose second column is between 10 and 20
filter-columns '10 <= $2 && $2 <= 20' < input.tsv
```

```bash
# 2) Keep only protein-coding rows with high score
filter-columns '$3 == "protein_coding" && $5 >= 0.95' < annotations.tsv
```

## Recommended Workflow

1. Confirm the stream is tab-delimited.
2. Write the predicate as a single quoted `awk` expression.
3. Run `filter-columns` in a pipe or with stdin redirection.
4. Spot-check the retained rows before continuing downstream.

## Guardrails

- The expression must be quoted as one shell argument, or the shell will split and reinterpret it before `awk` sees it.
- This wrapper hard-codes tab as the field separator; it is not a CSV-aware filter.
- `--help` and `--version` do not provide real documentation in this build.
- The wrapper injects `YR` and `DT` `awk` variables with the current year and date, so avoid accidental name collisions.

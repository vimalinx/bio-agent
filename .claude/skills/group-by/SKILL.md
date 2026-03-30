---
name: group-by
description: Use when you need to summarize tabular data by grouping rows on common column values and applying aggregation operations (sum, count, mean, etc.), similar to SQL GROUP BY.
disable-model-invocation: true
user-invocable: true
---

# group-by

## Quick Start
- **Command**: `groupBy -i <file> -g <cols> -c <cols> -o <ops>`
- **Local executable**: `/home/vimalinx/miniforge3/envs/bio/bin/groupBy`
- **Full reference**: See `references/help.md`

## When To Use This Tool

- Summarize tabular outputs by shared key columns, similar to SQL `GROUP BY`.
- Collapse many overlap rows into per-feature counts, sums, means, or distinct value lists.
- Aggregate one or more columns with operations like `sum`, `count`, `mean`, `collapse`, `distinct`, `concat`, `first`, and `last`.
- Post-process interval joins and annotation tables into compact summaries.

## Common Patterns

```bash
# 1) Sum a numeric column per genomic feature
groupBy \
  -i overlaps.tsv \
  -g 1,2,3,4 \
  -c 9 \
  -o sum
```

```bash
# 2) Apply multiple operations to the same column
groupBy \
  -i overlaps.tsv \
  -g 1,2,3,4 \
  -c 9,9 \
  -o sum,max
```

```bash
# 3) Collapse IDs and compute the mean score per group from stdin
cat overlaps.tsv | groupBy \
  -g 1,2,3,4 \
  -c 8,9 \
  -o collapse,mean
```

## Recommended Workflow

1. Decide which columns define the grouping key and make sure the input is already sorted/grouped by those columns.
2. Choose the summarized column list with `-c` and the corresponding aggregation operations with `-o`.
3. Run the aggregation on a file or via stdin, using `-header` / `-inheader` / `-outheader` when headers are present.
4. Tune `-prec`, `-delim`, or `-full` only when the downstream consumer needs those specific output conventions.

## Guardrails

- `-c` is required; without it, bedtools does not know which column(s) to aggregate.
- The input must already be sorted/grouped by the `-g` columns, or identical groups will be split across multiple output rows.
- Column numbers are 1-based.
- If you supply multiple columns and multiple operations, the counts must either match or one side must have length 1 so bedtools can broadcast it.
- `-full` keeps non-group columns from the first row in each group, which can be misleading if later rows in the same group differ.

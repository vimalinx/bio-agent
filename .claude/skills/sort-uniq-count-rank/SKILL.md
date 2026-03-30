---
name: sort-uniq-count-rank
description: Use when turning repeated nonblank text lines into a frequency-ranked table, with counts sorted descending after case-insensitive grouping.
disable-model-invocation: true
user-invocable: true
---

# sort-uniq-count-rank

Extension of `sort-uniq-count`. It builds the same intermediate `count<TAB>value` table, then sorts the result by count descending and by value using the same compact flag bundle.

## Quick Start

- **Command:** `... | sort-uniq-count-rank [bfinrs]`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/sort-uniq-count-rank`
- **Primary ranking sort:** `-k 1,1nr`

## When To Use This Tool

- Producing a ranked frequency table from repeated text lines
- Finding the most common case-insensitive values in a stream
- Getting directly to “top counts first” output without an extra sort stage
- Reusing the same compact sort-flag conventions as `sort-uniq-count`

## Common Patterns

```bash
# Ranked frequency table
printf 'beta\nAlpha\nalpha\nbeta\n' | sort-uniq-count-rank
```

```bash
# Reverse secondary ordering
printf 'a\na\nb\n' | sort-uniq-count-rank r
```

```bash
# Keep only the most frequent rows
cat values.txt | sort-uniq-count-rank | head
```

## Recommended Workflow

1. Feed it one logical item per line.
2. Use it when you want ranked output immediately, otherwise use `sort-uniq-count` first.
3. Pass only the supported compact sort letters (`bfinrs`) if you need to alter the secondary sort behavior.
4. Treat the first column as numeric frequency and the second column as the grouped value.

## Guardrails

- Like `sort-uniq-count`, this wrapper is case-insensitive because it always uses `uniq -i -c`.
- The wrapper sorts internally, so pre-sorted input is unnecessary.
- `-h` and `--version` are not metadata paths; they are mangled into downstream sort options. Locally, `-h` failed with `sort: stray character in field spec: invalid field specification '2s'`.
- The final ranking sort is `sort -t '\t' -k 1,1nr -k "2$flags"`, so the first column is always descending numeric count and the second-column behavior depends on the derived flag bundle.
- In local testing, `printf 'beta\nAlpha\nalpha\nbeta\n' | sort-uniq-count-rank` emitted the same two rows as the unranked wrapper because both counts were tied at `2`.

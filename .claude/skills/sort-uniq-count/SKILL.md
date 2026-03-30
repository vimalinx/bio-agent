---
name: sort-uniq-count
description: Use when counting nonblank text lines after an internal sort, especially when you want case-insensitive grouping in a compact shell wrapper.
disable-model-invocation: true
user-invocable: true
---

# sort-uniq-count

Shell pipeline wrapper that removes blank lines, sorts the stream, groups identical lines case-insensitively with `uniq -i -c`, and rewrites the result as tab-delimited `count<TAB>value`.

## Quick Start

- **Command:** `... | sort-uniq-count [bfinrs]`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/sort-uniq-count`
- **Default sort flag bundle:** `f`

## When To Use This Tool

- Counting repeated nonblank lines without manually composing `sort | uniq -c | awk`
- Performing case-insensitive frequency summaries on text streams
- Applying a small subset of GNU `sort` flags before counting
- Producing tab-delimited count tables for later ranking or filtering

## Common Patterns

```bash
# Default case-insensitive counting
printf 'beta\nAlpha\nalpha\nbeta\n' | sort-uniq-count
```

```bash
# Numeric pre-sort before counting
printf '10\n2\n2\n' | sort-uniq-count n
```

```bash
# Reverse sort before counting
cat values.txt | sort-uniq-count r
```

## Recommended Workflow

1. Feed the wrapper a one-item-per-line text stream.
2. Pass only the compact flag letters it understands (`bfinrs`) when you need to alter the internal `sort`.
3. Capture the resulting `count<TAB>value` table or pipe it into `sort-uniq-count-rank`.
4. Treat the output as case-insensitive counts unless you have inspected the shell pipeline and intentionally changed it.

## Guardrails

- The wrapper sorts internally, so the input does not need to be pre-sorted; the old “sorted input required” assumption is wrong.
- Counting is case-insensitive because the pipeline always uses `uniq -i -c`, and the default sort mode is `-f`.
- It does not implement real help/version flags. For example, `--version` was mangled into sort-option letters and locally failed with `sort: options '-in' are incompatible`.
- Unrecognized user arguments are stripped down to the subset `[bfinrs]`; if none survive, the wrapper falls back to `s` rather than erroring cleanly.
- In local testing, `printf 'beta\nAlpha\nalpha\nbeta\n' | sort-uniq-count` produced two rows: `2\tAlpha` and `2\tbeta`.

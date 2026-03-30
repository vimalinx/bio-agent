---
name: sort-table
description: Use when sorting tab-delimited, nonblank text rows with GNU `sort` while preserving a fixed tab field separator in shell pipelines.
disable-model-invocation: true
user-invocable: true
---

# sort-table

Minimal shell wrapper around GNU `sort`. It first removes blank lines with `grep '.'`, then calls `sort -t $'\\t' "$@"`, so tab is always the field separator.

## Quick Start

- **Command:** `... | sort-table [sort-args]`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/sort-table`
- **Fixed delimiter:** tab

## When To Use This Tool

- Sorting tab-delimited rows without repeatedly spelling out the tab separator
- Passing normal GNU `sort` key or numeric flags through a thin wrapper
- Cleaning out blank lines before sorting tabular text
- Reusing a predictable tab-based sort primitive inside bioinformatics shell pipelines

## Common Patterns

```bash
# Numeric sort on the second tab-delimited column
printf 'z\t10\n\na\t2\nb\t1\n' | sort-table -k 2,2n
```

```bash
# Lexicographic sort on the first column
cat table.tsv | sort-table -k 1,1
```

```bash
# Reverse numeric sort on a score column
cat table.tsv | sort-table -k 3,3nr
```

## Recommended Workflow

1. Make sure the input is truly tab-delimited text.
2. Pass ordinary GNU `sort` arguments exactly as you would to `sort`, except you do not need to specify `-t $'\\t'`.
3. Write the sorted output to stdout or redirect it to a file.
4. If you need documentation for flag semantics, consult GNU `sort`, not this wrapper.

## Guardrails

- Blank lines are dropped unconditionally because the wrapper begins with `grep '.'`.
- `-h` is not help here; it is forwarded to GNU `sort` as the human-numeric flag, so `sort-table -h` with no data does not print usage.
- `--version` is forwarded to GNU `sort`; in this environment it reported `sort (GNU coreutils) 9.10`.
- In live testing, `printf 'z\t10\n\na\t2\nb\t1\n' | sort-table -k 2,2n` yielded `b\t1`, `a\t2`, `z\t10`.

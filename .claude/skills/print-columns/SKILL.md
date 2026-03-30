---
name: print-columns
description: Use when projecting or transforming tab-delimited stdin columns with a tiny EDirect `awk` wrapper, especially for quick field arithmetic, quoting, or date stamping in shell pipelines.
disable-model-invocation: true
user-invocable: true
---

# print-columns

## Quick Start

- **Command:** `print-columns 'awk_print_expression'`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/print-columns`
- **I/O shape:** reads tab-delimited stdin and emits the requested fields on stdout

## When To Use This Tool

- Project or reorder tab-delimited columns without writing a full `awk` command each time.
- Add lightweight arithmetic or string transforms inside an EDirect shell pipeline.
- Stamp output with the current year (`YR`) or date (`DT`) via the wrapper's built-in variables.
- Quickly quote or lowercase specific fields before piping into another shell utility.

## Common Patterns

```bash
# 1) Reorder columns and add arithmetic
printf '1\t2\t3\n' | print-columns '$1, $2+1, YR, DT'
```

```bash
# 2) Quote a selected field
printf 'geneA\t42\n' | print-columns '$1, "\"" $2 "\""'
```

```bash
# 3) Lowercase and keep selected columns from an upstream extractor
xtract -pattern DocumentSummary -element Name,Status,CreateDate |
print-columns '$1, tolower($2), $3'
```

## Recommended Workflow

1. Make sure the incoming stream is tab-delimited, because the wrapper hard-codes `-F '\t'`.
2. Write the desired `awk` print expression and wrap it in single quotes so the shell does not expand `$1`, `$2`, and friends.
3. Pipe stdin into `print-columns` and verify that the transformed columns still line up with downstream expectations.
4. Use the built-in `YR` and `DT` variables when you need run-date metadata without calling `date` yourself.

## Guardrails

- The expression is injected directly into `awk "{print ...}"`; if you forget shell quoting, `$1` and similar fields will be expanded by the shell and the command can break with an `awk` syntax error.
- There is no real option parsing or built-in help path; `print-columns --help` with no stdin produces no useful output.
- The wrapper is stdin-oriented and does not support separate filenames or flags in the usual `awk` style.
- Field splitting is always tab-based, not whitespace-generic.
- The wrapper defines `YR` as the current year and `DT` as the current `YYYY-MM-DD` date for use inside the print expression.

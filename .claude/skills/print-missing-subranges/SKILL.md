---
name: print-missing-subranges
description: Use when reporting gaps in an ordered list of ascending integer positions, identifiers, or coordinates by printing the missing ranges between observed values.
disable-model-invocation: true
user-invocable: true
---

# print-missing-subranges

## Quick Start

- **Command:** `print-missing-subranges [file ...]`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/print-missing-subranges`
- **I/O shape:** reads ordered integers from stdin or files and writes missing ranges such as `3-4`

## When To Use This Tool

- Find numeric gaps in a sorted one-column list of positions or identifiers.
- Report missing spans between observed values before downstream range filling or QC.
- Keep the logic in a tiny shell pipeline instead of writing custom `awk` each time.
- Handle simple integer streams, not BED / GFF interval files.

## Common Patterns

```bash
# 1) Detect gaps from stdin
printf '1\n2\n5\n8\n' | print-missing-subranges
```

```bash
# 2) Detect gaps from a file
print-missing-subranges ordered_positions.txt
```

```bash
# 3) Use after extracting and sorting numeric identifiers
xtract -pattern DocumentSummary -element Id |
sort -n |
print-missing-subranges
```

## Recommended Workflow

1. Reduce the input to one ascending integer per line.
2. Sort numerically before calling the wrapper if the source stream is not already ordered.
3. Interpret each emitted `start-end` row as a missing inclusive block.
4. Stop here if you only need gap reporting; use a separate tool if you need interval reconstruction or filling.

## Guardrails

- The wrapper assumes ordered ascending integers; unsorted input or duplicates will give misleading ranges.
- There is no real help or version interface, and flags such as `--help` are treated as filenames.
- The first expected value is implicitly `1`, so an input starting at `5` will report `1-4` as missing.
- The tool only reports gaps between observed values; it does not infer a terminal upper bound after the last line.
- This is a one-column integer gap finder, not a generic genomic interval subtraction tool.

---
name: merge-bed
description: Use when merging overlapping or book-ended intervals in BED/GFF/VCF files into single intervals.
disable-model-invocation: true
user-invocable: true
---

# merge-bed

## Quick Start
- **Command:** `mergeBed -i sorted.bed [options]`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/mergeBed`
- **Full reference:** See `references/help.md`

## When To Use This Tool

- Collapse overlapping or book-ended intervals into nonredundant merged regions.
- Merge nearby intervals within a maximum gap using `-d`.
- Keep strand-specific merged blocks with `-s` or one chosen strand with `-S`.
- Summarize columns across merged blocks with `-c` and `-o`.

## Common Patterns

```bash
# 1) Basic merge of sorted intervals
mergeBed \
  -i peaks.sorted.bed
```

```bash
# 2) Merge intervals within 500 bp on the same strand
mergeBed \
  -i exons.sorted.bed \
  -s \
  -d 500
```

```bash
# 3) Merge and summarize scores and names
mergeBed \
  -i peaks.sorted.bed \
  -c 4,5 \
  -o collapse,max
```

## Recommended Workflow

1. Sort the input by chromosome and start coordinate before anything else.
2. Decide whether book-ended features should merge as-is (`-d 0`, the default) or whether you need a stricter / looser distance rule.
3. Add `-s` / `-S` only when strand is biologically meaningful for the interval type.
4. Use `-c` and `-o` explicitly if you need metadata preserved, because raw merge output only reports merged coordinates.

## Guardrails

- Sorted input is mandatory; unsorted files will produce wrong output.
- `-d 0` merges both overlapping and directly book-ended intervals; many users forget the book-ended part.
- Negative `-d` values enforce a minimum required overlap rather than a gap tolerance.
- If you provide multiple `-c` columns and multiple `-o` operations, their counts must align unless you intentionally rely on the single-column / single-op broadcast behavior.
- Prefer `-h` for help; `--version` is not cleanly supported on this wrapper.

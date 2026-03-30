---
name: intersect-bed
description: Use when you need to find overlaps between two genomic interval files (BED, GFF, VCF, or BAM), filter features by intersection, or count/report overlapping regions between datasets.
disable-model-invocation: true
user-invocable: true
---

# intersect-bed

## Quick Start
- **Command:** `intersectBed -a <A> -b <B> [options]`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/intersectBed`
- **Full reference:** See `references/help.md`

## When To Use This Tool

- Find overlaps between genomic intervals in BED, GFF, VCF, or BAM-like inputs.
- Filter A features to keep only overlapping records or only non-overlapping records.
- Count overlaps per A feature with `-c` / `-C`.
- Retain joined context from both files with `-wa -wb`, `-wo`, `-wao`, or `-loj`.
- Apply strand-aware and fraction-aware overlap rules before downstream annotation or QC.

## Common Patterns

```bash
# 1) Basic interval overlap
intersectBed \
  -a peaks.bed \
  -b promoters.bed
```

```bash
# 2) Keep both records plus overlap length
intersectBed \
  -a peaks.bed \
  -b promoters.bed \
  -wa -wb -wo
```

```bash
# 3) Count overlaps per A interval with reciprocal overlap filtering
intersectBed \
  -a peaks.bed \
  -b enhancers.bed \
  -c \
  -f 0.5 \
  -r
```

## Recommended Workflow

1. Decide whether you need filtering (`-u`, `-v`), joining (`-wa`, `-wb`, `-wo`, `-wao`, `-loj`), or counting (`-c`, `-C`) before you run the command.
2. Confirm chromosome naming conventions match across files before trusting an empty result.
3. Add `-s` / `-S` and `-f` / `-F` / `-r` / `-e` deliberately instead of assuming bedtools defaults fit the biology.
4. Use `-sorted` only when the inputs are truly sorted, and provide `-g` if you need a fixed chromosome order.

## Guardrails

- Both `-a` and `-b` are required, and `-b` can contain multiple files or wildcards.
- With BAM as `-a`, the default output is BAM-like alignment output unless you request `-bed` or `-ubam`.
- `-wao` reports non-overlapping A records with a NULL B feature and overlap `0`; `-wo` does not.
- `-C` reports counts per B file on distinct lines, which is easy to misread if you expected one line per A feature.
- Prefer `-h` for help; some `--help` / `--version` patterns on these bedtools wrappers emit errors before exiting.

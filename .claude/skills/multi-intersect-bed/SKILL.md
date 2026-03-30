---
name: multi-intersect-bed
description: Use when you need to identify overlapping genomic regions across multiple BED files simultaneously.
disable-model-invocation: true
user-invocable: true
---

# multi-intersect-bed

## Quick Start
- **Command:** `multiIntersectBed -i file1.bed file2.bed [file3.bed ...] [options]`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/multiIntersectBed`
- **Full reference:** See `references/help.md`

## When To Use This Tool

- Partition the genome into sub-intervals labeled by which of several files overlap them.
- Compare shared and unique regions across multiple BED / GFF / VCF inputs in one pass.
- Generate presence/absence matrices over segmented interval space.
- Include empty regions relative to a genome file with `-g -empty`.

## Common Patterns

```bash
# 1) Multi-file overlap segmentation
multiIntersectBed \
  -i sample1.bed sample2.bed sample3.bed
```

```bash
# 2) Add a header with readable file names
multiIntersectBed \
  -header \
  -names tumor normal blacklist \
  -i tumor.bed normal.bed blacklist.bed
```

```bash
# 3) Include empty regions across the genome
multiIntersectBed \
  -i a.bed b.bed \
  -g genome.txt \
  -empty
```

## Recommended Workflow

1. Sort every input file by chromosome and start before running the tool.
2. Decide whether you need just overlapping segmentation or also empty regions from a genome definition.
3. Use `-names` and `-header` when the output will be read by humans or imported into tables.
4. Post-process the membership columns to define how many files must support a region for your biological question.

## Guardrails

- Each interval file must be sorted by chromosome and start.
- This tool segments coordinate space; the output intervals are often smaller than the original input intervals.
- `-empty` requires `-g`.
- `-incl` / `-excl` style constraints do not exist here; this is an overlap partitioning tool, not a shuffler.
- Prefer `-h` for help; the captured `--help` path in references is misleading because the wrapper expects other arguments first.

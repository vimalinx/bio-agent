---
name: random-bed
description: Use when generating random genomic intervals for simulation, background sets, or statistical testing.
disable-model-invocation: true
user-invocable: true
---

# random-bed

## Quick Start
- **Command:** `randomBed -g genome.txt [-l length] [-n count] [-seed int]`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/randomBed`
- **Full reference:** See `references/help.md`

## When To Use This Tool

- Generate simple random genomic intervals from a genome definition.
- Build background interval sets for simulations or quick null distributions.
- Produce many fixed-length windows without reference to an input BED file.
- Create reproducible random sets with `-seed`.

## Common Patterns

```bash
# 1) Generate 10,000 random 500 bp intervals
randomBed \
  -g genome.txt \
  -l 500 \
  -n 10000 > random.bed
```

```bash
# 2) Reproducible random intervals
randomBed \
  -g genome.txt \
  -l 1000 \
  -n 5000 \
  -seed 42 > random.seed42.bed
```

```bash
# 3) Use a FASTA index as genome source
randomBed \
  -g reference.fa.fai \
  -l 200 \
  -n 1000
```

## Recommended Workflow

1. Build a valid genome file first, typically from a FASTA `.fai`.
2. Set interval length and count explicitly rather than relying on defaults.
3. Add `-seed` for reproducibility if the output will be reused or published.
4. Filter or post-process the output afterward if you need exclusion masks, chromosome preservation, or non-overlap constraints.

## Guardrails

- `-g` is required.
- Defaults are surprisingly large: 100 bp intervals and 1,000,000 records.
- `randomBed` is unconstrained random generation; if you need exclusion masks or same-chromosome shuffling of an existing BED set, use `shuffleBed` instead.
- The genome file is tab-delimited chromosome name plus size; a FASTA `.fai` works because bedtools reads only the first two columns.
- Prefer `-h` for help; GNU-style `--help` / `--version` calls on these wrappers are noisy.

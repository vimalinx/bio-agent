---
name: complement-bed
description: Use when you need to find genomic regions NOT covered by features in a BED/GFF/VCF file, such as identifying gaps, intergenic regions, or uncovered intervals.
disable-model-invocation: true
user-invocable: true
---

# complement-bed

## Quick Start
- **Command:** `complementBed -i intervals.bed -g genome.txt [options]`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/complementBed`
- **Full reference:** See `references/help.md`

## When To Use This Tool

- Find genomic gaps not covered by an interval set.
- Derive intergenic or uncovered regions relative to a reference genome definition.
- Convert a mask or annotation track into its uncovered complement.
- Restrict complement output to chromosomes actually present in the input with `-L`.

## Common Patterns

```bash
# 1) Compute uncovered genome segments
complementBed \
  -i exons.bed \
  -g genome.txt
```

```bash
# 2) Limit complement to chromosomes represented in the input
complementBed \
  -i targets.bed \
  -g genome.txt \
  -L
```

```bash
# 3) Use a FASTA index as the genome file
complementBed \
  -i blacklist.bed \
  -g reference.fa.fai
```

## Recommended Workflow

1. Build or obtain a correct genome file before trusting any complement output.
2. Make sure the interval file and genome file use the same chromosome names.
3. Decide whether the result should cover the whole genome from `-g` or only chromosomes that appear in the input (`-L`).
4. Inspect edge chromosomes manually when the complement is unexpectedly huge, because that often indicates naming mismatches or missing contigs.

## Guardrails

- `-g` is mandatory.
- The genome file must be tab-delimited with chromosome name in column 1 and chromosome length in column 2.
- Without `-L`, chromosomes present in the genome file but absent from the input will be emitted in full as complement intervals.
- Complement assumes the input intervals represent covered regions; overlapping or unsorted input can still produce valid complement output, but upstream normalization is often wise.
- Prefer `-h` for help; wrapper behavior for `--version` is noisy.

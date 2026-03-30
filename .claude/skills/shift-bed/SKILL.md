---
name: shift-bed
description: Use when you need to shift genomic intervals in BED/GFF/VCF files by a specified number of base pairs, either uniformly or strand-specifically.
disable-model-invocation: true
user-invocable: true
---

# shift-bed

## Quick Start
- **Command**: `shiftBed -i <bed/gff/vcf> -g <genome> -s <int>`
- **Local executable**: `/home/vimalinx/miniforge3/envs/bio/bin/shiftBed`
- **Full reference**: See `references/help.md`

## When To Use This Tool

- Translate intervals left or right along the genome by a fixed distance.
- Shift plus- and minus-strand features by different amounts with `-p` and `-m`.
- Express shifts as a fraction of feature length with `-pct`.
- Create offset control regions or adjust reported interval centers while preserving interval width.

## Common Patterns

```bash
# 1) Shift every interval 100 bp
shiftBed \
  -i peaks.bed \
  -g genome.sizes \
  -s 100
```

```bash
# 2) Shift plus and minus strands in opposite directions
shiftBed \
  -i transcripts.bed \
  -g genome.sizes \
  -p 500 \
  -m -500
```

```bash
# 3) Shift by 10% of each feature length
shiftBed \
  -i intervals.bed \
  -g genome.sizes \
  -s 0.10 \
  -pct
```

## Recommended Workflow

1. Prepare a genome file (or FASTA `.fai`) so bedtools can clamp shifted features to chromosome bounds.
2. Decide whether the shift is uniform with `-s` or strand-specific with `-p` and `-m`.
3. Decide whether values are absolute base pairs or fractions of feature length via `-pct`.
4. Inspect the output for boundary clipping at chromosome starts and ends before using it in downstream analysis.

## Guardrails

- `-i` and `-g` are both required.
- Use either `-s` alone or `-p` together with `-m`; those modes are mutually exclusive.
- With `-pct`, values like `0.10` mean 10% of feature length, not 0.10 bp.
- Starts are clipped to 0 and ends are clipped to chromosome length when a shift would move a feature out of bounds.
- Prefer `-h` for help; GNU-style `--help` and `--version` emit wrapper errors before usage text.

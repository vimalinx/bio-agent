---
name: flank-bed
description: Use when you need to create flanking intervals adjacent to BED/GFF/VCF features for promoter analysis, regulatory region discovery, or upstream/downstream sequence extraction.
disable-model-invocation: true
user-invocable: true
---

# flank-bed

## Quick Start
- **Command:** `flankBed -i features.bed -g genome.txt [-b <size> | -l <size> -r <size>] [options]`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/flankBed`
- **Full reference:** See `references/help.md`

## When To Use This Tool

- Create separate upstream and downstream flank intervals adjacent to existing features.
- Generate promoter-like or neighborhood windows around genes, peaks, or other annotations.
- Respect feature strand when translating left / right into upstream / downstream with `-s`.
- Define flank sizes as absolute bases or as a fraction of feature length with `-pct`.

## Common Patterns

```bash
# 1) Symmetric 1 kb flanks on both sides
flankBed \
  -i genes.bed \
  -g genome.txt \
  -b 1000
```

```bash
# 2) Strand-aware upstream/downstream flanks
flankBed \
  -i genes.bed \
  -g genome.txt \
  -l 2000 \
  -r 500 \
  -s
```

```bash
# 3) Flanks sized as a fraction of feature length
flankBed \
  -i peaks.bed \
  -g genome.txt \
  -l 0.5 \
  -r 0.25 \
  -pct
```

## Recommended Workflow

1. Decide whether you want symmetric flanks (`-b`) or distinct left / right sizes (`-l` and `-r`).
2. Add `-s` whenever left/right should be interpreted relative to biological strand.
3. Use `-pct` only when proportional flank size is the intended design.
4. Validate a few output records near chromosome starts and ends because flanks are clipped to genome boundaries.

## Guardrails

- `-i` and `-g` are required.
- Use either `-b` alone or `-l` with `-r`; do not mix the modes.
- `flankBed` creates new adjacent intervals; it does not extend the original interval in place like `slopBed`.
- Starts are clamped to `0` and ends are clamped to chromosome length from the genome file.
- Prefer `-h` for help; GNU-style `--help` / `--version` calls on these wrappers are noisy.

---
name: rnaforester
description: Use when comparing, aligning, or computing similarity/distance between RNA secondary structures, or when generating multiple structure alignments with consensus prediction.
disable-model-invocation: true
user-invocable: true
---

# rnaforester

## Quick Start

- **Command**: `RNAforester [options]`
- **Local executable**: `/home/vimalinx/miniforge3/envs/bio/bin/RNAforester`
- **Full reference**: See `references/help.md` for complete options and usage details

## When To Use This Tool

- Align or score RNA secondary structures directly rather than folding sequences anew.
- Run local, global, or small-in-large structure comparisons.
- Build multiple structure alignments with consensus prediction.
- Generate 2D alignment plots for manual inspection.

## Common Patterns

```bash
# 1) Align structures from an input file
RNAforester -f=structures.txt
```

```bash
# 2) Compute local structural similarity
RNAforester -l -f=structures.txt
```

```bash
# 3) Predict structures from sequences before aligning them
RNAforester -p -f=sequences.fa > forester.out
```

## Recommended Workflow

1. Prepare input structures in file and verify format compatibility
2. Run `RNAforester -f=inputfile` for basic structure alignment, or add `-l` for local similarity, `-s` for small-in-large, or `-m` for multiple alignment mode
3. Use `-p` to predict structures from sequences when needed, or `--score` to compute only scores without alignment output
4. Generate visualization with `-2d` for PostScript 2D plots if alignment inspection is needed

## Guardrails

- Input files require valid RNA secondary structure format; verify structure syntax before running
- Scoring parameters (`-pm`, `-pd`, `-bm`, `-br`, etc.) significantly affect results—use defaults unless specific tuning is required
- For multiple alignment mode (`-m`), consider clustering thresholds (`-mt`, `-mc`) to control alignment granularity

---
name: rnasubopt
description: Use when computing suboptimal RNA secondary structures within an energy range above the minimum free energy, or when sampling structures from the Boltzmann ensemble.
disable-model-invocation: true
user-invocable: true
---

# rnasubopt

## Quick Start

- **Command**: `RNAsubopt`
- **Local executable**: `/home/vimalinx/miniforge3/envs/bio/bin/RNAsubopt`
- **Full reference**: See `references/help.md` for complete options and parameter details

## When To Use This Tool

- Use `RNAsubopt` when you need a set of plausible secondary structures instead of a single best fold.
- Use `-e` to enumerate all structures within an energy band above the MFE for short or moderate-length RNAs.
- Use `-p` when exhaustive enumeration would explode and you instead want Boltzmann-weighted sampling from the ensemble.
- Reach for `-z`, `-D`, `-c`, or `-g` when the question is specifically about Zuker suboptimals, density of states, circular RNAs, or G-quadruplex-aware folding.
- It is also appropriate when experimental probing data should bias the structure ensemble through `--shape` or `--sp-data`.

## Common Patterns

```bash
# Enumerate structures within 2 kcal/mol of the MFE
printf 'GGGAAAUCC\n' | RNAsubopt -e 2

# Sample 100 structures from the Boltzmann ensemble
printf 'GGGAAAUCC\n' | RNAsubopt -p 100

# Sort enumerated suboptimal structures
printf 'GGGAAAUCC\n' | RNAsubopt -e 2 -s

# Compute density of states instead of explicit structures
printf 'GGGAAAUCC\n' | RNAsubopt -D
```

## Recommended Workflow

1. Prepare RNA sequence input via stdin or specify an input file with `-i`
2. Select algorithm mode: energy range enumeration (`-e`), stochastic sampling (`-p`), or Zuker suboptimals (`-z`)
3. Run `RNAsubopt` with appropriate parameters (e.g., `-e 3.0` for structures within 3 kcal/mol of MFE, `-p 1000` for 1000 sampled structures)
4. Review output containing dot-bracket secondary structures followed by energy values in kcal/mol

## Guardrails

- Output size grows exponentially with sequence length and energy range; use conservative `-e` values or switch to sampling (`-p`) for long sequences
- Default temperature is 37°C; adjust with `-T` for non-physiological or organism-specific conditions
- Nucleotide "T" is automatically converted to "U" by default; use `--noconv` to preserve input exactly

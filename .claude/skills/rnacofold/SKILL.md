---
name: rnacofold
description: Use when predicting secondary structures of two RNA sequences with dimerization, computing equilibrium concentrations of monomer and dimer species, or analyzing RNA-RNA hybridization thermodynamics.
disable-model-invocation: true
user-invocable: true
---

# rnacofold

## Quick Start

- **Command**: `RNAcofold [OPTIONS] < input.txt`
- **Local executable**: `/home/vimalinx/miniforge3/envs/bio/bin/RNAcofold`
- **Full reference**: See `references/help.md` for complete options and details

## When To Use This Tool

- Fold two RNAs together as a heterodimer or homodimer candidate.
- Compare MFE-only duplexes with ensemble-aware predictions using `-p`.
- Compute monomer/dimer free energies for concentration-dependent analyses.
- Estimate equilibrium concentrations for A, B, AA, BB, and AB species.

## Common Patterns

```bash
# 1) Fold one RNA pair as a dimer candidate
echo 'AUGCUA&UAGCAU' | RNAcofold
```

```bash
# 2) Add partition function and pairing probabilities
echo 'AUGCUA&UAGCAU' | RNAcofold -p
```

```bash
# 3) Compute all species and equilibrium concentrations
RNAcofold -a -c -f concentrations.txt < pairs.fa
```

## Recommended Workflow

1. Prepare input sequences concatenated with `&` as separator (e.g., `AUGCU&GCAUA`)
2. Run `RNAcofold -p` to compute MFE structure plus partition function and pairing probabilities
3. Use `-a -c` options to compute free energies and equilibrium concentrations for all species
4. Review bracket notation output and PostScript structure plots for dimerization analysis

## Guardrails

- Sequences must be concatenated with `&` character as separator; otherwise dimerization is not computed
- Equilibrium concentration calculations require the `-c` flag and initial monomer concentrations
- Use `-T` to rescale energy parameters when analyzing at non-physiological temperatures (default 37°C)

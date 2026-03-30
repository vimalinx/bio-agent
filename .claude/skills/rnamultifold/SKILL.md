---
name: rnamultifold
description: Use when predicting secondary structures and base pairing probabilities for multiple interacting RNA molecules
disable-model-invocation: true
user-invocable: true
---

# rnamultifold

## Quick Start

- **Command**: `RNAmultifold [OPTION]... [FILE]...`
- **Local executable**: `/home/vimalinx/miniforge3/envs/bio/bin/RNAmultifold`
- **Full reference**: See `references/help.md` for complete options and details

## When To Use This Tool

- Fold more than two interacting RNA strands in one complex.
- Compare one chosen multimer arrangement with the ensemble of all possible complexes.
- Add partition-function probabilities to multi-strand MFE predictions.
- Estimate concentrations for all species formed from the supplied strands.

## Common Patterns

```bash
# 1) Fold a specific multi-strand arrangement
echo 'AUGCUA&UAGCAU&GGAUCC' | RNAmultifold
```

```bash
# 2) Add partition function and pair probabilities
echo 'AUGCUA&UAGCAU&GGAUCC' | RNAmultifold -p
```

```bash
# 3) Compute all complexes and concentration estimates
RNAmultifold -a -c -f concentrations.txt < complexes.fa
```

## Recommended Workflow

1. Prepare input sequences with multiple strands concatenated using '&' as separator (e.g., `SEQUENCE_A&SEQUENCE_B`)
2. Run `RNAmultifold` with appropriate flags: `-p` for partition function, `-a` for all complexes up to the input count
3. Review the PostScript dot plot output file for base pairing probabilities
4. Use `-c` or `--concfile` to compute equilibrium concentrations if needed

## Guardrails

- Multiple strands must be concatenated with the '&' character as separator; sequences are read one per line
- Temperature defaults to 37°C; use `-T` to adjust energy parameters for non-standard conditions
- Terminate batch input with a single `@` character on its own line or EOF signal

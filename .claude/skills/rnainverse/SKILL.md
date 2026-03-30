---
name: rnainverse
description: Use when searching for RNA sequences that fold into a predefined secondary structure, inverting RNA folding predictions to find sequences matching target bracket notation structures.
disable-model-invocation: true
user-invocable: true
---

# rnainverse

## Quick Start

- **Command**: `RNAinverse`
- **Local executable**: `/home/vimalinx/miniforge3/envs/bio/bin/RNAinverse`
- **Reference**: See `references/help.md` for full option details

## When To Use This Tool

- Design sequences that fold into a target dot-bracket structure.
- Explore inverse-folding solutions instead of evaluating one fixed sequence.
- Hold some nucleotides fixed while randomizing the rest.
- Repeat the search many times to obtain alternative candidate sequences.

## Common Patterns

```bash
# 1) Search from an all-N random starting sequence
printf '(((...)))\nNNNNNNNNN\n@\n' | RNAinverse
```

```bash
# 2) Repeat the inverse-folding search multiple times
printf '(((...)))\nNNNNNNNNN\n@\n' | RNAinverse -R 20
```

```bash
# 3) Keep selected nucleotides fixed by using lowercase letters
printf '(((...)))\nNNaaNNNNN\n@\n' | RNAinverse
```

## Recommended Workflow

1. Prepare target structure(s) in bracket notation and optional starting sequence(s)
2. Run `RNAinverse` with appropriate flags (e.g., `-R` for repeated search, `-Fp` for partition function mode)
3. Pipe or type structure and sequence pairs to stdin; use `@` or EOF to end input
4. Review output: best sequence found, Hamming distance, and structure distance if unsuccessful

## Guardrails

- Input structures must be valid bracket notation; malformed input causes unpredictable behavior
- A starting sequence of "N"s or a blank line randomizes the search; lowercase letters are held fixed
- Unsuccessful searches append a structure distance; verify output matches target structure before use

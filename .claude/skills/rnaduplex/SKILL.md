---
name: rnaduplex
description: Use when computing optimal and suboptimal secondary structures for hybridization of two RNA strands, such as probe-target binding predictions.
disable-model-invocation: true
user-invocable: true
---

# rnaduplex

## Quick Start

- **Command**: `RNAduplex [OPTION]... < input.fa`
- **Local executable**: `/home/vimalinx/miniforge3/envs/bio/bin/RNAduplex`
- **Full reference**: See [`references/help.md`](references/help.md) for complete options and model details

## When To Use This Tool

- Use `RNAduplex` when you want the hybridization structure between two RNA strands and only care about **inter-molecular** base pairs.
- It is especially suited to probe-target style questions, such as a short RNA or oligo against a longer target.
- Use `-e` when you need near-optimal alternative duplexes, not just the best-scoring interaction.
- Do not use it as a general cofolding tool when each strand may also form substantial intra-molecular structure; that is outside its simplified model.

## Common Patterns

```bash
# Predict the best duplex for two sequences from stdin
printf 'GGGAAAUCC\nGGAUUUCCC\n' | RNAduplex

# Enumerate suboptimal duplexes within 2 kcal/mol of the optimum
printf 'GGGAAAUCC\nGGAUUUCCC\n' | RNAduplex -e 2

# Sort reported duplexes by free energy
printf 'GGGAAAUCC\nGGAUUUCCC\n' | RNAduplex -e 2 -s

# Recalculate hybridization under a different temperature
printf 'GGGAAAUCC\nGGAUUUCCC\n' | RNAduplex -T 25
```

## Recommended Workflow

1. Prepare two RNA sequences as input (stdin or file), noting that "T" is auto-converted to "U" unless `--noconv` is set
2. Run `RNAduplex` with relevant options (e.g., `-s` to sort by free energy, `-e <range>` for suboptimal structures within an energy range)
3. Parse the output: dot-bracket structure with `&` separating strands, position ranges (from,to : from,to), and energy in kcal/mol
4. Adjust model parameters if needed (e.g., `-T` for temperature, `--salt` for salt concentration, `-P` for custom energy parameters)

## Guardrails

- For general cases requiring intra-molecular base pairs, use `RNAcofold` instead
- Default temperature is 37°C and salt concentration is 1.021M; adjust for non-physiological conditions
- Only inter-molecular base pairs are considered; this tool is optimized for probe-target scenarios

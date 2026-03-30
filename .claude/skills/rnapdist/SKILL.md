---
name: rnapdist
description: Use when calculating structure distances between thermodynamic ensembles of RNA secondary structures from sequence input.
disable-model-invocation: true
user-invocable: true
---

# rnapdist

## Quick Start

- **Command:** `RNApdist [OPTION]...` — reads RNA sequences from stdin
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/RNApdist`
- **Full reference:** See [`references/help.md`](references/help.md) for all options and details

## When To Use This Tool

- Use `RNApdist` when you need to compare RNA sequences by the distance between their **thermodynamic structure ensembles**, not by sequence identity alone.
- It is useful for asking whether two RNAs have similar folding landscapes even if their minimum-free-energy structures are not identical.
- Switch comparison mode with `-X` when you need a specific ensemble-distance definition for your analysis.
- Use `-B` when you want a profile-style alignment output in addition to the distance values.

## Common Patterns

```bash
# Compare two or more sequences from stdin using the default profile distance
printf 'GGGAAAUCC\nGGAAAUUCC\n' | RNApdist

# Use an alternative comparison directive
printf 'GGGAAAUCC\nGGAAAUUCC\n' | RNApdist -X m

# Emit a backtracked profile alignment to a file
printf 'GGGAAAUCC\nGGAAAUUCC\n' | RNApdist -B profiles.txt

# Recompute ensemble distances at a different temperature
printf 'GGGAAAUCC\nGGAAAUUCC\n' | RNApdist -T 25
```

## Recommended Workflow

1. Prepare input RNA sequences (FASTA or plain format) for comparison
2. Select comparison mode with `-X` (`p`, `m`, `f`, or `c`; default is `p`)
3. Run `RNApdist` with appropriate options (e.g., `-T` for temperature, `--salt` for salt concentration)
4. Review distance output; optionally use `-B` to generate aligned structure profiles

## Guardrails

- Input is read from stdin; ensure sequences are provided via pipe or redirect
- Default temperature is 37°C and salt concentration is 1.021M; adjust with `-T` and `--salt` if needed
- Nucleotide "T" is automatically converted to "U" unless `--noconv` is specified

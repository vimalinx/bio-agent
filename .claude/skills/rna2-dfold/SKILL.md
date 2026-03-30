---
name: rna2-dfold
description: Use when computing MFE structures, partition functions, and Boltzmann-sampled secondary structures within k,l distance neighborhoods relative to two reference structures for an RNA sequence.
disable-model-invocation: true
user-invocable: true
---

# rna2-dfold

## Quick Start

- **Command:** `RNA2Dfold [OPTIONS] < sequence_with_two_structures`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/RNA2Dfold`
- **Full reference:** See [`references/help.md`](references/help.md) for complete options and model details

## When To Use This Tool

- Partition RNA secondary structure space by base-pair distance to two reference structures.
- Compare alternative folding neighborhoods around two candidate conformations for the same RNA.
- Compute MFE representatives and, with `-p`, ensemble statistics for each `(k,l)` distance class.
- Sample structures from specific neighborhoods with stochastic backtracking.

## Common Patterns

```bash
# 1) Compute MFE representatives and partition-function statistics
cat <<'EOF' | RNA2Dfold -p
GGGAAAUCC
(((...)))
((.....))
EOF
```

```bash
# 2) Restrict the explored distance range to both references
cat input.txt | RNA2Dfold -p -K 10 -L 10
```

```bash
# 3) Backtrack samples from one specific neighborhood
cat input.txt | RNA2Dfold -p --stochBT=100 --neighborhood=3:5
```

## Recommended Workflow

1. Prepare input: an RNA sequence plus two reference structures in dot-bracket notation
2. Run `RNA2Dfold -p` to compute partition function and Gibbs free energy for each k,l neighborhood
3. Use `--stochBT=INT` to generate Boltzmann samples from specified neighborhoods
4. Analyze MFE representatives and sampled structures across distance classes

## Guardrails

- Requires exactly two reference structures in dot-bracket notation as input alongside the sequence
- Distance bounds `-K` and `-L` must accommodate the desired neighborhood range
- `--stochBT` only makes sense together with `-p`

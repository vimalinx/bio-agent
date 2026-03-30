---
name: rnapkplex
description: Use when searching an RNA sequence for pseudoknot-forming interactions by combining local accessibility with interaction energy, especially when ordinary pseudoknot-free folding is insufficient.
disable-model-invocation: true
user-invocable: true
---

# rnapkplex

## Quick Start

- **Command**: `RNAPKplex [OPTIONS] < input.fasta`
- **Local executable**: `/home/vimalinx/miniforge3/envs/bio/bin/RNAPKplex`
- **Full reference**: See `references/help.md` for complete options and details

## When To Use This Tool

- Use `RNAPKplex` when pseudoknots are central to the structural hypothesis and pseudoknot-free RNA folding tools are not sufficient.
- It is useful for flagging putative pseudoknot sites by combining local accessibility with interaction energy gain.
- Use the probability cutoff `-c` to suppress weakly accessible candidate sites and `-e` to demand stronger pseudoknot stabilization.
- Use `-s` when you want near-optimal pseudoknot alternatives instead of only the best one.

## Common Patterns

```bash
# Basic pseudoknot search from stdin
printf '>seq\nGGGAAAUCCCUUU\n' | RNAPKplex

# Require stronger energy gain before reporting pseudoknots
printf '>seq\nGGGAAAUCCCUUU\n' | RNAPKplex -e -10

# Filter low-accessibility candidate regions
printf '>seq\nGGGAAAUCCCUUU\n' | RNAPKplex -c 1e-4

# Include near-optimal suboptimal pseudoknot solutions
printf '>seq\nGGGAAAUCCCUUU\n' | RNAPKplex -s 2
```

## Recommended Workflow

1. Prepare input RNA sequence in FASTA format
2. Run `RNAPKplex` with default parameters to identify potential pseudoknots
3. Adjust `-e` (energy cutoff) or `-c` (probability cutoff) to filter results as needed
4. Use `-s` to explore suboptimal structures within a specified energy range

## Guardrails

- Algorithm uses O(n^2*w^4) CPU time and O(n*w^2) memory; avoid very long sequences
- Always uses dangle=2 model; this cannot be configured
- Default energy cutoff is -8.10 kcal/mol; pseudoknots with less favorable energy gains are rejected
- The skill name is `rnapkplex`, but the actual executable is capitalized as `RNAPKplex`

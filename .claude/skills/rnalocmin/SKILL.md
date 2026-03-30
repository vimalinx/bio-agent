---
name: rnalocmin
description: Use when analyzing RNA secondary structure landscapes to find local minima via gradient walks, generate barrier trees, or compute rates for kinetic modeling with treekin.
disable-model-invocation: true
user-invocable: true
---

# rnalocmin

## Quick Start

- **Command**: `RNAlocmin [OPTION]... [FILE]...`
- **Local executable**: `/home/vimalinx/miniforge3/envs/bio/bin/RNAlocmin`
- **Full reference**: See [references/help.md](references/help.md) for complete options and details

## When To Use This Tool

- Collapse a sampled RNA structure ensemble into local minima by gradient walks.
- Build barrier-tree-like summaries from `RNAsubopt` output.
- Produce kinetic landscape inputs for `treekin`.
- Filter minima by basin depth or energy-barrier criteria.

## Common Patterns

```bash
# 1) Derive local minima from sampled suboptimal structures
RNAsubopt -p 10000 < sequence.txt > suboptp.txt
RNAlocmin -s sequence.txt < suboptp.txt > locmin.txt
```

```bash
# 2) Emit barrier-tree style output
RNAlocmin -s sequence.txt -b < suboptp.txt > barriers.txt
```

```bash
# 3) Keep only minima above a barrier threshold
RNAlocmin -s sequence.txt --minh 1.5 < suboptp.txt > filtered_minima.txt
```

## Recommended Workflow

1. Generate sampled structures using `RNAsubopt -p <count> < sequence.txt > suboptp.txt`
2. Run `RNAlocmin -s sequence.txt < suboptp.txt` to compute local minima via gradient descent
3. Add `-b` for barrier tree output or `-r` for rates generation if kinetic analysis is needed
4. Filter results with `--minh` to report only minima exceeding a specified energy barrier threshold

## Guardrails

- Requires structure input from stdin (typically from RNAsubopt); sequence file via `-s` is optional if sequence is first line of input
- Do not combine `--noLP` with random walk (`-w R`) or shift move set (`-m S`)
- Use `-p` to provide previously found local minima output instead of recomputing from sequence

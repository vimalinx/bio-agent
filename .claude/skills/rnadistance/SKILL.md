---
name: rnadistance
description: Use when calculating distances between RNA secondary structures, including base pair distance and tree or string editing-based dissimilarity measures.
disable-model-invocation: true
user-invocable: true
---

# rnadistance

## Quick Start

- **Command**: `RNAdistance [OPTION]...`
- **Local executable**: `/home/vimalinx/miniforge3/envs/bio/bin/RNAdistance`
- **Full reference**: See [references/help.md](references/help.md) for complete options

## When To Use This Tool

- Quantify how different two RNA secondary structures are.
- Compare structures with base-pair distance or tree/string-edit representations.
- Switch to Shapiro's coarse-grained cost matrix with `-S` when you care about abstract motifs.
- Emit aligned backtracks to inspect which substructures match.

## Common Patterns

```bash
# 1) Compute default distances between two structures from stdin
printf '(((...)))\n((.....))\n' | RNAdistance
```

```bash
# 2) Choose a specific distance representation
printf '(((...)))\n((.....))\n' | RNAdistance -D f -X p
```

```bash
# 3) Write an aligned backtrack to a file
printf '(((...)))\n((.....))\n' | RNAdistance -B=alignment.txt
```

## Recommended Workflow

1. Prepare RNA secondary structure inputs to compare
2. Select distance representation with `-D` (default `f`) and comparison directive with `-X` (default `p`)
3. Run `RNAdistance` with structures via stdin, optionally enabling `-S` for Shapiro's cost matrix or `-B` for backtrack output
4. Interpret distance values; use backtracking output to visualize structural matches

## Guardrails

- Do not use base pair distance for structures of different lengths (not recommended per documentation)
- Provide RNA secondary structures via stdin before invoking
- Specify output filename with `-B=<filename>` if alignment/backtrack output is needed

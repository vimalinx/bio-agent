---
name: rnalfold
description: Use when computing locally stable RNA secondary structures with a maximal base pair span, scanning large genomes for short RNA structures, or predicting local RNA folding with Z-score filtering.
disable-model-invocation: true
user-invocable: true
---

# rnalfold

## Quick Start

- **Command**: `RNALfold`
- **Local executable**: `/home/vimalinx/miniforge3/envs/bio/bin/RNALfold`
- **Full reference**: `references/help.md`

## When To Use This Tool

- Search one long RNA for locally stable structural elements.
- Limit folding to a maximum base-pair span instead of computing one global fold.
- Filter local hits by Z-score when you need stronger statistical support.
- Generate compact local-structure calls for genome-scale scans.

## Common Patterns

```bash
# 1) Scan a sequence from stdin with default span
echo 'GGGAAAUCCGGGAAAUCC' | RNALfold
```

```bash
# 2) Restrict the maximal base-pair span
echo 'GGGAAAUCCGGGAAAUCC' | RNALfold -L 100
```

```bash
# 3) Report only strongly supported local structures
echo 'GGGAAAUCCGGGAAAUCC' | RNALfold -L 120 -z -2.5
```

## Recommended Workflow

1. Prepare input RNA sequence file or pipe sequence via stdin
2. Run `RNALfold` with appropriate `-L` span value for your use case
3. Optionally apply `-z` for Z-score filtering or `--shape` for SHAPE-guided prediction
4. Review output listing local structures, energies, and starting positions

## Guardrails

- Verify input sequences are valid RNA/DNA (T is auto-converted to U unless `--noconv` is set)
- The `-L` span parameter directly affects memory and CPU usage; larger values increase resource demands
- Output may contain overlapping or subsumed structures; use Z-score options to filter results

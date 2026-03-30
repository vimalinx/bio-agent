---
name: analyse-dists
description: Use when passing legacy ViennaRNA distance-matrix data through the AnalyseDists helper for simple formatting or downstream plotting workflows.
disable-model-invocation: true
user-invocable: true
---

# analyse-dists

Legacy ViennaRNA helper around stdin distance-matrix data. The skill name is lowercase, but the real executable is the capitalized binary `AnalyseDists`.

## Quick Start

- **Skill name:** `analyse-dists`
- **Real executable:** `AnalyseDists`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/AnalyseDists`

## When To Use This Tool

- Pass an existing distance matrix through a ViennaRNA helper without writing a custom parser.
- Keep a legacy ViennaRNA workflow that expects `AnalyseDists` / `AnalyseDist` style post-processing.
- Toggle the old compact `-X[swn]` modifier family on matrix-style stdin data.
- Use this only when you already have distance-matrix text; it is not a sequence aligner or structure predictor.

## Common Patterns

```bash
# 1) Feed a small matrix on stdin
printf '0 1\n1 0\n' |
PATH=/home/vimalinx/miniforge3/envs/bio/bin:$PATH \
AnalyseDists
```

```bash
# 2) Apply one of the legacy -X modifiers while keeping stdin-based usage
printf '0 1\n1 0\n' |
PATH=/home/vimalinx/miniforge3/envs/bio/bin:$PATH \
AnalyseDists -Xn
```

## Recommended Workflow

1. Prepare the distance matrix upstream and keep it available on stdin, because the usage string advertises no positional input file.
2. Invoke the real binary name `AnalyseDists`, not the lowercase skill folder name.
3. Smoke-test the matrix without modifiers first, then add `-Xs`, `-Xw`, or `-Xn` only if your downstream tool actually depends on them.
4. Compare stdout on a tiny matrix before trusting the transformation on large datasets.

## Guardrails

- The executable name and the skill name do not match: the binary is `AnalyseDists`, and the embedded usage text even says `AnalyseDist` in the singular.
- `-h`, `--help`, and `--version` do not produce clean metadata output here; they all collapse to the same `[ERROR]   usage: AnalyseDist [-X[swn]]` path.
- Live smoke tests with a tiny `2 x 2` matrix simply echoed the matrix back on stdout, both with no flags and with `-Xn`, so validate that the chosen modifier actually changes what you need.
- Local evidence only confirms the compact `-X[swn]` family from the usage string; option semantics beyond that were not recoverable from runnable help.

---
name: esl-weight
description: Use when adding Stockholm sequence-weight annotations to nucleotide or protein MSAs before downstream HMMER-style modeling.
disable-model-invocation: true
user-invocable: true
---

# esl-weight

## Quick Start

- **Command:** `esl-weight [options] <msafile>`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/esl-weight`
- **Full reference:** See `references/help.md` for the current startup failure; option details below are grounded in the local man page plus binary strings.

## When To Use This Tool

- Use `esl-weight` when you need per-sequence weights written back into a multiple alignment as Stockholm `#=GS <seqname> WT <weight>` annotation.
- It is useful before downstream profile-model building or when you want an explicit, inspectable weighted alignment artifact.
- Reach for `-g` for Gerstein/Sonnhammer/Chothia weights, `-p` for Henikoff position-based weights, or `-b` for BLOSUM-style cluster weights.

## Common Patterns

```bash
# Default Gerstein/Sonnhammer/Chothia weighting
esl-weight alignment.sto > weighted.sto

# Faster Henikoff position-based weighting
esl-weight -p alignment.sto > pb-weighted.sto

# BLOSUM-style clustering weights at a chosen identity threshold
esl-weight -b --id 0.70 alignment.sto > blosum70.sto

# Force protein alphabet when autodetection is ambiguous
esl-weight --amino alignment.sto > weighted-aa.sto
```

## Recommended Workflow

1. Fix the local shared-library issue first so the binary can start.
2. Prepare the input multiple alignment and force the alphabet with `--amino`, `--dna`, or `--rna` if autodetection could be ambiguous.
3. Choose the weighting rule that matches the downstream method.
4. Inspect the emitted Stockholm alignment and confirm `#=GS ... WT` lines are present.
5. Feed the weighted alignment into the next modeling step only after the annotations look plausible.

## Guardrails

- The local executable currently fails to start because `libopenblas.so.0` is missing. Until that library issue is fixed, `-h` and live runtime validation are unavailable.
- Despite the startup failure, the local man page documents `-g` as the default, `-p` as Henikoff position-based weighting, and `-b` as BLOSUM-style clustering weights.
- `--id <x>` only applies with `-b`; the documented default threshold is `0.62`.
- Output is written in Stockholm format with `WT` annotations even if the input alignment came from another accepted format.
- Option details here are intentionally conservative because the current environment cannot execute the binary end-to-end.

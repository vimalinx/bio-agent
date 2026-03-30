---
name: kinwalker
description: Use when simulating RNA folding kinetics during transcription to predict cotranscriptional folding pathways and transient intermediate structures.
disable-model-invocation: true
user-invocable: true
---

# kinwalker

## Quick Start

- **Command**: `kinwalker [OPTIONS] < SeqFile > Outfile`
- **Local executable**: `/home/vimalinx/miniforge3/envs/bio/bin/kinwalker`
- **Full reference**: `references/help.md`

## When To Use This Tool

- Model cotranscriptional RNA folding while the chain is still elongating.
- Compare different barrier heuristics for transient folding pathways.
- Tune transcription rate and folding window size to match a biological regime.
- Produce a trajectory-oriented kinetics prediction rather than an equilibrium ensemble.

## Common Patterns

```bash
# 1) Run a basic cotranscriptional folding simulation
kinwalker < seq.txt > trajectory.txt
```

```bash
# 2) Change the barrier heuristic and transcription rate
kinwalker --barrier_heuristic B --transcription_rate 50 < seq.txt > trajectory.txt
```

```bash
# 3) Constrain the folding window and disable lonely pairs
kinwalker --windowsize 120 --nolonely 1 < seq.txt > trajectory.txt
```

## Recommended Workflow

1. Prepare sequence input file with target RNA sequence
2. Select barrier heuristic via `--barrier_heuristic` (M/S/B/A; default: M for Morgan-Higgs)
3. Set transcription parameters (`--transcription_rate`, `--transcribed`, `--windowsize`) to match biological conditions
4. Run kinwalker, redirect output to file, and review predicted folding trajectory

## Guardrails

- Does not support `--version`; use `--help` to verify installation
- Input read from SeqFile or stdin; output written to Outfile or stdout
- ViennaRNA parameters (`--dangle`, `--nolonely`) should be consistent with any upstream/downstream ViennaRNA tools

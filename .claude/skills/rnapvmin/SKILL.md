---
name: rnapvmin
description: Use when working with RNA soft constraints and need to compute pairing probabilities with position-specific perturbation minimization from the ViennaRNA package.
disable-model-invocation: true
user-invocable: true
---

# rnapvmin

## Quick Start

- **Command:** `RNApvmin [options] [input_file]`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/RNApvmin`
- **Full reference:** See `references/help.md` for complete options and usage details

## When To Use This Tool

- Infer a perturbation vector that reconciles predicted pairing probabilities with experimental SHAPE-derived probabilities.
- Generate soft-constraint inputs for downstream ViennaRNA folding runs.
- Optimize per-position perturbations instead of hard-coding one SHAPE transformation.
- Study how strongly experimental probing data must bias the folding model.

## Common Patterns

```bash
# 1) Compute a perturbation vector from a sequence on stdin plus a SHAPE file
echo 'GGGAAAUCC' | RNApvmin observations.shape > perturbation.txt
```

```bash
# 2) Choose a specific SHAPE-to-probability conversion model
echo 'GGGAAAUCC' | RNApvmin --shapeConversion=O observations.shape > perturbation.txt
```

```bash
# 3) Tune the optimization with more samples and a custom tau/sigma ratio
echo 'GGGAAAUCC' | RNApvmin --sampleSize=1000 --tauSigmaRatio=1.0 observations.shape > perturbation.txt
```

## Recommended Workflow

1. Prepare your RNA sequence input in the appropriate format
2. Run `RNApvmin` with required options (see `references/help.md` for available parameters)
3. Capture the output pairing probabilities or constraint data
4. Use the output as soft constraints in downstream RNA structure prediction tools

## Guardrails

- In this environment the binary currently fails to start because `libopenblas.so.0` is missing, so live help/version output is unavailable until that dependency is fixed.
- The sequence is read from stdin, while the positional argument is a SHAPE file whose lines must look like `[position] [nucleotide] [absolute_shape_reactivity]`.
- Use conservative language when documenting this tool: some option details here come from binary strings rather than successful runtime help.

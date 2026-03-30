---
name: rnaalifold
description: Use when predicting consensus secondary structures from multiple sequence alignments of RNA. Computes minimum free energy structures, partition functions, and base pairing probabilities for aligned RNA sequences.
disable-model-invocation: true
user-invocable: true
---

# rnaalifold

## Quick Start

- **Command**: `RNAalifold [options] <input.aln>`
- **Local executable**: `/home/vimalinx/miniforge3/envs/bio/bin/RNAalifold`
- **Full reference**: See [references/help.md](references/help.md) for complete options and details

## When To Use This Tool

- Predict a consensus secondary structure from an RNA multiple sequence alignment.
- Add ensemble probabilities with `-p` instead of relying on MFE alone.
- Quantify structural conservation with `--sci`.
- Generate alignment-wide structure and dot-plot outputs from one run.

## Common Patterns

```bash
# 1) Predict the consensus MFE structure from an alignment
RNAalifold family.aln
```

```bash
# 2) Add partition function and pairing probabilities
RNAalifold -p family.aln
```

```bash
# 3) Compute SCI for a conserved alignment
RNAalifold -p --sci family.aln > alifold.txt
```

## Recommended Workflow

1. Prepare input alignment in CLUSTAL, Stockholm, FASTA, or MAF format
2. Run basic consensus prediction: `RNAalifold alignment.aln`
3. Add partition function for probabilities: `RNAalifold -p alignment.aln`
4. Review output files: `alirna.ps` (structure), `alidot.ps` (dot plot), `alifold.out` (credibility-sorted pair list)

## Guardrails

- Input must be a valid multiple sequence alignment in CLUSTAL, Stockholm, FASTA, or MAF format
- Avoid mixing very similar and dissimilar sequences; duplicate sequences can distort predictions
- Output files overwrite existing files of the same name in the current directory

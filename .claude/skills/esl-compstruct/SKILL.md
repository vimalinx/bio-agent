---
name: esl-compstruct
description: Use when comparing two Stockholm format files with secondary structure markup to evaluate how well a test structure matches a trusted reference.
disable-model-invocation: true
user-invocable: true
---

# esl-compstruct

Compares trusted and test secondary structure annotations in Stockholm format files, reporting agreement metrics.

## Quick Start

- **Command:** `esl-compstruct [-options] <trusted file> <test file>`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/esl-compstruct`
- **Full reference:** See `references/help.md`

## When To Use This Tool

- Use `esl-compstruct` when comparing predicted RNA secondary structure annotation against a trusted reference.
- It is appropriate for Stockholm files carrying WUSS secondary-structure markup in the same sequence order.
- Use `-m` if you want Mathews-style relaxed matching that tolerates a one-position slip.
- Reach for `-p` when pseudoknotted base pairs should be included in the evaluation.

## Common Patterns

```bash
# Compare a predicted structure set against a trusted reference
esl-compstruct trusted.sto test.sto

# Allow Mathews-style relaxed correctness
esl-compstruct -m trusted.sto test.sto

# Include pseudoknotted base pairs in the comparison
esl-compstruct -p trusted.sto test.sto

# Suppress the verbose header for cleaner output
esl-compstruct --quiet trusted.sto test.sto
```

## Recommended Workflow

1. Prepare your trusted Stockholm file with secondary structure markup in WUSS notation
2. Prepare your test Stockholm file with the same sequences in the same order
3. Run `esl-compstruct <trusted file> <test file>` to compare structures
4. Review output metrics to assess prediction accuracy

## Guardrails

- Both input files must be in Stockholm format with secondary structure markup
- Sequences must appear in the same order in both files
- Structure markup must use WUSS notation; use `esl-compstruct -h` for option details
- `-p` changes the evaluation surface by counting pseudoknotted pairs, so results are not directly comparable to default runs

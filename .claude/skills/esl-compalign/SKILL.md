---
name: esl-compalign
description: Use when comparing a test multiple sequence alignment against a trusted reference alignment to compute accuracy. Requires Stockholm format files with #=GC RF markup.
disable-model-invocation: true
user-invocable: true
---

# esl-compalign

## Quick Start
- **Command**: `esl-compalign [-options] <trusted file> <test file>`
- **Local executable**: `/home/vimalinx/miniforge3/envs/bio/bin/esl-compalign`
- **Full reference**: See `references/help.md`

## When To Use This Tool

- Use `esl-compalign` when evaluating a test alignment against a trusted reference alignment.
- It is appropriate for benchmark or method-comparison workflows where both alignments are in Stockholm format with RF annotation.
- Use `-c` when you want per-column statistics and `-p` when comparing alignment accuracy against posterior probability information.
- Reach for it when you need an explicit quantitative comparison of alignment quality rather than just visual inspection.

## Common Patterns

```bash
# Compare a test alignment against a trusted alignment
esl-compalign trusted.sto test.sto

# Emit per-column statistics instead of per-sequence statistics
esl-compalign -c trusted.sto test.sto

# Compare accuracy as a function of posterior probability
esl-compalign -p trusted.sto test.sto

# Write column-wise stats in ssdraw-compatible format
esl-compalign -c --c2dfile compalign.dfile trusted.sto test.sto
```

## Recommended Workflow
1. Prepare trusted and test alignments in Stockholm format with #=GC RF markup
2. Verify sequences appear in identical order in both files
3. Confirm #=GC RF markup has identical number of non-gap characters in both files
4. Run `esl-compalign <trusted file> <test file>` to compute accuracy

## Guardrails
- Both files must be in Stockholm format with #=GC RF markup
- Sequences must occur in the same order in the two files
- Number of non-gap characters in #=GC RF markup must be identical between files
- `-p` only makes sense when posterior probability annotation exists in the tested alignment context

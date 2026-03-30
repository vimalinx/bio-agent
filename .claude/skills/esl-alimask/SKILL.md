---
name: esl-alimask
description: Use when you need to mask columns in a multiple sequence alignment using gap frequencies, posterior probabilities, external mask files, or the RF annotation, or to truncate alignments to specific coordinate ranges.
disable-model-invocation: true
user-invocable: true
---

# esl-alimask

## Quick Start

- **Command:** `esl-alimask [options] <msafile> ...`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/esl-alimask`
- **Detailed reference:** See `references/help.md` for full option list and usage details

## When To Use This Tool

- Use `esl-alimask` when you need to remove or retain alignment columns based on an explicit mask, coordinate range, gap fraction, posterior probability, or RF annotation.
- It is appropriate for MSA cleanup before HMM building, consensus trimming, or downstream comparative analyses.
- Use `-t` for coordinate-based trimming, `-g` for gap-based masking, and `-p` for posterior-probability-based masking.
- Reach for `--rf-is-mask` when the alignment already carries a trusted `#=GC RF` annotation defining the columns to keep.

## Common Patterns

```bash
# Keep only columns 23..100 of an alignment
esl-alimask -t alignment.sto 23..100 > trimmed.sto

# Mask columns with too many gaps
esl-alimask -g --gapthresh 0.3 alignment.sto > gapmasked.sto

# Mask using posterior probabilities
esl-alimask -p --pavg 0.9 alignment.sto > ppmasked.sto

# Apply an explicit 0/1 mask file
esl-alimask alignment.sto mask.txt > masked.sto
```

## Recommended Workflow

1. Prepare your MSA file in a supported format (e.g., Stockholm, aligned FASTA)
2. Choose a masking strategy: external mask file, gap-based, posterior probability-based, or RF annotation
3. Run `esl-alimask` with the appropriate mode flag (`-t`, `-g`, `-p`, or `--rf-is-mask`) or provide a mask file
4. Verify the output alignment has the expected columns masked or truncated

## Guardrails

- Use `-h` for help; `--help` and `--version` are not supported options
- Ensure the MSA file format matches the expected input (check with Easel tools if needed)
- When using `-t`, provide coordinates in the correct format and range for the alignment
- `-g` and `-p` can be combined, but the other major usage modes are mutually exclusive

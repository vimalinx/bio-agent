---
name: esl-mask
description: Use when applying coordinate-based masks to named sequences in FASTA or other Easel-supported sequence files.
disable-model-invocation: true
user-invocable: true
---

# esl-mask

## Quick Start

- **Command:** `esl-mask [options] <sqfile> <maskfile>`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/esl-mask`
- **Full reference:** See `references/help.md` for detailed options (run `esl-mask -h`)

## When To Use This Tool

- Use `esl-mask` when you have named sequences plus a coordinate table describing which residues to mask or keep.
- It is useful for masking low-confidence intervals, trimming flanks, hiding specific motif regions, or generating region-only views with reverse masking.
- Reach for `-l` to lowercase masked residues instead of replacing them, or `-m <c>` to mask with a custom character such as `N` or `X`.
- Use `-R` when your mask file is not in the exact same order as the sequence file and you have an SSI index available.

## Common Patterns

```bash
# Mask listed regions with the default X character
esl-mask sequences.fa mask.tsv > masked.fa

# Lowercase the masked residues instead of replacing them
esl-mask -l sequences.fa mask.tsv > masked-lower.fa

# Keep only the listed region and mask everything else
esl-mask -r sequences.fa keep-regions.tsv > region-only.fa

# Random-access masking from an SSI-indexed sequence file, padding each region by 5 nt
esl-mask -R -x 5 -m N sequences.fa mask.tsv > padded.fa
```

## Recommended Workflow

1. Prepare a supported sequence file such as FASTA, EMBL, GenBank, or another Easel-recognized format.
2. Build a mask file with at least three whitespace-delimited fields per line: sequence name, 1-based start, and 1-based end.
3. Decide whether you want normal masking, reverse masking (`-r`), lowercasing (`-l`), or a replacement character (`-m`).
4. If mask rows are not aligned to the sequence-file order, create an SSI index with `esl-sfetch --index` and rerun with `-R`.
5. Inspect output around interval boundaries, especially if you used `-x` to extend masked regions.

## Guardrails

- The mask file uses 1-based inclusive coordinates and ignores blank lines plus `#` comments.
- By default, sequence names must appear in the same order and number in both files; `-R` is the escape hatch, but it requires an `.ssi` index.
- `-r` masks everything outside `start..end`, not the interval itself.
- `-h` works; `--help` and `--version` are rejected by the local executable.
- `-x <n>` extends masking by up to `n` residues on both sides, which can change behavior near sequence ends.

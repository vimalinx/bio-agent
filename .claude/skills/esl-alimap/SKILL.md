---
name: esl-alimap
description: Use when comparing or mapping two multiple sequence alignments in Stockholm format to analyze their overlap or relationship.
disable-model-invocation: true
user-invocable: true
---

# esl-alimap

## Quick Start

- **Command:** `esl-alimap [options] <msafile1> <msafile2>`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/esl-alimap`
- **Full reference:** See `references/help.md` for detailed options (via `esl-alimap -h`)

## When To Use This Tool

- Use `esl-alimap` when you need to map columns or RF positions between two related Stockholm alignments.
- It is useful for tracking how one alignment corresponds to another after trimming, masking, or subalignment extraction.
- Use it when you want 0/1 masks that project alignment columns or RF positions from one MSA onto another.
- Reach for `--submap` when the second alignment is known to be a strict subalignment of the first.

## Common Patterns

```bash
# Print a column-by-column mapping between two Stockholm alignments
esl-alimap aln1.sto aln2.sto

# Suppress verbose per-column mapping and just emit summary information
esl-alimap -q aln1.sto aln2.sto

# Write a mask describing aln1 columns that map to aln2 RF positions
esl-alimap --mask-a2rf aln1_to_aln2.mask aln1.sto aln2.sto

# Generate a subalignment mask when aln2 is a subalignment of aln1
esl-alimap --submap sub.mask aln1.sto aln2.sto
```

## Recommended Workflow

1. Prepare two MSAs in Stockholm format (required input format)
2. Run `esl-alimap [options] <msafile1> <msafile2>` with desired options
3. Review output to understand alignment mapping relationship
4. Use results to guide downstream comparative alignment analysis

## Guardrails

- Both input files must be in Stockholm format
- Use `-h` for help (not `--help` or `--version`, which are unsupported)
- Ensure both alignments contain related sequences for meaningful mapping
- If alphabet guessing is ambiguous, force it with `--amino`, `--dna`, or `--rna`

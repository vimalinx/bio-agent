---
name: esl-afetch
description: Use when retrieving specific multiple sequence alignments from an MSA file by name, or when indexing MSA files for faster access.
disable-model-invocation: true
user-invocable: true
---

# esl-afetch

Tool from the HMMER suite for extracting named alignments from multiple sequence alignment files.

## Quick Start

- **Command:** `esl-afetch [options] <msafile> <name>`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/esl-afetch`
- **Full reference:** See `references/help.md` for complete options and usage details

## When To Use This Tool

- Use `esl-afetch` when you need to retrieve named alignments from a multi-alignment file.
- It is the alignment analogue of `esl-sfetch`: index once, then pull one or many alignments by key.
- Use `-f` for batch extraction and `--outformat` when the fetched alignments should be rewritten in another alignment format.
- It is useful when building alignment subsets or extracting specific families from large Stockholm/Pfam-style collections.

## Common Patterns

```bash
# Index an MSA file
esl-afetch --index families.sto

# Fetch one named alignment
esl-afetch families.sto PF00001 > PF00001.sto

# Fetch many named alignments listed in a file
esl-afetch -f families.sto ids.txt > subset.sto

# Fetch and rewrite in aligned FASTA format
esl-afetch --outformat afa families.sto PF00001 > PF00001.afa
```

## Recommended Workflow

1. Verify your MSA file format and identify target alignment names
2. Optionally index large MSA files with `esl-afetch --index <msafile>` for faster access
3. Retrieve alignments using either single name or batch mode with `-f`
4. Validate extracted alignments contain expected sequences

## Guardrails

- Ensure alignment names match exactly as stored in the MSA file
- Use `-f` with a name file when retrieving multiple alignments efficiently
- Run `esl-afetch -h` for additional options (note: `--help` is not supported)
- `--index` creates an SSI sidecar and is the right first step for repeated lookups on large MSA collections

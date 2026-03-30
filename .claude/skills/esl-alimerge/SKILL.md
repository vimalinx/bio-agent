---
name: esl-alimerge
description: Use when merging multiple sequence alignment files in Stockholm or Pfam format into a single alignment.
disable-model-invocation: true
user-invocable: true
---

# esl-alimerge

## Quick Start

- **Command:** `esl-alimerge [options] <alignment file 1> <alignment file 2>`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/esl-alimerge`
- **Full reference:** See [references/help.md](references/help.md) for complete options

## When To Use This Tool

- Use `esl-alimerge` when you need to merge two or more related alignments using their RF annotation as the coordinate system.
- It is appropriate for Stockholm or Pfam alignments that represent compatible views of the same family or consensus space.
- Use `--list` when the merge spans more than two input alignment files.
- Reach for `--rfonly` when only RF-supported columns should survive in the merged result.

## Common Patterns

```bash
# Merge two Stockholm/Pfam alignments
esl-alimerge aln1.sto aln2.sto > merged.sto

# Merge many alignments listed in a file
esl-alimerge --list merge.list > merged.sto

# Write merged output in aligned FASTA format
esl-alimerge --outformat afa aln1.sto aln2.sto > merged.afa

# Keep only RF-supported columns in the merged alignment
esl-alimerge --rfonly aln1.sto aln2.sto > merged_rfonly.sto
```

## Recommended Workflow

1. Verify all input alignment files are in Stockholm or Pfam format
2. For two files, run `esl-alimerge [options] file1.sto file2.sto`
3. For more than two files, create a list file and run `esl-alimerge --list <listfile>`
4. Specify output format with relevant options if needed (stockholm is default)

## Guardrails

- Input files must be Stockholm or Pfam format only
- Use `-h` for additional help options; `--version` and `--help` are not supported
- Ensure all alignments being merged share compatible sequence naming conventions
- `-v` only makes sense together with `-o`, because the merge report goes to stdout otherwise

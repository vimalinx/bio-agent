---
name: bowtie2-inspect
description: Use when you need to extract reference sequences, names, or summary information from a Bowtie2 index file.
disable-model-invocation: true
user-invocable: true
---

# bowtie2-inspect

## Quick Start

- **Command**: `bowtie2-inspect [options] <bt2_base>`
- **Local executable**: `/home/vimalinx/miniforge3/envs/bio/bin/bowtie2-inspect`
- **Full reference**: See `references/help.md`

## When To Use This Tool

- Use `bowtie2-inspect` when you need to recover sequences, names, or metadata from an existing Bowtie 2 index basename.
- It is the generic inspector and is the right first choice when you are not manually forcing the small or large direct executable.
- Use `-n` for name-only output, `-s` for a summary, and the default mode when you want FASTA reconstructed from the index.
- Use `--large-index` if both small and large forms are present and you need to force inspection of the large index.

## Common Patterns

```bash
# Print a summary of the index
bowtie2-inspect -s ref

# List reference names only
bowtie2-inspect -n ref

# Recover FASTA from the index
bowtie2-inspect ref > ref_from_index.fa

# Force inspection of a large index
bowtie2-inspect --large-index -s ref_large
```

## Recommended Workflow

1. Verify the index base name (without `.1.bt2`/`.2.bt2` suffix)
2. Run `bowtie2-inspect -s <bt2_base>` to get a summary of the index
3. Use `-n` to list reference names only, or run without flags for FASTA output
4. Save output with `-o <filename>` or redirect to a file

## Guardrails

- Provide the bt2 base name without trailing `.1.bt2`/`.2.bt2` extensions
- Output goes to stdout by default; use `-o` or shell redirection to save
- Use `--large-index` only when forcing inspection of a large-format index

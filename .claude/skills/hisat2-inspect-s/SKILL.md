---
name: hisat2-inspect-s
description: Use when extracting metadata, reference names, SNPs, splice sites, or exon information from HISAT2 index files (.ht2).
disable-model-invocation: true
user-invocable: true
---

# hisat2-inspect-s

## Quick Start

- **Command**: `hisat2-inspect-s [options] <ht2_base>`
- **Local executable**: `/home/vimalinx/miniforge3/envs/bio/bin/hisat2-inspect-s`
- **Full reference**: See `references/help.md` for complete options and details

## When To Use This Tool

- Use `hisat2-inspect-s` when you know the target index is the standard HISAT2 small format (`.ht2`) and want to inspect that binary directly.
- It is useful for extracting sequence names, summaries, and embedded graph annotations from a small index without wrapper auto-selection.
- Use it when validating a small-index build or debugging annotation content in a standard HISAT2 index.
- For general use, `hisat2-inspect` remains the more flexible entry point.

## Common Patterns

```bash
# Summarize a standard HISAT2 index
hisat2-inspect-s -s genome

# List reference names only
hisat2-inspect-s -n genome

# Extract splice sites or exons embedded in the index
hisat2-inspect-s --ss genome > splicesites.txt
hisat2-inspect-s --exon genome > exons.txt

# Reconstruct FASTA from the index
hisat2-inspect-s -e genome > genome.fa
```

## Recommended Workflow

1. Identify the HISAT2 index base name (filename minus `.1.ht2`/`.2.ht2` suffix)
2. Run `hisat2-inspect-s -s <ht2_base>` to get a summary of index contents
3. Use `-n` for names only, or `--snp`/`--ss`/`--exon` for specific annotations
4. Redirect output to a file if extracting full FASTA sequences

## Guardrails

- Provide the index base name without the `.1.ht2`/`.2.ht2` extension
- Use `-e/--ht2-ref` sparingly; reconstructing references is slow
- Ensure the index files exist in the working directory or provide full paths
- The direct executable prints a wrapper-warning message; that warning is expected when calling `hisat2-inspect-s` directly

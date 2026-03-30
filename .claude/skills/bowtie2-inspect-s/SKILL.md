---
name: bowtie2-inspect-s
description: Use when you need to inspect Bowtie 2 index files to extract reference sequence names, lengths, or index summary information from .bt2 files.
disable-model-invocation: true
user-invocable: true
---

# bowtie2-inspect-s

## Quick Start

- **Command**: `bowtie2-inspect-s <bt2_base>`
- **Local executable**: `/home/vimalinx/miniforge3/envs/bio/bin/bowtie2-inspect-s`
- **Full reference**: See [references/help.md](references/help.md) for complete options

## When To Use This Tool

- Use `bowtie2-inspect-s` when you know the index is the standard Bowtie 2 small format (`.bt2`) and want to inspect that binary directly.
- It is useful for recovering sequence names, printing summaries, or reconstructing FASTA from a small index.
- Use it when you want to avoid ambiguity between small and large index formats during debugging or validation.
- In general-purpose workflows, `bowtie2-inspect` is still the better default entry point.

## Common Patterns

```bash
# Summarize a standard Bowtie 2 index
bowtie2-inspect-s -s ref

# List only reference names
bowtie2-inspect-s -n ref

# Reconstruct FASTA from the index
bowtie2-inspect-s ref > ref.fa

# Save summary output directly to a file
bowtie2-inspect-s -s ref -o ref.summary.txt
```

## Recommended Workflow

1. Identify the Bowtie 2 index base name (path without `.1.bt2`/`.2.bt2` suffix)
2. Run `bowtie2-inspect-s -s <bt2_base>` to print a summary including reference names, lengths, and index properties
3. Use `-n` to list only reference names, or omit flags for FASTA output
4. Save output to a file using `-o <filename>` or redirect stdout

## Guardrails

- Requires valid Bowtie 2 index files (`.bt2`) present at the specified base path
- The `<bt2_base>` argument must exclude trailing `.1.bt2`/`.2.bt2` extensions
- This is a direct executable; prefer the wrapper script if available
- The direct executable emits a wrapper warning message; that warning is normal when calling `bowtie2-inspect-s` directly

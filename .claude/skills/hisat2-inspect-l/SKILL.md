---
name: hisat2-inspect-l
description: Use when you need to inspect or extract information from HISAT2 large index files (.ht2l), including reference sequences, splice sites, SNPs, exons, or index summaries.
disable-model-invocation: true
user-invocable: true
---

# hisat2-inspect-l

## Quick Start

- **Command**: `hisat2-inspect-l [options] <ht2_base>`
- **Local executable**: `/home/vimalinx/miniforge3/envs/bio/bin/hisat2-inspect-l`
- **Full reference**: `references/help.md`

## When To Use This Tool

- Use `hisat2-inspect-l` when you know the target index is the large HISAT2 format (`.ht2l`) and want to inspect it directly.
- It is useful for debugging large-index builds, checking embedded SNP/splice/exon annotations, or reconstructing reference content.
- Use it when you want to avoid ambiguity about whether the wrapper will resolve to the small or large index flavor.
- In routine cases, the generic `hisat2-inspect` wrapper is still the better default.

## Common Patterns

```bash
# Summarize a large HISAT2 index
hisat2-inspect-l -s genome_large

# List reference names only
hisat2-inspect-l -n genome_large

# Extract embedded SNPs or splice sites
hisat2-inspect-l --snp genome_large > snps.txt
hisat2-inspect-l --ss genome_large > splicesites.txt

# Reconstruct the reference from a large index
hisat2-inspect-l -e genome_large > genome_large.fa
```

## Recommended Workflow

1. Run with `-s/--summary` first to understand index contents and properties
2. Use `-n/--names` to list reference sequence names without full output
3. Extract specific features as needed (`--snp`, `--ss`, `--exon`)
4. Use `-e/--ht2-ref` only when you need to reconstruct the full reference (slow)

## Guardrails

- The `<ht2_base>` argument is the ht2 filename minus trailing `.1.ht2l/.2.ht2l`
- Reconstructing reference with `-e/--ht2-ref` is slow; prefer `-s` or `-n` for quick inspection
- Output defaults to FASTA format to stdout; redirect or pipe as needed
- The direct executable prints a wrapper-warning message; that warning is expected when calling `hisat2-inspect-l` directly

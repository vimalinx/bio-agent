---
name: hisat2-build-s
description: Use when building a HISAT2 graph-based index from reference sequences for splice-aware RNA-seq alignment, optionally incorporating SNPs, haplotypes, splice sites, or exon annotations.
disable-model-invocation: true
user-invocable: true
---

# hisat2-build-s

## Quick Start

- **Command**: `hisat2-build-s <reference_in> <ht2_index_base>`
- **Local executable**: `/home/vimalinx/miniforge3/envs/bio/bin/hisat2-build-s`
- **Full reference**: See [references/help.md](references/help.md) for complete options and usage details.

## When To Use This Tool

- Use `hisat2-build-s` when building a standard HISAT2 small index (`.ht2`) for typical genome sizes.
- It is suitable for graph-aware index generation that augments the reference with SNPs, haplotypes, splice sites, exons, or repeat annotations.
- Use it when you specifically want to force the small-index builder rather than rely on `hisat2-build` wrapper logic.
- This is the normal upstream step before `hisat2-align-s`.

## Common Patterns

```bash
# Build a standard HISAT2 index from one FASTA
hisat2-build-s genome.fa genome

# Add splice sites and exon annotations for RNA-seq alignment
hisat2-build-s genome.fa genome --ss splicesites.txt --exon exons.txt

# Include SNP and haplotype annotations
hisat2-build-s genome.fa genome --snp snps.txt --haplotype haplotypes.txt

# Parallelize index construction
hisat2-build-s -p 8 genome.fa genome
```

## Recommended Workflow

1. Prepare reference sequence file(s) and optional annotation files (SNPs, haplotypes, splice sites, exons).
2. Run `hisat2-build-s` with reference input and desired index base name, using `-p` for multithreading.
3. Verify generated `.ht2` index files are created at the specified base path.
4. Note the tool warning: consider using `hisat2-build` wrapper instead of `hisat2-build-s` directly.

## Guardrails

- The tool recommends using `hisat2-build` wrapper instead of `hisat2-build-s` directly.
- Both `<reference_in>` and `<ht2_index_base>` arguments are required.
- Use `-p <int>` to control thread count based on available system resources.
- Downstream aligners should receive the basename only, without `.ht2` suffixes

---
name: hisat2-build-l
description: Use when building large HISAT2 index files from reference sequences for RNA-seq alignment with splice-aware mapping support.
disable-model-invocation: true
user-invocable: true
---

# hisat2-build-l

## Quick Start
- Command: `hisat2-build-l <reference_in> <ht2_index_base>`
- Local executable: `/home/vimalinx/miniforge3/envs/bio/bin/hisat2-build-l`
- Full reference: [references/help.md](references/help.md)

## When To Use This Tool

- Use `hisat2-build-l` when the reference or graph augmentation is large enough that you need HISAT2 large-index output (`.ht2l`).
- It is appropriate when building splice-aware or graph-aware indexes that include SNPs, haplotypes, splice sites, exons, or repeat annotations.
- Use it when you deliberately want the large-index builder instead of letting `hisat2-build` auto-select the backend.
- This is the right preparatory step before `hisat2-align-l`.

## Common Patterns

```bash
# Build a large HISAT2 index from one FASTA
hisat2-build-l genome.fa genome_large

# Build with splice sites and exons for RNA-seq alignment
hisat2-build-l genome.fa genome_large --ss splicesites.txt --exon exons.txt

# Include SNP and haplotype annotations
hisat2-build-l genome.fa genome_large --snp snps.txt --haplotype haplotypes.txt

# Use 8 threads during index construction
hisat2-build-l -p 8 genome.fa genome_large
```

## Recommended Workflow
1. Prepare reference FASTA file(s) and optional annotation files (SNP, haplotype, splice sites, exons)
2. Run `hisat2-build-l` with reference input and desired index base name
3. Use `-p` flag to specify thread count for parallel processing
4. Verify generated `.ht2l` index files are present before running HISAT2 alignment

## Guardrails
- The tool warns that `hisat2-build` wrapper is recommended over direct `hisat2-build-l` usage
- Use `--bmax`, `--bmaxdivn`, and `--dcv` options to manage memory for large references
- Output index files use `.ht2l` extension (large index format), not standard `.ht2`
- Pass only the basename to downstream aligners; do not append `.ht2l` suffixes manually

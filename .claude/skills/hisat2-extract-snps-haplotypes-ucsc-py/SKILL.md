---
name: hisat2-extract-snps-haplotypes-ucsc-py
description: Use when extracting SNPs and haplotypes from UCSC SNP files for HISAT2 graph-based genome indexing.
disable-model-invocation: true
user-invocable: true
---

# hisat2-extract-snps-haplotypes-ucsc-py

## Quick Start

- **Command**: `hisat2_extract_snps_haplotypes_UCSC.py <genome_file> <snp_fname> <base_fname>`
- **Local executable**: `/home/vimalinx/miniforge3/envs/bio/bin/hisat2_extract_snps_haplotypes_UCSC.py`
- **Full reference**: See [references/help.md](references/help.md) for complete options and usage details

## When To Use This Tool

- Use `hisat2_extract_snps_haplotypes_UCSC.py` when your variant source is a UCSC SNP table and you need HISAT2-ready `.snp` and `.haplotype` files.
- It is specifically for UCSC-formatted SNP downloads, not generic VCF input.
- Use it when preparing a variant-aware HISAT2 index from public UCSC polymorphism resources matched to a reference FASTA.
- Reach for `--testset` when you want synthetic reference/alternate test FASTAs alongside the normal SNP/haplotype outputs.

## Common Patterns

```bash
# Convert a UCSC SNP table into HISAT2 SNP and haplotype files
hisat2_extract_snps_haplotypes_UCSC.py genome.fa snp144Common.txt.gz hg38_ucsc

# Tune haplotype grouping distances
hisat2_extract_snps_haplotypes_UCSC.py genome.fa snp144Common.txt.gz hg38_ucsc --inter-gap 30 --intra-gap 50

# Print extraction statistics to stderr
hisat2_extract_snps_haplotypes_UCSC.py genome.fa snp144Common.txt.gz hg38_ucsc -v

# Also emit testset FASTAs in addition to .snp and .haplotype
hisat2_extract_snps_haplotypes_UCSC.py genome.fa snp144Common.txt.gz hg38_ucsc --testset
```

## Recommended Workflow

1. Download a UCSC SNP file (e.g., from `hgdownload.soe.ucsc.edu/goldenPath/hg38/database/`)
2. Prepare your reference genome FASTA file (`genome.fa`)
3. Run `hisat2_extract_snps_haplotypes_UCSC.py genome.fa snp144Common.txt.gz output_base`
4. Use the generated SNP/haplotype files when building a HISAT2 graph index with `hisat2-build`

## Guardrails

- Input SNP file must be in UCSC format (plain text or gzipped); other formats are not supported
- Genome file must be a FASTA file matching the UCSC SNP file's reference build
- Use `--verbose` to monitor statistics; large SNP files may require significant memory
- Output is keyed by `base_fname` and writes at least `base_fname.snp` and `base_fname.haplotype`; `--testset` additionally emits `.ref.testset.fa` and `.alt.testset.fa`
- This helper does not implement `--version`; use `-h/--help` instead

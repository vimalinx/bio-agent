---
name: hisat2-extract-snps-haplotypes-vcf-py
description: Use when extracting SNPs and haplotypes from VCF files to build variant-aware HISAT2 graph genome indexes
disable-model-invocation: true
user-invocable: true
---

# hisat2-extract-snps-haplotypes-vcf-py

## Quick Start
- **Command**: `hisat2_extract_snps_haplotypes_VCF.py <genome_file> <VCF_fnames> <base_fname>`
- **Local executable**: `/home/vimalinx/miniforge3/envs/bio/bin/hisat2_extract_snps_haplotypes_VCF.py`
- **Full reference**: See [references/help.md](references/help.md)

## When To Use This Tool

- Use `hisat2_extract_snps_haplotypes_VCF.py` when your variants are already in VCF and you need HISAT2 graph-index inputs.
- It is appropriate for genome-, chromosome-, or gene-oriented reference builds where VCF-derived SNP/haplotype extraction is required.
- Use it instead of the UCSC extractor whenever the source data is generic VCF rather than UCSC SNP tables.
- Reach for `--extra-files` if you also want auxiliary `.ref` and `_backbone.fa` outputs for downstream inspection or genotyping workflows.

## Common Patterns

```bash
# Convert one VCF into HISAT2 SNP and haplotype files
hisat2_extract_snps_haplotypes_VCF.py genome.fa variants.vcf.gz hg38_vcf

# Combine multiple VCFs via a comma-separated argument
hisat2_extract_snps_haplotypes_VCF.py genome.fa cohort1.vcf.gz,cohort2.vcf.gz hg38_vcf

# Change reference scale and emit extra backbone/reference files
hisat2_extract_snps_haplotypes_VCF.py genome.fa variants.vcf.gz hg38_vcf --reference-type chromosome --extra-files

# Allow non-rs identifiers and print extraction statistics
hisat2_extract_snps_haplotypes_VCF.py genome.fa variants.vcf.gz hg38_vcf --non-rs -v
```

## Recommended Workflow
1. Prepare a genome FASTA file (e.g., `genome.fa`) and VCF file(s) containing variant data
2. Run extraction: `hisat2_extract_snps_haplotypes_VCF.py genome.fa variants.vcf output_base`
3. Tune `--inter-gap` (default: 30) and `--intra-gap` (default: 50) to control haplotype grouping
4. Use output files as input for HISAT2 graph index building

## Guardrails
- VCF files can be plain text or gzipped; multiple files are comma-separated
- SNP IDs must begin with "rs" unless `--non-rs` is specified
- Use `--verbose` to monitor extraction statistics during processing
- Output is keyed by `base_fname` and writes at least `.snp` and `.haplotype`; `--extra-files` additionally produces `.ref` and `_backbone.fa`
- This helper does not implement `--version`; use `-h/--help` instead

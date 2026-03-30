# hisat2-extract-snps-haplotypes-vcf-py Help Reference

- Command: `hisat2_extract_snps_haplotypes_VCF.py`
- Sources: conda_bioconda
- Local executable: `/home/vimalinx/miniforge3/envs/bio/bin/hisat2_extract_snps_haplotypes_VCF.py`
- Summary: CLI installed by bioconda package hisat2.
- Package names: hisat2

## Captured Version

```text
$ hisat2_extract_snps_haplotypes_VCF.py --version
usage: hisat2_extract_snps_haplotypes_VCF.py [-h]
                                             [--reference-type REFERENCE_TYPE]
                                             [--inter-gap INTER_GAP]
                                             [--intra-gap INTRA_GAP]
                                             [--non-rs]
                                             [--genotype-vcf GENOTYPE_VCF]
                                             [--genotype-gene-list GENOTYPE_GENE_LIST]
                                             [--extra-files] [-v]
                                             [genome_file] [VCF_fnames]
                                             [base_fname]
hisat2_extract_snps_haplotypes_VCF.py: error: unrecognized arguments: --version
```

## Captured Help

```text
$ hisat2_extract_snps_haplotypes_VCF.py --help
usage: hisat2_extract_snps_haplotypes_VCF.py [-h]
                                             [--reference-type REFERENCE_TYPE]
                                             [--inter-gap INTER_GAP]
                                             [--intra-gap INTRA_GAP]
                                             [--non-rs]
                                             [--genotype-vcf GENOTYPE_VCF]
                                             [--genotype-gene-list GENOTYPE_GENE_LIST]
                                             [--extra-files] [-v]
                                             [genome_file] [VCF_fnames]
                                             [base_fname]

Extract SNPs and haplotypes from VCF files

positional arguments:
  genome_file           input genome file (e.g. genome.fa)
  VCF_fnames            A comma-seperated VCF files (plain text or gzipped
                        file is accepted: GRCh38_dbSNP_no_SVs.vcf or
                        GRCh38_dbSNP_no_SVs.vcf.gz
  base_fname            base filename for SNPs and haplotypes

options:
  -h, --help            show this help message and exit
  --reference-type REFERENCE_TYPE
                        Reference type: gene, chromosome, and genome (default:
                        genome)
  --inter-gap INTER_GAP
                        Maximum distance for variants to be in the same
                        haplotype (default: 30)
  --intra-gap INTRA_GAP
                        Break a haplotype into several haplotypes (default:
                        50)
  --non-rs              Allow SNP IDs not beginning with rs
  --genotype-vcf GENOTYPE_VCF
                        VCF file name for genotyping (default: empty)
  --genotype-gene-list GENOTYPE_GENE_LIST
                        A comma-separated list of genes to be genotyped
                        (default: empty)
  --extra-files         Output extra files such as _backbone.fa and .ref
  -v, --verbose         also print some statistics to stderr
```

## Captured Man Page

```text
No man page captured.
```

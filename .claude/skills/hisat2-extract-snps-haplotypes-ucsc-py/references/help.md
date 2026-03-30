# hisat2-extract-snps-haplotypes-ucsc-py Help Reference

- Command: `hisat2_extract_snps_haplotypes_UCSC.py`
- Sources: conda_bioconda
- Local executable: `/home/vimalinx/miniforge3/envs/bio/bin/hisat2_extract_snps_haplotypes_UCSC.py`
- Summary: CLI installed by bioconda package hisat2.
- Package names: hisat2

## Captured Version

```text
$ hisat2_extract_snps_haplotypes_UCSC.py --version
usage: hisat2_extract_snps_haplotypes_UCSC.py [-h] [--inter-gap INTER_GAP]
                                              [--intra-gap INTRA_GAP] [-v]
                                              [--testset]
                                              [genome_file] [snp_fname]
                                              [base_fname]
hisat2_extract_snps_haplotypes_UCSC.py: error: unrecognized arguments: --version
```

## Captured Help

```text
$ hisat2_extract_snps_haplotypes_UCSC.py --help
usage: hisat2_extract_snps_haplotypes_UCSC.py [-h] [--inter-gap INTER_GAP]
                                              [--intra-gap INTRA_GAP] [-v]
                                              [--testset]
                                              [genome_file] [snp_fname]
                                              [base_fname]

Extract SNPs and haplotypes from a SNP file downloaded from UCSC (e.g.
http://hgdownload.soe.ucsc.edu/goldenPath/hg38/database/snp144.txt.gz)

positional arguments:
  genome_file           input genome file (e.g. genome.fa)
  snp_fname             input snp file downloaded from UCSC (plain text or
                        gzipped file is accepted: snp144Common.txt or
                        snp144Common.txt.gz)
  base_fname            base filename for SNPs and haplotypes

options:
  -h, --help            show this help message and exit
  --inter-gap INTER_GAP
                        Maximum distance for variants to be in the same
                        haplotype
  --intra-gap INTRA_GAP
                        Break a haplotype into several haplotypes
  -v, --verbose         also print some statistics to stderr
  --testset             print test reads
```

## Captured Man Page

```text
No man page captured.
```

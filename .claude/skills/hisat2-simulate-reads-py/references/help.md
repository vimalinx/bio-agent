# hisat2-simulate-reads-py Help Reference

- Command: `hisat2_simulate_reads.py`
- Sources: conda_bioconda
- Local executable: `/home/vimalinx/miniforge3/envs/bio/bin/hisat2_simulate_reads.py`
- Summary: CLI installed by bioconda package hisat2.
- Package names: hisat2

## Captured Version

```text
$ hisat2_simulate_reads.py --version
hisat2_simulate_reads.py 2.0.0-alpha
```

## Captured Help

```text
$ hisat2_simulate_reads.py --help
usage: hisat2_simulate_reads.py [-h] [-d] [--single-end] [-r READ_LEN]
                                [-f FRAG_LEN] [-n NUM_FRAG] [-e EXPR_PROFILE]
                                [--repeat-info REPEAT_FNAME]
                                [--error-rate ERROR_RATE]
                                [--max-mismatch MAX_MISMATCH]
                                [--random-seed RANDOM_SEED]
                                [--snp-prob SNP_PROB] [--sanity-check] [-v]
                                [--version]
                                [genome_file] [gtf_file] [snp_file]
                                [base_fname]

Simulate reads from GENOME (fasta) and GTF files

positional arguments:
  genome_file           input GENOME file
  gtf_file              input GTF file
  snp_file              input SNP file
  base_fname            output base filename

options:
  -h, --help            show this help message and exit
  -d, --dna             DNA-seq reads (default: RNA-seq reads)
  --single-end          single-end reads (default: paired-end reads)
  -r READ_LEN, --read-length READ_LEN
                        read length (default: 100)
  -f FRAG_LEN, --fragment-length FRAG_LEN
                        fragment length (default: 250)
  -n NUM_FRAG, --num-fragment NUM_FRAG
                        number of fragments (default: 1000000)
  -e EXPR_PROFILE, --expr-profile EXPR_PROFILE
                        expression profile: flux or constant (default: flux)
  --repeat-info REPEAT_FNAME
                        repeat information filename
  --error-rate ERROR_RATE
                        per-base sequencing error rate (%) (default: 0.0)
  --max-mismatch MAX_MISMATCH
                        max mismatches due to sequencing errors (default: 3)
  --random-seed RANDOM_SEED
                        random seeding value (default: 0)
  --snp-prob SNP_PROB   probability of a read including a snp when the read
                        spans the snp ranging from 0.0 to 1.0 (default: 1.0)
  --sanity-check        sanity check
  -v, --verbose         also print some statistics to stderr
  --version             show program's version number and exit
```

## Captured Man Page

```text
No man page captured.
```

---
name: hisat2-simulate-reads-py
description: Use when simulating RNA-seq or DNA-seq reads from a reference genome and GTF annotation file, optionally incorporating SNP variants and controlling expression profiles.
disable-model-invocation: true
user-invocable: true
---

# hisat2-simulate-reads-py

## Quick Start

- **Command:** `hisat2_simulate_reads.py [genome_file] [gtf_file] [snp_file] [base_fname]`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/hisat2_simulate_reads.py`
- **Full reference:** See `references/help.md` for complete options and usage details

## When To Use This Tool

- Use `hisat2_simulate_reads.py` when you need synthetic HISAT2-style benchmark reads from a genome, annotation, and SNP set.
- It is appropriate for RNA-seq by default, but can also simulate DNA-seq with `-d`.
- Use it when benchmarking alignment settings, validating graph-aware variant handling, or generating controlled test data with fixed read and fragment lengths.
- Reach for it when you need reproducible simulations with explicit random seeds and optional sanity checks.

## Common Patterns

```bash
# Default paired-end RNA-seq simulation
hisat2_simulate_reads.py genome.fa annotation.gtf variants.snp sim

# Single-end RNA-seq with shorter reads
hisat2_simulate_reads.py genome.fa annotation.gtf variants.snp sim --single-end -r 75 -n 100000

# DNA-seq simulation with explicit random seed
hisat2_simulate_reads.py genome.fa annotation.gtf variants.snp sim -d --random-seed 42

# Run internal sanity checks and print extra statistics
hisat2_simulate_reads.py genome.fa annotation.gtf variants.snp sim --sanity-check -v
```

## Recommended Workflow

1. Prepare a reference genome FASTA file and corresponding GTF annotation file
2. Optionally prepare a SNP file if variant incorporation is needed
3. Run `hisat2_simulate_reads.py` with required positional arguments and desired options (e.g., `-n` for fragment count, `-e` for expression profile)
4. Validate output using `--sanity-check` and review statistics with `-v` if needed

## Guardrails

- Requires both genome FASTA and GTF files as positional inputs
- Defaults to paired-end RNA-seq reads; use `--single-end` and/or `-d` for alternative modes
- Set `--random-seed` for reproducible simulations
- The script writes output files based on `base_fname`, including `base_fname.sam` and at least `base_fname_1.fa` (plus `base_fname_2.fa` for paired-end mode)
- In the current environment, `-h` prints a non-fatal Python `SyntaxWarning` before the usage text; treat that as a script warning, not a failed invocation

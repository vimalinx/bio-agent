---
name: hisat2-read-statistics-py
description: Use when you need to compute basic read statistics (count, min/max/average length) from FASTQ/FASTA files before or after HISAT2 alignment workflows.
disable-model-invocation: true
user-invocable: true
---

# hisat2-read-statistics-py

## Quick Start

- **Command**: `hisat2_read_statistics.py [read_file] [-n READ_COUNT]`
- **Local executable**: `/home/vimalinx/miniforge3/envs/bio/bin/hisat2_read_statistics.py`
- **Full reference**: See `references/help.md`

## When To Use This Tool

- Use `hisat2_read_statistics.py` when you want a quick length/profile sanity check on input reads before alignment or simulation.
- It is appropriate for FASTA/FASTQ read files when you need rough counts and min/max/average read lengths without launching a full QC suite.
- Use it to verify read-length assumptions before choosing HISAT2 scoring or simulation parameters.
- It is also useful after synthetic-read generation to confirm outputs roughly match expected read lengths.

## Common Patterns

```bash
# Sample the default first 10,000 reads
hisat2_read_statistics.py reads.fq.gz

# Increase the sample size
hisat2_read_statistics.py reads.fq.gz -n 100000

# Scan the entire file
hisat2_read_statistics.py reads.fq.gz -n 0

# Check simulated reads before alignment
hisat2_read_statistics.py sim_1.fa
```

## Recommended Workflow

1. Verify the read file format (FASTQ or FASTA) is compatible with HISAT2 tools.
2. Run `hisat2_read_statistics.py <read_file>` to compute statistics on the first 10,000 reads (default).
3. Use `-n` flag to adjust sample size (e.g., `-n 100000` for larger samples or `-n 0` for entire file if supported).
4. Review output to confirm read lengths and counts are within expected ranges before proceeding to alignment.

## Guardrails

- The tool samples a subset of reads by default (10,000); statistics may not reflect entire file if `-n` is not adjusted.
- No `--version` flag is available; verify installation via `--help` or the executable path.
- Ensure the input file exists and is readable; the tool expects a valid reads file as the positional argument.
- `-n 0` means no sampling cutoff, so the script scans the entire file rather than zero reads

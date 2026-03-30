---
name: hisat2-align-s
description: Use when aligning RNA-seq reads to a HISAT2 index using the alignment binary directly. Supports spliced alignment with optional splice site annotation.
disable-model-invocation: true
user-invocable: true
---

# hisat2-align-s

## Quick Start

- **Command**: `hisat2-align-s -x <ht2-idx> {-1 <m1> -2 <m2> | -U <r>} [-S <sam>]`
- **Local executable**: `/home/vimalinx/miniforge3/envs/bio/bin/hisat2-align-s`
- **Full options**: see [references/help.md](references/help.md)

## When To Use This Tool

- Use `hisat2-align-s` when aligning reads against a standard HISAT2 small index (`.ht2`).
- It is a good fit for splice-aware RNA-seq alignment, especially when you want to inject known splice sites or produce `--dta` output for transcript assemblers.
- Use it when you explicitly want the small-index binary rather than the generic `hisat2` wrapper.
- For non-RNA or strictly contiguous alignments, disable splice handling with `--no-spliced-alignment`.

## Common Patterns

```bash
# Single-end splice-aware alignment
hisat2-align-s -x genome -U reads.fq -S aln.sam

# Paired-end RNA-seq alignment with 8 threads
hisat2-align-s -x genome -1 reads_R1.fq -2 reads_R2.fq -p 8 -S aln.sam

# Guide alignment with known splice sites and transcript-assembler output
hisat2-align-s -x genome -U reads.fq --known-splicesite-infile splicesites.txt --dta -S aln.sam

# DNA-style alignment without spliced alignment
hisat2-align-s -x genome -U reads.fq --no-spliced-alignment -S aln.sam
```

## Recommended Workflow

1. Build or obtain a HISAT2 index (`.ht2` files) for your reference genome
2. Prepare input reads as FASTQ/FASTA; specify paired mates with `-1` and `-2`, or unpaired with `-U`
3. Run alignment with appropriate options (e.g., `--dta` for transcript assemblers, `-p` for threads, `--known-splicesite-infile` if available)
4. Redirect or specify SAM output with `-S`; process downstream with samtools or transcript assemblers

## Guardrails

- The tool warns that running `hisat2-align` directly is not recommended; prefer the `hisat2` wrapper script for typical use
- Large values for `-k` or `--max-seeds` can significantly slow alignment on repetitive genomes
- Spliced alignment is enabled by default; use `--no-spliced-alignment` only for DNA-read alignment scenarios
- `-I/-X` fragment-length options only apply when spliced alignment is disabled

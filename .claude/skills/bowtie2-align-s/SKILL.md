---
name: bowtie2-align-s
description: Use when aligning sequencing reads (FASTQ/FASTA) to a reference genome using Bowtie 2. Supports paired-end, unpaired, interleaved, and BAM inputs with SAM output.
disable-model-invocation: true
user-invocable: true
---

# bowtie2-align-s

## Quick Start

- **Command:** `bowtie2-align-s -x <bt2-idx> {-1 <m1> -2 <m2> | -U <r>} [-S <sam>]`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/bowtie2-align-s`
- **Full options:** See [references/help.md](references/help.md)

## When To Use This Tool

- Use `bowtie2-align-s` when aligning reads against a standard Bowtie 2 small index (`.bt2`).
- It is appropriate for FASTQ, FASTA, raw-read, interleaved, or name-sorted unaligned BAM inputs.
- Use it when you explicitly want the small-index aligner instead of the generic `bowtie2` wrapper.
- In most everyday pipelines, the wrapper `bowtie2` remains the safer default unless you need to pin the underlying binary.

## Common Patterns

```bash
# Align unpaired reads against a standard Bowtie 2 index
bowtie2-align-s -x ref -U reads.fq -S aln.sam

# Align paired-end reads and use 8 threads
bowtie2-align-s -x ref -1 reads_R1.fq -2 reads_R2.fq -p 8 -S aln.sam

# Use local alignment with a sensitive preset
bowtie2-align-s -x ref -U reads.fq --very-sensitive-local -S aln.sam

# Suppress unaligned reads in SAM output
bowtie2-align-s -x ref -U reads.fq --no-unal -S aln.sam
```

## Recommended Workflow

1. Ensure a Bowtie 2 index exists at `<bt2-idx>` (built with `bowtie2-build`; Bowtie 1 indexes are incompatible)
2. Prepare reads in FASTQ (default), FASTA (`-f`), or other supported formats
3. Run alignment: `bowtie2-align-s -x <bt2-idx> -U reads.fq -S output.sam` (add `-p N` for multithreading)
4. Optionally use presets (e.g., `--very-sensitive`) or reporting options (`-k`, `-a`, `--no-unal`)

## Guardrails

- The tool warns that running `bowtie2-align` directly is not recommended; prefer the `bowtie2` wrapper for typical use
- MAPQ values are not meaningful when using `-k` or `-a` reporting modes
- Use `-I`/`-X` to set min/max fragment length for paired-end; defaults are 0 and 500

---
name: subread-align
description: Use when aligning RNA-seq or genomic DNA-seq reads to a reference index. Supports paired-end and single-end reads in FASTQ, FASTA, SAM, or BAM formats.
disable-model-invocation: true
user-invocable: true
---

# subread-align

## Quick Start
- **Command:** `subread-align -i <index_name> -r <input> -t <type> -o <output>`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/subread-align`
- **Version:** 2.1.1
- **Full reference:** See [references/help.md](references/help.md) for complete options and flags

## When To Use This Tool

- Align genomic DNA-seq reads with a fast Subread-based aligner.
- Align RNA-seq reads when full splice-junction discovery is not the main requirement.
- Produce BAM output directly for downstream QC or counting.
- Prefer `subjunc` instead when exon-exon junction detection is central.

## Common Patterns

```bash
# 1) Genomic DNA-seq alignment
subread-align \
  -i ref_index \
  -r reads.fastq.gz \
  -t 1 \
  -o sample.bam \
  -T 8
```

```bash
# 2) Paired-end RNA-seq alignment
subread-align \
  -i ref_index \
  -r sample_R1.fastq.gz \
  -R sample_R2.fastq.gz \
  -t 0 \
  -o sample.bam \
  -T 8
```

```bash
# 3) Coordinate-sorted BAM ready for genome-browser loading
subread-align \
  -i ref_index \
  -r sample_R1.fastq.gz \
  -R sample_R2.fastq.gz \
  -t 1 \
  -o sample.bam \
  -T 8 \
  --sortReadsByCoordinates
```

## Recommended Workflow

1. Build the index first with `subread-buildindex` and keep the basename stable.
2. Choose `-t 0` for RNA-seq and `-t 1` for genomic DNA before tuning anything else.
3. Add paired-end orientation and fragment constraints only if the library design requires it.
4. Validate mapping quality and BAM size before counting or variant calling.

## Guardrails
- `-i`, `-r`, and `-t` are mandatory, and `-i` expects the index basename, not the FASTA file.
- Gzipped FASTQ/FASTA are auto-detected; use `--SAMinput` or `--BAMinput` only for alignment-file input.
- Default output is BAM; use `--SAMoutput` only if plain-text SAM is actually needed.
- `--multiMapping` changes reporting behavior substantially; pair it with `-B` intentionally.
- `-m`, `-p`, `-M`, and `-I` affect sensitivity and specificity, so keep those settings cohort-consistent.

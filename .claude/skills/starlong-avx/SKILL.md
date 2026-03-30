---
name: starlong-avx
description: Use when aligning long RNA-seq reads to a reference genome with splice-aware mapping, or when generating STAR genome indices for long-read data.
disable-model-invocation: true
user-invocable: true
---

# starlong-avx

## Quick Start

- **Command:** `STARlong-avx`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/STARlong-avx`
- **Full reference:** See `references/help.md` for complete options and parameters

## When To Use This Tool

- Align long RNA-seq reads from PacBio or Nanopore with STARlong.
- Build or reuse STAR-compatible genome indices for long-read splice-aware mapping.
- Map full-length transcript reads while keeping STAR-style splice-junction outputs.
- Run a long-read-focused STAR wrapper using the AVX-optimized binary.

## Common Patterns

```bash
# 1) Build a genome index for STARlong
STARlong-avx \
  --runMode genomeGenerate \
  --genomeDir starlong_index \
  --genomeFastaFiles genome.fa \
  --sjdbGTFfile genes.gtf \
  --runThreadN 16
```

```bash
# 2) Align long reads from FASTQ
STARlong-avx \
  --genomeDir starlong_index \
  --readFilesIn longreads.fastq \
  --runThreadN 16
```

```bash
# 3) Align gzipped long reads and emit sorted BAM
STARlong-avx \
  --genomeDir starlong_index \
  --readFilesIn longreads.fastq.gz \
  --readFilesCommand zcat \
  --outSAMtype BAM SortedByCoordinate \
  --runThreadN 16
```

## Recommended Workflow

1. Prepare reference genome FASTA and optional GTF annotation file
2. Generate genome index: `STARlong-avx --runMode genomeGenerate --genomeDir <index_dir> --genomeFastaFiles <genome.fa> --sjdbGTFfile <annot.gtf> --runThreadN <threads>`
3. Align long reads: `STARlong-avx --genomeDir <index_dir> --readFilesIn <reads.fq> --runThreadN <threads>`
4. Review output alignments (SAM/BAM) and splice junction files (`SJ.out.tab`)

## Guardrails

- Always specify `--genomeDir` pointing to a valid STAR genome index directory
- Ensure `--runThreadN` matches available CPU cores to avoid resource contention
- Use `--readFilesCommand zcat` for gzipped input files; STAR expects uncompressed FASTA/FASTQ by default

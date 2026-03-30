---
name: starlong-ssse3
description: Use when aligning long RNA-seq reads to a reference genome with splice-aware mapping using the SSSE3-optimized STARlong binary.
disable-model-invocation: true
user-invocable: true
---

# starlong-ssse3

## Quick Start

- **Command:** `STARlong-ssse3 --genomeDir /path/to/index --readFilesIn reads.fq`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/STARlong-ssse3`
- **Full reference:** See [references/help.md](references/help.md) for complete options

## When To Use This Tool

- Align long RNA-seq reads from PacBio or Nanopore with STARlong.
- Build or reuse STAR-compatible genome indices for long-read splice-aware mapping.
- Map full-length transcript reads while keeping STAR-style splice-junction outputs.
- Run a long-read-focused STAR wrapper using the SSSE3-optimized binary.

## Common Patterns

```bash
# 1) Build a genome index for STARlong
STARlong-ssse3 \
  --runMode genomeGenerate \
  --genomeDir starlong_index \
  --genomeFastaFiles genome.fa \
  --sjdbGTFfile genes.gtf \
  --runThreadN 16
```

```bash
# 2) Align long reads from FASTQ
STARlong-ssse3 \
  --genomeDir starlong_index \
  --readFilesIn longreads.fastq \
  --runThreadN 16
```

```bash
# 3) Align gzipped long reads and emit sorted BAM
STARlong-ssse3 \
  --genomeDir starlong_index \
  --readFilesIn longreads.fastq.gz \
  --readFilesCommand zcat \
  --outSAMtype BAM SortedByCoordinate \
  --runThreadN 16
```

## Recommended Workflow

1. Generate or obtain a genome index using `--runMode genomeGenerate` with FASTA and optional GTF files
2. Run alignment with `STARlong-ssse3 --genomeDir /path/to/index --readFilesIn reads.fq`
3. Specify thread count with `--runThreadN` to parallelize alignment
4. Collect output alignments (SAM/BAM) and splice junction files (`SJ.out.tab`)

## Guardrails

- Ensure genome index compatibility; this version requires genome index version 2.7.4a or later
- Specify `--readFilesCommand zcat` (or similar) when input files are compressed
- Do not mix STARlong with standard STAR genome indexes; regenerate indexes appropriate for long-read mode

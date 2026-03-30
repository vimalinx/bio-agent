---
name: starlong-plain
description: Use when aligning long RNA-seq reads (PacBio, Nanopore) to a reference genome using splice-aware mapping with STARlong.
disable-model-invocation: true
user-invocable: true
---

# starlong-plain

## Quick Start
- **Command:** `STARlong-plain --genomeDir /path/to/index --readFilesIn reads.fastq`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/STARlong-plain`
- **Full reference:** See `references/help.md` for complete options and parameters

## When To Use This Tool

- Align long RNA-seq reads from PacBio or Nanopore with STARlong.
- Build or reuse STAR-compatible genome indices for long-read splice-aware mapping.
- Map full-length transcript reads while keeping STAR-style splice-junction outputs.
- Run a long-read-focused STAR wrapper instead of the short-read defaults.

## Common Patterns

```bash
# 1) Build a genome index for STARlong
STARlong-plain \
  --runMode genomeGenerate \
  --genomeDir starlong_index \
  --genomeFastaFiles genome.fa \
  --sjdbGTFfile genes.gtf \
  --runThreadN 16
```

```bash
# 2) Align long reads from FASTQ
STARlong-plain \
  --genomeDir starlong_index \
  --readFilesIn longreads.fastq \
  --runThreadN 16
```

```bash
# 3) Align gzipped long reads and emit sorted BAM
STARlong-plain \
  --genomeDir starlong_index \
  --readFilesIn longreads.fastq.gz \
  --readFilesCommand zcat \
  --outSAMtype BAM SortedByCoordinate \
  --runThreadN 16
```

## Recommended Workflow

1. Prepare genome FASTA and optionally GTF annotation for splice junctions
2. Generate genome index: `STARlong-plain --runMode genomeGenerate --genomeDir ./index --genomeFastaFiles genome.fa --sjdbGTFfile annotations.gtf`
3. Align long reads: `STARlong-plain --genomeDir ./index --readFilesIn reads.fastq`
4. Collect output alignments (SAM/BAM) and splice junction files from the output directory

## Guardrails

- Genome FASTA files must be plain text, not compressed
- `--genomeSAindexNbases` may need scaling for small genomes: `min(14, log2(GenomeLength)/2 - 1)`
- Specify shell explicitly with `--sysShell /bin/bash` if default shell fails
- Compressed read input still requires `--readFilesCommand zcat` or an equivalent decompressor

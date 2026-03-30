---
name: star-sse3
description: Use when aligning RNA-seq reads to a reference genome with splice-aware mapping, generating genome indexes, or performing splice junction detection.
disable-model-invocation: true
user-invocable: true
---

# star-sse3

## Quick Start

- **Command:** `STAR-sse3 --genomeDir /path/to/index --readFilesIn reads.fq`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/STAR-sse3`
- **Full reference:** See `references/help.md` for complete options and parameter details

## When To Use This Tool

- Build STAR genome indices for RNA-seq alignment.
- Perform splice-aware alignment of short RNA-seq reads against a genome.
- Run STAR modes with the SSE3-optimized STAR binary.
- Generate splice-junction-aware mappings for downstream counting, transcript assembly, or QC.

## Common Patterns

```bash
# 1) Build a STAR genome index
STAR-sse3 \
  --runMode genomeGenerate \
  --genomeDir star_index \
  --genomeFastaFiles genome.fa \
  --sjdbGTFfile genes.gtf \
  --runThreadN 16
```

```bash
# 2) Align paired-end gzipped RNA-seq reads
STAR-sse3 \
  --genomeDir star_index \
  --readFilesIn sample_R1.fastq.gz sample_R2.fastq.gz \
  --readFilesCommand zcat \
  --runThreadN 16
```

```bash
# 3) Align and emit coordinate-sorted BAM
STAR-sse3 \
  --genomeDir star_index \
  --readFilesIn sample_R1.fastq.gz sample_R2.fastq.gz \
  --readFilesCommand zcat \
  --outSAMtype BAM SortedByCoordinate \
  --runThreadN 16
```

## Recommended Workflow

1. Generate genome index with `--runMode genomeGenerate` using FASTA files and optional GTF annotations
2. Align reads with `--runMode alignReads` specifying `--genomeDir` and `--readFilesIn`
3. Set `--runThreadN` to match available CPU cores for parallel processing
4. Collect aligned BAM output and splice junction files from the output directory

## Guardrails

- Genome index must exist before alignment; generate it first with `--runMode genomeGenerate`
- Compressed input files require `--readFilesCommand` (e.g., `zcat` for `.gz` files)
- Ensure `--genomeSAindexNbases` is scaled appropriately for small genomes

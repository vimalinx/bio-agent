---
name: star-avx
description: Use when aligning RNA-seq reads to a reference genome with splice-aware mapping, generating genome indices, or processing single-cell RNA-seq data with STARsolo.
disable-model-invocation: true
user-invocable: true
---

# star-avx

## Quick Start

- **Command**: `STAR-avx [options] --genomeDir /path/to/genome/index/ --readFilesIn R1.fq R2.fq`
- **Local executable**: `/home/vimalinx/miniforge3/envs/bio/bin/STAR-avx`
- **Full reference**: `references/help.md`

## When To Use This Tool

- Build STAR genome indices for RNA-seq alignment.
- Perform splice-aware alignment of short RNA-seq reads against a genome.
- Run STARsolo, BAM-input, or lift-over modes with the AVX-optimized STAR binary.
- Generate splice-junction-aware mappings for downstream counting, transcript assembly, or QC.

## Common Patterns

```bash
# 1) Build a STAR genome index
STAR-avx \
  --runMode genomeGenerate \
  --genomeDir star_index \
  --genomeFastaFiles genome.fa \
  --sjdbGTFfile genes.gtf \
  --runThreadN 16
```

```bash
# 2) Align paired-end gzipped RNA-seq reads
STAR-avx \
  --genomeDir star_index \
  --readFilesIn sample_R1.fastq.gz sample_R2.fastq.gz \
  --readFilesCommand zcat \
  --runThreadN 16
```

```bash
# 3) Align and emit coordinate-sorted BAM
STAR-avx \
  --genomeDir star_index \
  --readFilesIn sample_R1.fastq.gz sample_R2.fastq.gz \
  --readFilesCommand zcat \
  --outSAMtype BAM SortedByCoordinate \
  --runThreadN 16
```

## Recommended Workflow

1. Generate a genome index using `--runMode genomeGenerate` with `--genomeFastaFiles` and `--sjdbGTFfile`
2. Align reads with `--runMode alignReads` specifying `--genomeDir` and `--readFilesIn`
3. Set appropriate thread count with `--runThreadN` based on available cores
4. Review output alignments (SAM/BAM) and splice junction files (`SJ.out.tab`)

## Guardrails

- Genome index must be compatible with STAR version 2.7.4a or later (`versionGenome` parameter)
- Ensure `--genomeSAindexNbases` is scaled appropriately for small genomes: `min(14, log2(GenomeLength)/2 - 1)`
- Use `--readFilesCommand zcat` for compressed `.gz` input files; FASTA/FASTQ inputs cannot be zipped directly

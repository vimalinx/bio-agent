---
name: star-sse4-1
description: Use when aligning RNA-seq reads to a reference genome, generating STAR genome indices, or performing splice-aware transcript alignment.
disable-model-invocation: true
user-invocable: true
---

# star-sse4-1

## Quick Start
- **Command**: `STAR-sse4.1`
- **Local executable**: `/home/vimalinx/miniforge3/envs/bio/bin/STAR-sse4.1`
- **Full reference**: See `references/help.md` for complete options and parameters

## When To Use This Tool
- Build STAR genome indices for RNA-seq alignment.
- Perform splice-aware alignment of short RNA-seq reads against a genome.
- Run STAR, lift-over, or BAM-input modes with the SSE4.1-optimized STAR binary.
- Generate splice-junction-aware mappings for downstream counting, transcript assembly, or QC.

## Common Patterns
```bash
# 1) Build a STAR genome index
STAR-sse4.1 \
  --runMode genomeGenerate \
  --genomeDir star_index \
  --genomeFastaFiles genome.fa \
  --sjdbGTFfile genes.gtf \
  --runThreadN 16
```

```bash
# 2) Align paired-end gzipped RNA-seq reads
STAR-sse4.1 \
  --genomeDir star_index \
  --readFilesIn sample_R1.fastq.gz sample_R2.fastq.gz \
  --readFilesCommand zcat \
  --runThreadN 16
```

```bash
# 3) Align and emit coordinate-sorted BAM
STAR-sse4.1 \
  --genomeDir star_index \
  --readFilesIn sample_R1.fastq.gz sample_R2.fastq.gz \
  --readFilesCommand zcat \
  --outSAMtype BAM SortedByCoordinate \
  --runThreadN 16
```

## Recommended Workflow
1. Generate genome index with `--runMode genomeGenerate`, providing FASTA via `--genomeFastaFiles` and optional GTF via `--sjdbGTFfile`
2. Set `--genomeDir` to the index directory and configure threads with `--runThreadN`
3. Align reads using `--runMode alignReads` with input files specified via `--readFilesIn`
4. Collect output alignments (SAM/BAM) and splice junction files from the output directory

## Guardrails
- Always provide `--genomeDir` pointing to a valid genome index before running alignment
- Set `--runThreadN` appropriately for available CPU cores to avoid resource contention
- Use `--sjdbOverhang` set to read length minus 1 for optimal splice junction detection

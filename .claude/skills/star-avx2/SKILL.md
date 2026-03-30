---
name: star-avx2
description: Use when aligning RNA-seq reads to a reference genome or generating genome indices for spliced transcript alignment
disable-model-invocation: true
user-invocable: true
---

# star-avx2

## Quick Start

- **Command**: `STAR-avx2`
- **Local executable**: `/home/vimalinx/miniforge3/envs/bio/bin/STAR-avx2`
- **Reference**: See [references/help.md](references/help.md) for full options and parameters

## When To Use This Tool

- Build STAR genome indices for RNA-seq alignment.
- Perform splice-aware alignment of short RNA-seq reads against a genome.
- Run STAR modes with the AVX2-optimized STAR binary.
- Generate splice-junction-aware mappings for downstream counting, transcript assembly, or QC.

## Common Patterns

```bash
# 1) Build a STAR genome index
STAR-avx2 \
  --runMode genomeGenerate \
  --genomeDir star_index \
  --genomeFastaFiles genome.fa \
  --sjdbGTFfile genes.gtf \
  --runThreadN 16
```

```bash
# 2) Align paired-end gzipped RNA-seq reads
STAR-avx2 \
  --genomeDir star_index \
  --readFilesIn sample_R1.fastq.gz sample_R2.fastq.gz \
  --readFilesCommand zcat \
  --runThreadN 16
```

```bash
# 3) Align and emit coordinate-sorted BAM
STAR-avx2 \
  --genomeDir star_index \
  --readFilesIn sample_R1.fastq.gz sample_R2.fastq.gz \
  --readFilesCommand zcat \
  --outSAMtype BAM SortedByCoordinate \
  --runThreadN 16
```

## Recommended Workflow

1. **Generate genome index**: `STAR-avx2 --runMode genomeGenerate --genomeDir /path/to/index --genomeFastaFiles genome.fa --sjdbGTFfile annotations.gtf`
2. **Align reads**: `STAR-avx2 --genomeDir /path/to/index --readFilesIn R1.fq R2.fq --runThreadN N`
3. **Handle compressed input**: Add `--readFilesCommand zcat` for `.gz` files or `bzcat` for `.bz2` files
4. **Check outputs**: Review `Aligned.out.sam` for alignments and `SJ.out.tab` for splice junctions

## Guardrails

- Set `--runThreadN` to match available CPU cores; default is 1 thread
- Ensure `--sjdbOverhang` equals read length minus 1 for optimal junction detection
- Use `--genomeLoad NoSharedMemory` on shared systems to avoid memory conflicts

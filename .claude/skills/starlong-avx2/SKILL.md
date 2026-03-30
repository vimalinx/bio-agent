---
name: starlong-avx2
description: Use when aligning long RNA-seq reads to a reference genome using the AVX2-optimized STARlong aligner for splice-aware mapping.
disable-model-invocation: true
user-invocable: true
---

# starlong-avx2

## Quick Start
- Command: `STARlong-avx2 --genomeDir /path/to/index --readFilesIn reads.fq`
- Local executable: `/home/vimalinx/miniforge3/envs/bio/bin/STARlong-avx2`
- Full reference: [references/help.md](references/help.md)

## When To Use This Tool
- Align long RNA-seq reads from PacBio or Nanopore with STARlong.
- Build or reuse STAR-compatible genome indices for long-read splice-aware mapping.
- Map full-length transcript reads while keeping STAR-style splice-junction outputs.
- Run a long-read-focused STAR wrapper using the AVX2-optimized binary.

## Common Patterns
```bash
# 1) Build a genome index for STARlong
STARlong-avx2 \
  --runMode genomeGenerate \
  --genomeDir starlong_index \
  --genomeFastaFiles genome.fa \
  --sjdbGTFfile genes.gtf \
  --runThreadN 16
```

```bash
# 2) Align long reads from FASTQ
STARlong-avx2 \
  --genomeDir starlong_index \
  --readFilesIn longreads.fastq \
  --runThreadN 16
```

```bash
# 3) Align gzipped long reads and emit sorted BAM
STARlong-avx2 \
  --genomeDir starlong_index \
  --readFilesIn longreads.fastq.gz \
  --readFilesCommand zcat \
  --outSAMtype BAM SortedByCoordinate \
  --runThreadN 16
```

## Recommended Workflow
1. Prepare or obtain a genome index directory using `--runMode genomeGenerate` with FASTA and optional GTF files
2. Run alignment with `STARlong-avx2 --genomeDir <index> --readFilesIn <reads>` adjusting `--runThreadN` for parallelism
3. Use `--readFilesCommand zcat` for gzipped input files as needed
4. Review output files (Aligned.out.sam, SJ.out.tab) and check Log.final.out for mapping statistics

## Guardrails
- Always specify `--genomeDir` pointing to a valid STAR genome index directory
- Set `--runThreadN` appropriately for available CPU cores to avoid resource contention
- Ensure input read files match the expected format (FASTA/FASTQ); use `--readFilesCommand` for compressed files

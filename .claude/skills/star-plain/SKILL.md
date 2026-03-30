---
name: star-plain
description: Use when aligning RNA-seq reads to a reference genome with splice-aware mapping, generating genome indices, or performing related operations like lift-over and BAM input processing.
disable-model-invocation: true
user-invocable: true
---

# star-plain

## Quick Start
- **Command**: `STAR-plain`
- **Local executable**: `/home/vimalinx/miniforge3/envs/bio/bin/STAR-plain`
- **Full reference**: `references/help.md`

## When To Use This Tool

- Build STAR genome indices for RNA-seq alignment.
- Perform splice-aware alignment of short RNA-seq reads against a genome.
- Lift over annotations between assemblies or process BAM input with STAR run modes.
- Generate splice-junction-aware mappings for downstream counting, transcript assembly, or QC.

## Common Patterns

```bash
# 1) Build a STAR genome index
STAR-plain \
  --runMode genomeGenerate \
  --genomeDir star_index \
  --genomeFastaFiles genome.fa \
  --sjdbGTFfile genes.gtf \
  --runThreadN 16
```

```bash
# 2) Align paired-end gzipped RNA-seq reads
STAR-plain \
  --genomeDir star_index \
  --readFilesIn sample_R1.fastq.gz sample_R2.fastq.gz \
  --readFilesCommand zcat \
  --runThreadN 16
```

```bash
# 3) Align and emit coordinate-sorted BAM
STAR-plain \
  --genomeDir star_index \
  --readFilesIn sample_R1.fastq.gz sample_R2.fastq.gz \
  --readFilesCommand zcat \
  --outSAMtype BAM SortedByCoordinate \
  --runThreadN 16
```

## Recommended Workflow

1. **Generate genome index**: `STAR-plain --runMode genomeGenerate --genomeDir /path/to/index --genomeFastaFiles genome.fa --sjdbGTFfile annotations.gtf --runThreadN N`
2. **Align reads**: `STAR-plain --genomeDir /path/to/index --readFilesIn R1.fq R2.fq --runThreadN N`
3. **Handle compressed input**: add `--readFilesCommand zcat` for `.gz` files or `bzcat` for `.bz2` files
4. **Review output**: check alignment results and splice junction file `SJ.out.tab`

## Guardrails

- Genome FASTA files must be plain text and cannot be zipped
- Scale `--genomeSAindexNbases` down for small genomes: use `min(14, log2(GenomeLength)/2 - 1)`
- Use `--genomeLoad NoSharedMemory` for isolated runs to avoid shared memory issues on some systems
- Compressed read files need an explicit decompression command such as `--readFilesCommand zcat`

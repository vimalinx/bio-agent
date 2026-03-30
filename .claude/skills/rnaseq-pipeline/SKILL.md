---
name: rnaseq-pipeline
description: Use when building or reviewing an end-to-end RNA-seq workflow from raw reads through quantification, differential expression, and basic interpretation.
allowed-tools:
  - Read
  - Write
  - Bash(fastqc:*)
  - Bash(star:*)
  - Bash(hisat2:*)
  - Bash(salmon:*)
  - Bash(featurecounts:*)
  - Bash(r:*)
  - Bash(python:*)
context: fork
agent: bio-expert
---

# RNA-seq Analysis Pipeline Skill

## Quick Start

- **Scope:** project-level RNA-seq workflow, not a single CLI executable
- **Core stages:** QC -> trimming -> alignment or pseudoalignment -> quantification -> DE -> plots
- **Primary tools in this workspace:** `FastQC`, `MultiQC`, `STAR`, `hisat2`, `featureCounts`, `Salmon`, `R/DESeq2`

## When To Use This Tool

- Build a complete bulk RNA-seq analysis workflow from FASTQ files to biological interpretation.
- Choose between alignment-based and alignment-free quantification paths.
- Standardize project structure, checkpoints, and expected deliverables for an RNA-seq study.
- Review an existing RNA-seq pipeline for missing QC, counting, or DE steps.

## Common Patterns

```bash
# 1) Alignment-based workflow
fastqc raw/*.fastq.gz -o qc/raw/
STAR --runMode genomeGenerate --genomeDir genome_index --genomeFastaFiles genome.fa --sjdbGTFfile genes.gtf
STAR --genomeDir genome_index --readFilesIn sample_R1.fastq.gz sample_R2.fastq.gz --readFilesCommand zcat --outSAMtype BAM SortedByCoordinate
featureCounts -a genes.gtf -o counts.txt sample.bam
```

```bash
# 2) Lightweight quantification workflow
fastqc raw/*.fastq.gz -o qc/raw/
salmon index -t transcripts.fa -i transcriptome_index
salmon quant -i transcriptome_index -l A -1 sample_R1.fastq.gz -2 sample_R2.fastq.gz -o sample_quant
```

```r
# 3) Differential expression handoff
library(DESeq2)
dds <- DESeqDataSetFromMatrix(countData = counts, colData = coldata, design = ~ condition)
dds <- DESeq(dds)
res <- results(dds)
```

## Recommended Workflow

1. Start with sample metadata, contrasts, reference assembly, and annotation versions fixed in writing.
2. Run raw-read QC first and decide whether trimming is actually necessary.
3. Choose one quantification branch deliberately: splice-aware alignment plus counting, or transcript-level pseudoalignment.
4. Build a count matrix or abundance table only after confirming library strandedness and annotation compatibility.
5. Run DE with proper biological replicates, then produce PCA, heatmap, MA, and volcano summaries.
6. Finish with enrichment or pathway analysis only after validating the upstream statistical model.

## Guardrails

- Never mix genome assembly and annotation releases.
- Strandedness mistakes will corrupt counts; verify it before cohort-scale quantification.
- Differential expression without biological replication is not a real DE workflow.
- Batch effects, low-count filtering, and contrast specification should be decided before interpreting significant genes.
- This meta-skill should delegate command-level details to the individual tool skills instead of duplicating every CLI option inline.

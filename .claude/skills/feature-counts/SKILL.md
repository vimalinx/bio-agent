---
name: feature-counts
description: Use when you need to assign aligned sequencing reads to genes or genomic features for expression quantification from SAM/BAM files
disable-model-invocation: true
user-invocable: true
---

# feature-counts

## Quick Start
- **Command:** `featureCounts`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/featureCounts`
- **Version:** 2.1.1
- **Full options:** see [references/help.md](references/help.md)

## When To Use This Tool

- Convert aligned RNA-seq BAM/SAM files into gene-level count matrices.
- Count reads at exon level with `-f`, or junction-supporting reads with `-J`.
- Handle stranded, paired-end, and multi-mapping policies explicitly.
- Prefer this after `STAR` or `subjunc` when you need a simple, transparent counting step.

## Common Patterns

```bash
# 1) Standard gene-level counting for paired-end, reversely stranded RNA-seq
featureCounts \
  -a genes.gtf \
  -o counts.txt \
  -T 8 \
  -p --countReadPairs \
  -s 2 \
  sample.bam
```

```bash
# 2) Exon-level counting instead of gene-level summarization
featureCounts \
  -a genes.gtf \
  -o exon_counts.txt \
  -T 8 \
  -f \
  -t exon \
  -g gene_id \
  sample.bam
```

```bash
# 3) Count exon-exon junction support
featureCounts \
  -a genes.gtf \
  -G genome.fa \
  -o counts.txt \
  -J \
  sample.bam
```

## Recommended Workflow

1. Start from coordinate-sorted BAM files aligned to the same assembly as the annotation.
2. Decide gene-level vs feature-level summarization and set `-f`, `-t`, and `-g` accordingly.
3. Set library-specific flags explicitly: `-p`, `--countReadPairs`, `-s`, `-M`, `--fraction`, `-Q`.
4. Review both `counts.txt` and `counts.txt.summary` before downstream DE analysis.

## Guardrails
- Chromosome names must match between BAM and annotation; use `-A` alias mapping if they do not.
- For paired-end libraries, `-p` alone assumes paired reads, but `--countReadPairs` is what switches counting from reads to fragments.
- Strandness is easy to invert; verify whether the library is `0`, `1`, or `2` before counting the whole cohort.
- `-M` uses the `NH` tag to detect multi-mappers; do not enable it blindly if aligner tags are inconsistent.
- Annotation format defaults to `GTF`; specify `-F SAF` when using SAF input.

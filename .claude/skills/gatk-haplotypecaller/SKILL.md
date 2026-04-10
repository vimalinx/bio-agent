---
name: gatk-haplotypecaller
description: Use when running GATK HaplotypeCaller to emit per-sample germline variant calls or gVCFs from analysis-ready BAM/CRAM inputs.
disable-model-invocation: true
user-invocable: true
---

# gatk-haplotypecaller

## Quick Start
- **Command:** `gatk HaplotypeCaller`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/gatk`
- **Install hint:** Install GATK into the active bioinformatics environment or put a working `gatk` executable on `PATH`.

## When To Use This Tool

- Per-sample germline SNP and indel calling from analysis-ready BAM or CRAM files.
- Emitting reference-confidence gVCFs for later joint genotyping.
- Standard Broad/GATK-style germline workflows after alignment, duplicate handling, and BQSR.

## Common Patterns

```bash
gatk HaplotypeCaller \
  -R reference.fa \
  -I sample.analysis_ready.bam \
  -O sample.g.vcf.gz \
  -ERC GVCF
```

## Guardrails

- Input BAM or CRAM should already be analysis-ready and matched to the exact reference build.
- Joint calling workflows usually want `-ERC GVCF`, not a raw single-sample VCF.
- This skill definition only proves the workflow step is known; the local `gatk` executable still has to exist for real execution.

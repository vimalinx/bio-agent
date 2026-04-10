---
name: gatk-genotypegvcfs
description: Use when joint-genotyping one or more germline gVCFs into a cohort VCF with GATK GenotypeGVCFs.
disable-model-invocation: true
user-invocable: true
---

# gatk-genotypegvcfs

## Quick Start
- **Command:** `gatk GenotypeGVCFs`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/gatk`
- **Install hint:** Install GATK into the active bioinformatics environment or put a working `gatk` executable on `PATH`.

## When To Use This Tool

- Joint-genotyping per-sample gVCFs into a cohort VCF.
- Standard downstream step after producing reference-confidence gVCFs with HaplotypeCaller.
- Germline SNP/indel discovery workflows for WES or WGS cohorts.

## Common Patterns

```bash
gatk GenotypeGVCFs \
  -R reference.fa \
  -V cohort.g.vcf.gz \
  -O cohort.joint.vcf.gz
```

## Guardrails

- Input gVCFs must have been generated against the same reference build and compatible interval scheme.
- This skill definition only proves the workflow step is known; the local `gatk` executable still has to exist for real execution.

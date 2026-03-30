---
name: vcf-subset
description: Use when subsetting VCF files by samples or filtering variant types from bgzipped VCF input.
disable-model-invocation: true
user-invocable: true
---

# vcf-subset

## Quick Start
- **Command**: `vcf-subset [OPTIONS] in.vcf.gz > out.vcf`
- **Local executable**: `/home/vimalinx/miniforge3/envs/bio/bin/vcf-subset`
- **Full reference**: See `references/help.md`

## When To Use This Tool

- Keep only a subset of samples from a compressed VCF.
- Restrict rows to certain variant classes such as SNPs or indels.
- Trim away unused alternate alleles after sample subsetting.
- Extract variants private to a subset of samples.

## Common Patterns

```bash
# 1) Keep a subset of samples
vcf-subset -c samples.txt in.vcf.gz > subset.vcf
```

```bash
# 2) Keep only indels for one sample and drop non-variant rows
vcf-subset -c SAMPLE1 -t indels -e in.vcf.gz > sample1.indels.vcf
```

```bash
# 3) Keep private variants and trim unused ALTs
vcf-subset -c cases.txt -p -a in.vcf.gz > cases.private.vcf
```

## Recommended Workflow

1. Start from a bgzipped VCF and decide whether the primary goal is sample restriction, type filtering, or privacy filtering.
2. Supply the target sample list with `-c`, either as a file or comma-separated list.
3. Add row-level modifiers like `-t`, `-e`, `-u`, `-p`, or `-a` only after thinking through their interaction.
4. Validate the resulting sample columns and variant counts before feeding the subset into association or QC workflows.

## Guardrails

- Input is expected to be a bgzipped VCF.
- `-f` forces past missing requested samples; use it only when you understand exactly which samples are absent.
- `-e` excludes rows without variants in the kept subset, while `-r` replaces excluded sample genotypes with reference; combining them changes both row and genotype semantics.
- `-a` trimming alternate alleles can change ALT ordering/content, so be careful if downstream annotations depend on the original allele representation.

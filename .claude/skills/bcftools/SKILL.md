---
name: bcftools
description: Use when working with VCF/BCF variant files for indexing, manipulation, analysis, or variant calling.
disable-model-invocation: true
user-invocable: true
---

# bcftools

## Quick Start
- **Command:** `bcftools`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/bcftools`
- **Version:** 1.22
- **Full reference:** See [references/help.md](references/help.md) for complete help text and subcommand details

## When To Use This Tool

- Inspect, filter, normalize, query, call, and summarize VCF/BCF files.
- Default companion tool for modern variant workflows.
- Use it after alignment/variant calling and before downstream annotation or cohort comparison.
- Prefer subcommand-oriented use such as `view`, `norm`, `query`, `stats`, `call`, or `mpileup`.

## Common Patterns

```bash
# 1) Subset and view a compressed VCF
bcftools view -r chr1:100000-110000 cohort.vcf.gz
```

```bash
# 2) Normalize variants against a reference
bcftools norm -f reference.fa -Oz -o cohort.norm.vcf.gz cohort.vcf.gz
bcftools index cohort.norm.vcf.gz
```

```bash
# 3) Extract tabular fields
bcftools query -f '%CHROM\t%POS\t%REF\t%ALT[\t%GT]\n' cohort.vcf.gz
```

```bash
# 4) Produce summary statistics
bcftools stats cohort.vcf.gz > cohort.stats.txt
```

## Recommended Workflow

1. Keep VCF/BCF indexed whenever possible.
2. Use `view` or `filter` to subset before heavier operations.
3. Normalize indels with `norm` before comparing or merging callsets.
4. Use `query` and `stats` for reporting instead of ad hoc parsing when possible.

## Guardrails

- Indexed VCF/BCF works in all situations; streams and unindexed files do not.
- `bcftools norm` needs the correct reference FASTA to do honest left-alignment and normalization.
- Use `plugin -lv` before reinventing functionality that already exists in a plugin.
- Be explicit about compressed output with `-Oz` or BCF output with `-Ob` when building pipelines.

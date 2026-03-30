---
name: vcf-query
description: Use when extracting and formatting specific fields from compressed VCF files, querying variants by region, or generating custom tabular output with genotype and INFO data.
disable-model-invocation: true
user-invocable: true
---

# vcf-query

## Quick Start
- **Command:** `vcf-query [OPTIONS] file.vcf.gz`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/vcf-query`
- **Full reference:** See `references/help.md`

## When To Use This Tool

- Extract selected VCF fields into a custom tabular report.
- Loop over per-sample genotype fields with bracket expressions.
- Run quick region-restricted queries on an indexed `.vcf.gz`.
- Keep using it only if you already depend on the vcftools Perl utility; for new workflows, prefer `bcftools query`.

## Common Patterns

```bash
# 1) Extract core variant fields plus depth
vcf-query \
  file.vcf.gz \
  -f '%CHROM\t%POS\t%REF\t%ALT\t%INFO/DP\n'
```

```bash
# 2) Emit per-sample genotype information
vcf-query \
  file.vcf.gz \
  -f '%CHROM:%POS[\t%SAMPLE=%GT]\n'
```

```bash
# 3) Restrict output to a region
vcf-query \
  file.vcf.gz \
  -r 1:1000-2000 \
  -f '%CHROM\t%POS\t%FILTER\n'
```

## Recommended Workflow

1. Start by listing available columns with `-l` if the file provenance is unclear.
2. Build the output format string deliberately with `%INFO/TAG`, `%GT`, `%SAMPLE`, and bracket loops when sample iteration is needed.
3. Restrict to a genomic interval with `-r` only when the file is properly indexed.
4. Redirect output to a file or pipe it into downstream table-processing tools.

## Guardrails

- Input files are expected to be compressed VCFs, and region queries require tabix indexing.
- This script is explicitly marked upstream as not being supported in the future; prefer `bcftools query` for durable pipelines.
- The default format string already loops over samples, so be explicit with `-f` if you want predictable output.
- `-c/--columns` can take either a comma-separated list or a file of one column name per line.

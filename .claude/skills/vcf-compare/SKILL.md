---
name: vcf-compare
description: Use when comparing two or more bgzipped and tabix-indexed VCF files to assess concordance of variant calls, positions, or genotypes.
disable-model-invocation: true
user-invocable: true
---

# vcf-compare

## Quick Start
- **Command:** `vcf-compare [OPTIONS] file1.vcf.gz file2.vcf.gz ...`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/vcf-compare`
- **Full reference:** See `references/help.md`

## When To Use This Tool

- Measure concordance between two or more indexed VCF callsets.
- Compare either positions only or full genotypes with `-g`.
- Generate per-chromosome comparison outputs and plotting summaries.
- Inspect indel comparison behavior with a tolerance window when callers left-align differently.

## Common Patterns

```bash
# 1) Compare positions only
vcf-compare truth.vcf.gz calls.vcf.gz
```

```bash
# 2) Compare genotypes for matched samples
vcf-compare -g truth.vcf.gz calls.vcf.gz
```

```bash
# 3) Restrict to PASS records and make plots
vcf-compare \
  -a \
  -g \
  -p cmp_plots \
  truth.vcf.gz calls.vcf.gz
```

## Recommended Workflow

1. Make sure all inputs are bgzipped and tabix-indexed before comparing.
2. Decide whether you care about positional concordance only or true genotype agreement with `-g`.
3. Use sample-name mapping if the files carry equivalent samples under different column names.
4. Review summary metrics and, for difficult cases, restrict to regions or apply a comparison window for indels.

## Guardrails

- Inputs must be bgzipped and tabix-indexed.
- Without `-g`, this is mostly a position-level comparison, not a sample-genotype concordance audit.
- `--ignore-indels` and `-w` can materially change the biological interpretation of agreement.
- `-c/--chromosomes` is retained only for backward compatibility; prefer `-r/--regions`.

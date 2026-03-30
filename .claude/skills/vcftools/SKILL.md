---
name: vcftools
description: Use when working with Variant Call Format (VCF) files and need to filter, summarize, or manipulate variant data.
disable-model-invocation: true
user-invocable: true
---

# vcftools

## Quick Start
- **Command:** `vcftools`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/vcftools`
- **Version:** 0.1.17
- **Full reference:** See [references/help.md](references/help.md) and the installed man page under `/home/vimalinx/miniforge3/envs/bio/share/man/man1/vcftools.1`

## When To Use This Tool

- Filter VCF or BCF files by site, variant type, allele frequency, or missingness.
- Export summary statistics such as allele frequency, Hardy-Weinberg tests, or site depth.
- Recode filtered VCFs for downstream tools.
- Prefer `vcftools` for classic population-genetics style filtering and quick summaries.

## Common Patterns

```bash
# 1) SNP-only filtered VCF
vcftools \
  --gzvcf cohort.vcf.gz \
  --remove-indels \
  --recode --recode-INFO-all \
  --out cohort.snps_only
```

```bash
# 2) Common-variant, low-missingness filter
vcftools \
  --gzvcf cohort.vcf.gz \
  --maf 0.05 \
  --max-missing 0.9 \
  --recode --recode-INFO-all \
  --out cohort.filtered
```

```bash
# 3) Allele-frequency report for one chromosome
vcftools \
  --gzvcf cohort.vcf.gz \
  --freq \
  --chr 1 \
  --out chr1.freq
```

```bash
# 4) Site mean depth summary
vcftools \
  --gzvcf cohort.vcf.gz \
  --site-mean-depth \
  --out cohort.depth
```

## Recommended Workflow

1. Pick the correct input mode first: `--vcf`, `--gzvcf`, or `--bcf`.
2. Separate filtering passes from statistics passes so outputs stay interpretable.
3. When writing a new VCF, use `--recode` and usually `--recode-INFO-all`.
4. Keep the filtering thresholds documented, because small MAF or missingness changes can materially alter results.

## Guardrails

- If `--out` is omitted, files default to the `out.*` prefix in the current directory.
- `--recode` writes a new VCF; without it many filtering commands only emit summary files.
- `--max-missing 1.0` keeps only sites with no missing genotypes, which is often much harsher than intended.
- Distinguish site filters from genotype-aware downstream interpretation; filtering can strongly bias frequency-based summaries.

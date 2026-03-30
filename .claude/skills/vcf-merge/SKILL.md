---
name: vcf-merge
description: Use when merging multiple VCF files by genomic position to create multi-sample VCFs from individual or fewer-sample VCFs.
disable-model-invocation: true
user-invocable: true
---

# vcf-merge

## Quick Start
- **Command**: `vcf-merge [OPTIONS] file1.vcf.gz file2.vcf.gz ... > out.vcf`
- **Local executable**: `/home/vimalinx/miniforge3/envs/bio/bin/vcf-merge`
- **Full reference**: See `references/help.md`

## When To Use This Tool

- Merge multiple bgzipped, indexed VCFs into one multi-sample VCF by genomic position.
- Combine per-sample or small-cohort VCFs that describe overlapping loci.
- Control how allele differences are collapsed at the same locus.
- Use `vcf-concat` instead when files are already split by chromosome or disjoint genomic blocks.

## Common Patterns

```bash
# 1) Standard merge
vcf-merge sample1.vcf.gz sample2.vcf.gz > merged.vcf
```

```bash
# 2) Stricter merge behavior with no allele collapsing
vcf-merge \
  -c none \
  sample1.vcf.gz sample2.vcf.gz sample3.vcf.gz \
  > merged.vcf
```

```bash
# 3) Restrict the merge to target regions
vcf-merge \
  -r regions.txt \
  sample1.vcf.gz sample2.vcf.gz \
  > merged.regions.vcf
```

## Recommended Workflow

1. Bgzip and tabix-index every input VCF before merging.
2. Choose the `-c/--collapse` policy deliberately because it changes how same-position allele differences are treated.
3. Write the merged VCF to a new file, then compress and index it if it will be queried later.
4. Check sample columns and duplicate-position handling before trusting the merged callset.

## Guardrails

- All inputs must be bgzipped and tabix-indexed.
- This is positional merging, not file concatenation.
- `-d` removes duplicate consecutive rows by keeping only the first, which can hide data loss if used casually.
- `-R` fills missing genotypes with a user-supplied reference-style string such as `0/0`; be explicit about ploidy assumptions if you use it.

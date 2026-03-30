---
name: vcf-contrast
description: Use when comparing variant samples against background samples to identify unique genotypes and novel variants in VCF files.
disable-model-invocation: true
user-invocable: true
---

# vcf-contrast

## Quick Start

- **Command**: `vcf-contrast +<variant_samples> -<background_samples> [OPTIONS] file.vcf.gz`
- **Local executable**: `/home/vimalinx/miniforge3/envs/bio/bin/vcf-contrast`
- **Full reference**: See [references/help.md](references/help.md)

## When To Use This Tool

- Contrast one sample group against another within a multi-sample VCF.
- Identify sites where case or focal samples carry genotypes or alleles absent from background samples.
- Add `NOVELGT`, `NOVELAL`, and `NOVELTY` INFO annotations for downstream filtering or reporting.
- Perform quick cohort-difference scans without writing a custom comparison script.

## Common Patterns

```bash
# 1) Find variants present in A,B but absent from C,D,E
vcf-contrast \
  +A,B \
  -C,D,E \
  cohort.vcf.gz
```

```bash
# 2) Report only sites with novel genotypes
vcf-contrast \
  -n \
  +cases1,cases2 \
  -controls1,controls2,controls3 \
  cohort.vcf.gz
```

```bash
# 3) Require minimum depth and respect FILTER status
vcf-contrast \
  +tumor \
  -normal \
  -d 10 \
  -f \
  cohort.vcf.gz
```

## Recommended Workflow

1. Prepare a bgzip-compressed VCF file containing all samples to be compared
2. Identify the samples expected to have unique variants (+<list>) and the background control samples (-<list>)
3. Run `vcf-contrast +A,B -C,D,E [OPTIONS] file.vcf.gz` with flags such as `-n` to output only novel sites or `-f` to apply filters
4. Pipe output to `vcf-query` or other tools to extract and format the annotated fields of interest

## Guardrails

- Both variant sample list (+<list>) and background sample list (-<list>) are required arguments
- Input VCF must be bgzip-compressed with `.vcf.gz` extension
- Haploid genotypes are internally treated as homozygous diploid; "0/1" and "1" are considered different genotypes
- `-n` limits output to novel sites only; without it, the tool still emits all records, just with additional INFO annotations
- `-f` discards rows whose FILTER is neither `PASS` nor `.`, which changes the comparison universe before novelty is computed

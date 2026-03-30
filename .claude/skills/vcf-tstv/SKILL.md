---
name: vcf-tstv
description: Use when you need to calculate the transition/transversion (Ts/Tv) ratio from VCF files for variant call quality assessment.
disable-model-invocation: true
user-invocable: true
---

# vcf-tstv

## Quick Start

- **Command**: `cat file.vcf | vcf-tstv`
- **Local executable**: `/home/vimalinx/miniforge3/envs/bio/bin/vcf-tstv`
- **Reference**: See [references/help.md](references/help.md) for full options

## When To Use This Tool

- Compute a quick transition/transversion ratio from a VCF stream.
- Perform a lightweight QC sanity check on SNP callsets.
- Compare Ts/Tv behavior between filtered and unfiltered VCFs in a shell pipeline.
- Use a legacy vcftools helper when a simple one-number summary is enough.

## Common Patterns

```bash
# 1) Calculate Ts/Tv from a plain VCF
cat file.vcf | vcf-tstv
```

```bash
# 2) Calculate Ts/Tv from a compressed VCF stream
gunzip -c file.vcf.gz | vcf-tstv
```

```bash
# 3) Evaluate Ts/Tv after an upstream SNP-only filter
bcftools view -v snps filtered.vcf.gz | vcf-tstv
```

## Recommended Workflow

1. Ensure your VCF file is valid and contains SNP variants
2. Pipe the VCF to the tool: `cat file.vcf | vcf-tstv`
3. Review the reported Ts/Tv ratio
4. Compare against expected values for your sample type (e.g., ~2.0–2.1 for human whole-genome data)

## Guardrails

- Accepts VCF input via stdin only; no file path arguments supported
- Only supports `-h` for help; no filtering or output formatting options
- Does not support `--version`; verify via bioconda/vcftools package info
- Treat the result as a rough QC metric; the expected Ts/Tv depends strongly on organism, assay, region selection, and filtering state
- For meaningful comparison, make sure upstream filtering and SNP selection are consistent across the callsets you compare

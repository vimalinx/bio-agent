---
name: fill-an-ac
description: Use when you need to populate or update AC (allele count) fields in VCF files from the vcftools suite.
disable-model-invocation: true
user-invocable: true
---

# fill-an-ac

## Quick Start

- **Command:** `fill-an-ac < in.vcf > out.vcf`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/fill-an-ac`
- **Full reference:** See [references/help.md](references/help.md) for complete options

## When To Use This Tool

- Recalculate `AC` and `AN` INFO fields from genotype columns.
- Normalize VCFs that are missing allele-count metadata after genotype edits or sample filtering.
- Add fresh allele-count annotations before downstream frequency-based filtering or QC.

## Common Patterns

```bash
# 1) Recalculate AC and AN from a VCF stream
fill-an-ac < input.vcf > output.vcf
```

```bash
# 2) Use an explicit input filename and bgzip the result
fill-an-ac input.vcf | bgzip -c > output.vcf.gz
```

## Recommended Workflow

1. Start from a genotype-containing VCF with valid sample columns.
2. Run `fill-an-ac` from stdin or by passing a single input filename.
3. Inspect the header to confirm both `AC` and `AN` INFO definitions were added.
4. Spot-check a few sites before using the recalculated counts downstream.

## Guardrails

- The script accepts either stdin or one filename argument; it is not stdin-only.
- `--help` works, but `--version` is not implemented and errors as an unknown parameter.
- The recalculation is hard-coded as `recalc_ac_an(2)`, so it assumes diploid genotype counting.
- Existing `AC` / `AN` content is recomputed from genotypes rather than preserved verbatim.

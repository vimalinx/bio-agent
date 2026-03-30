---
name: vcf-to-tab
description: Use when converting VCF genotype data to simple tabular format for downstream analysis or reporting.
disable-model-invocation: true
user-invocable: true
---

# vcf-to-tab

## Quick Start
- **Command:** `vcf-to-tab [OPTIONS] < in.vcf > out.tab`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/vcf-to-tab`
- **Full reference:** See `references/help.md`

## When To Use This Tool

- Convert a streamed VCF into a simple tabular representation quickly.
- Emit IUPAC-coded alleles if that specific output style is needed.
- Keep using it only in legacy vcftools-style stream pipelines; for new work, prefer `bcftools query`.

## Common Patterns

```bash
# 1) Convert a plain VCF stream to tab
cat input.vcf | vcf-to-tab > out.tab
```

```bash
# 2) Use IUPAC ambiguity codes
cat input.vcf | vcf-to-tab -i > out.iupac.tab
```

## Recommended Workflow

1. Stream a valid VCF into stdin.
2. Decide whether ambiguity codes are needed with `-i`.
3. Write the tabular output to a file and inspect a few lines for column expectations.
4. Move to `bcftools query` if the output specification starts to become more complex than this script can express.

## Guardrails

- This is a deprecated vcftools utility; `bcftools query` is the preferred modern replacement.
- Input is stdin-driven and output is stdout-driven.
- `--version` is not supported in the usual way; use `-h` for interface help.
- Because the format is simple and opinionated, do not expect the field-level flexibility of `bcftools query`.

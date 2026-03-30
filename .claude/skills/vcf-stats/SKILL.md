---
name: vcf-stats
description: Use when computing statistics on VCF files, filtering variant data by quality or fields, or generating summary reports from gzipped VCF inputs.
disable-model-invocation: true
user-invocable: true
---

# vcf-stats

## Quick Start
- **Command**: `vcf-stats [OPTIONS] file.vcf.gz`
- **Local executable**: `/home/vimalinx/miniforge3/envs/bio/bin/vcf-stats`
- **Full reference**: See `references/help.md`

## When To Use This Tool

- Generate summary statistics and sample-aware reports from a gzipped VCF.
- Slice statistics by FILTER, QUAL, INFO, FORMAT, or sample-specific fields.
- Produce reusable dump files or prefixed output directories from vcftools-style stats runs.
- Use it mainly when you are already in a vcftools workflow; for broader modern VCF reporting, `bcftools stats` is often a better default.

## Common Patterns

```bash
# 1) Generate stats with a quality and filter breakdown
vcf-stats \
  file.vcf.gz \
  -f FILTER,QUAL=10:200 \
  -p out/
```

```bash
# 2) Generate stats for a single sample
vcf-stats \
  file.vcf.gz \
  -f SAMPLE/NA00001/DP=1:200 \
  -p out/
```

```bash
# 3) Save a dump that can be replayed later
vcf-stats file.vcf.gz > perl.dump
```

## Recommended Workflow

1. Start from a gzipped VCF and decide whether you want all samples or a subset with `-s`.
2. Specify one or more filter expressions with `-f` to control which summaries are produced.
3. Use `-p` to keep outputs grouped in a predictable directory or prefix.
4. Review the generated summaries before turning them into dashboards or QC gates.

## Guardrails

- Input is expected to be a gzipped VCF.
- `-f` expressions are powerful but easy to misuse; double-check field paths like `INFO/INDEL` or `SAMPLE/NAME/DP`.
- Excluding irrelevant samples with `-s` can materially improve runtime on large cohorts.
- This tool does not provide a normal `--version` path; use `-h` for interface confirmation.

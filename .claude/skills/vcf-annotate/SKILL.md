---
name: vcf-annotate
description: Use when annotating VCF files with custom annotations, applying filters, or modifying INFO/ID/QUAL/FILTER columns.
disable-model-invocation: true
user-invocable: true
---

# vcf-annotate

## Quick Start
- **Command**: `vcf-annotate [OPTIONS] < in.vcf > out.vcf`
- **Local executable**: `/home/vimalinx/miniforge3/envs/bio/bin/vcf-annotate`
- **Full reference**: See `references/help.md`

## When To Use This Tool

- Add INFO, FILTER, ID, or QUAL annotations to a streamed VCF.
- Recalculate AC/AN, HWE, inbreeding coefficient, or TYPE tags on an existing callset.
- Apply built-in heuristic filters or custom annotation overlays from a tabix-indexed side table.
- Keep using it mainly when you are already in a vcftools-based stream workflow; for newer pipelines, `bcftools annotate` is often a better long-term choice.

## Common Patterns

```bash
# 1) Add custom annotations from a tabix-indexed table
zcat input.vcf.gz \
  | vcf-annotate \
      -a annotations.gz \
      -c CHROM,FROM,TO,INFO/GN \
      -d "key=INFO,ID=GN,Number=1,Type=String,Description='Gene Name'" \
  | bgzip -c > output.vcf.gz
```

```bash
# 2) Recalculate allele count tags and variant type
zcat input.vcf.gz \
  | vcf-annotate --fill-AC-AN --fill-type \
  | bgzip -c > output.vcf.gz
```

```bash
# 3) Remove tags and apply built-in filters
zcat input.vcf.gz \
  | vcf-annotate -r INFO/DP,FILTER -f +/Q=20/d=5 \
  | bgzip -c > output.vcf.gz
```

## Recommended Workflow

1. Decide whether you are annotating from a side table, recalculating tags, or filtering records.
2. If using external annotations, prepare a bgzipped tabix-indexed table and matching header descriptions up front.
3. Stream the VCF through `vcf-annotate`, then recompress the output if the result will be indexed or reused.
4. Check the output header and a few representative records before pushing the file downstream.

## Guardrails

- This tool is stream-oriented: VCF input comes from stdin and output goes to stdout.
- Annotation files given with `-a` must be tabix-indexed and their column mapping in `-c` must match reality.
- `-H/--hard-filter` removes records failing FILTER, which is much more destructive than merely annotating them.
- `--normalize-alleles` can change REF/ALT representation; only use it when downstream expectations are clear.

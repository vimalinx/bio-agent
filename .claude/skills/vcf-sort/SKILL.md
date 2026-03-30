---
name: vcf-sort
description: Use when VCF files need sorting by chromosome and position, particularly before downstream analysis or indexing. Pipes VCF input through stdin.
disable-model-invocation: true
user-invocable: true
---

# vcf-sort

## Quick Start
- **Command:** `vcf-sort [options] < input.vcf > sorted.vcf`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/vcf-sort`
- **Full reference:** See `references/help.md`

## When To Use This Tool

- Sort an unsorted VCF before indexing or downstream comparison.
- Apply natural chromosome ordering with `-c` instead of raw lexicographic order.
- Repair ordering after concatenation or ad hoc editing.
- Prefer `bcftools sort` in newer pipelines if you want a more actively maintained implementation.

## Common Patterns

```bash
# 1) Sort a plain-text VCF from stdin
cat input.vcf | vcf-sort > sorted.vcf
```

```bash
# 2) Use natural chromosome ordering
zcat input.vcf.gz | vcf-sort -c > sorted.vcf
```

```bash
# 3) Set a custom temp directory for large sorts
zcat input.vcf.gz | vcf-sort -t /scratch > sorted.vcf
```

## Recommended Workflow

1. Decompress or stream the input into stdin because `vcf-sort` is stdin-driven.
2. Use `-c` when chromosome-like names should follow natural version order.
3. Write the sorted output to a new file, then recompress and index it if later tools expect `.vcf.gz`.
4. Validate sort order before assuming region-based tools will behave correctly.

## Guardrails

- This utility reads from stdin and writes to stdout; it does not take an input filename as a positional argument.
- Natural chromosome ordering with `-c` depends on a `sort` implementation that supports `--version-sort`.
- Header lines are preserved at the top, but malformed body records can still propagate into the output.
- Remember to `bgzip` and `tabix` the result if downstream tools require indexed compressed VCF.

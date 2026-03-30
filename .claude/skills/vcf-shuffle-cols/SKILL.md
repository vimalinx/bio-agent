---
name: vcf-shuffle-cols
description: Use when you need to reorder sample columns in a VCF file to match the column order of a template VCF.
disable-model-invocation: true
user-invocable: true
---

# vcf-shuffle-cols

## Quick Start
- **Command:** `vcf-shuffle-cols -t template.vcf[.gz] input.vcf[.gz] > output.vcf`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/vcf-shuffle-cols`
- **Fallback launcher in this workspace:** `/home/vimalinx/miniforge3/envs/bio/bin/perl /home/vimalinx/miniforge3/envs/bio/bin/vcf-shuffle-cols`
- **Full reference:** See `references/help.md`

## When To Use This Tool

- Reorder sample columns in one VCF to match a trusted template VCF.
- Normalize sample order before joins, comparisons, or downstream tools that assume aligned sample columns.
- Fix order mismatches without rewriting the variant content itself.
- Use stdin as the data source when the input VCF is already being streamed.

## Common Patterns

```bash
# 1) Reorder one VCF to match a template
/home/vimalinx/miniforge3/envs/bio/bin/perl \
  /home/vimalinx/miniforge3/envs/bio/bin/vcf-shuffle-cols \
  -t template.vcf.gz \
  input.vcf.gz > reordered.vcf
```

```bash
# 2) Stream the input VCF from stdin
gunzip -c input.vcf.gz | \
  /home/vimalinx/miniforge3/envs/bio/bin/perl \
  /home/vimalinx/miniforge3/envs/bio/bin/vcf-shuffle-cols \
  -t template.vcf.gz > reordered.vcf
```

```bash
# 3) Reorder before a phased join
/home/vimalinx/miniforge3/envs/bio/bin/perl \
  /home/vimalinx/miniforge3/envs/bio/bin/vcf-shuffle-cols \
  -t chunk1.vcf \
  chunk2.vcf > chunk2.reordered.vcf
```

## Recommended Workflow

1. Pick a template VCF whose sample names and order you trust.
2. Verify the input and template contain the same sample set before reordering.
3. Run the shuffle step and write to a new file, then use that normalized VCF in downstream joins or comparisons.
4. Recompress and reindex afterward if the next tool expects `.vcf.gz` plus tabix.

## Guardrails

- In this shell, direct invocation may fail with `Can't locate Vcf.pm`; activate the bio environment first or call the script through `/home/vimalinx/miniforge3/envs/bio/bin/perl`.
- The template is required via `-t`; the script errors if sample names do not match one-to-one.
- The common usage examples show `.vcf.gz`, but the script itself can read a file argument or stdin; compression is not the core requirement.
- Output is written to stdout, so always redirect it.
- This only reorders columns; it does not reconcile missing samples, merge records, or fix variant-level inconsistencies.

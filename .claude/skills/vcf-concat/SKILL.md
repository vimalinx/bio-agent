---
name: vcf-concat
description: Use when concatenating VCF files split by chromosome or when merging multiple gzipped VCFs into a single output.
disable-model-invocation: true
user-invocable: true
---

# vcf-concat

## Quick Start
- **Command:** `vcf-concat [OPTIONS] A.vcf.gz B.vcf.gz C.vcf.gz > out.vcf`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/vcf-concat`
- **Full reference:** See `references/help.md`

## When To Use This Tool

- Concatenate VCFs that represent adjacent genomic partitions, often by chromosome.
- Check that multiple VCFs share compatible sample columns before joining.
- Allow small overlaps with merge-sort behavior when partition boundaries are slightly messy.
- Pad missing columns with `.` when joining sex-chromosome or otherwise asymmetric sample tables.

## Common Patterns

```bash
# 1) Concatenate chromosome-split VCFs
vcf-concat chr1.vcf.gz chr2.vcf.gz chr3.vcf.gz > cohort.vcf
```

```bash
# 2) Read the file list from disk
vcf-concat -f vcf_files.txt > cohort.vcf
```

```bash
# 3) Check column compatibility without concatenating
vcf-concat -c chr1.vcf.gz chr2.vcf.gz chr3.vcf.gz
```

## Recommended Workflow

1. Confirm the files are truly concatenable and not meant for positional merging.
2. Use `-c` once before large concatenation jobs if there is any doubt about column consistency.
3. If files have small overlaps, set `-s` deliberately and understand that it is only a partial merge sort.
4. Recompress and index the result if later tools expect `.vcf.gz`.

## Guardrails

- This is for concatenation of genomic partitions, not for multi-sample merging at shared loci.
- Input columns should match unless you knowingly use `-p/--pad-missing`.
- `-s` is not a general-purpose sorter; it is only for limited overlap handling.
- `--version` is not supported in the usual way here; use `-h` for interface help.

---
name: fill-ref-md5
description: Use when VCF headers need reference and contig tags with MD5 checksums per VCFv4.1 specification.
disable-model-invocation: true
user-invocable: true
---

# fill-ref-md5

## Quick Start

- Command: `fill-ref-md5 [OPTIONS] in.vcf.gz out.vcf.gz`
- Local executable: `/home/vimalinx/miniforge3/envs/bio/bin/fill-ref-md5`
- Reference: see `references/help.md` for full options and examples

## When To Use This Tool

- Add `reference` and `contig` header lines with MD5 checksums to a compressed VCF.
- Make a VCF header more compliant with the VCFv4.1-style reference metadata recommendations.
- Populate missing contig MD5 values from a reference FASTA before data sharing or downstream indexing.

## Common Patterns

```bash
# 1) Compute MD5s from a reference FASTA and cache them in a dictionary
fill-ref-md5 -r ref.fa -d ref.fa.dict in.vcf.gz out.vcf.gz
```

```bash
# 2) Add assembly/species/taxonomy annotations to contig header lines
fill-ref-md5 \
  -r ref.fa \
  -d ref.fa.dict \
  -i AS:GRCh38,SP:"Homo sapiens",TX:9606 \
  in.vcf.gz out.vcf.gz
```

## Recommended Workflow

1. Ensure input VCF is bgzip-compressed and tabix-indexed
2. Prepare reference FASTA indexed by `samtools faidx`
3. Run `fill-ref-md5 -r ref.fa -d ref.fa.dict in.vcf.gz out.vcf.gz`
4. Verify output VCF header contains new reference/contig tags

## Guardrails

- Input VCF must be compressed and tabix-indexed
- Reference FASTA must be indexed by samtools faidx
- Dictionary file opens in append mode; existing records are not modified
- You need at least one of `-d` or `-r`; `-d` alone only works if the dictionary already contains all required chromosomes.
- `--help` works, but `--version` is not implemented and errors as an unknown parameter.
- The script shells out to `tabix`, `samtools faidx`, and `md5sum`, so those helpers must be available.

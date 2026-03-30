---
name: vcf-convert
description: Use when converting VCF files between format versions (4.0, 4.1, 4.2) for compatibility with downstream bioinformatics tools.
disable-model-invocation: true
user-invocable: true
---

# vcf-convert

## Quick Start
- **Command:** `vcf-convert -v <4.0|4.1|4.2> [options] < in.vcf > out.vcf`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/vcf-convert`
- **Fallback launcher in this workspace:** `/home/vimalinx/miniforge3/envs/bio/bin/perl /home/vimalinx/miniforge3/envs/bio/bin/vcf-convert`
- **Full reference:** See `references/help.md`

## When To Use This Tool

- Convert a VCF stream between versions 4.0, 4.1, and 4.2 for downstream compatibility.
- Upgrade older VCFs before handing them to newer tooling.
- Normalize indel representation during version conversion when you can provide the reference FASTA.
- Keep using it only if you already depend on the vcftools Perl helpers; for fresh pipelines, prefer modern `bcftools`-based normalization when possible.

## Common Patterns

```bash
# 1) Upgrade an older SNP-only VCF to 4.2
/home/vimalinx/miniforge3/envs/bio/bin/perl \
  /home/vimalinx/miniforge3/envs/bio/bin/vcf-convert \
  -v 4.2 \
  < input.vcf > output.vcf
```

```bash
# 2) Convert an indel-containing VCF with a faidx-indexed reference
/home/vimalinx/miniforge3/envs/bio/bin/perl \
  /home/vimalinx/miniforge3/envs/bio/bin/vcf-convert \
  -v 4.2 \
  -r ref.fa \
  < input.vcf > output.vcf
```

```bash
# 3) Downgrade cautiously for an older consumer
/home/vimalinx/miniforge3/envs/bio/bin/perl \
  /home/vimalinx/miniforge3/envs/bio/bin/vcf-convert \
  -v 4.1 \
  < input.vcf > output.vcf
```

## Recommended Workflow

1. Confirm which VCF version the downstream tool actually requires before converting anything.
2. Treat the input as a stream: feed it on stdin and capture the converted VCF from stdout.
3. Provide `-r ref.fa` whenever non-SNP variants are present so indel REF / ALT rewriting is well-defined.
4. Validate the output with a downstream parser or `vcf-validator` before swapping it into a pipeline.

## Guardrails

- In this shell, direct invocation may fail with `Can't locate Vcf.pm`; activate the bio environment first or call the script through `/home/vimalinx/miniforge3/envs/bio/bin/perl`.
- The `-v/--version` option sets the target VCF format version; it is not a program-version flag.
- Downgrading VCF versions is explicitly marked upstream as experimental.
- Indel conversion needs a samtools-faidx indexed reference FASTA via `-r`.
- This tool reads from stdin and writes to stdout; it does not edit files in place.

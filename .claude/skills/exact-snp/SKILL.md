---
name: exact-snp
description: Use when calling SNPs from aligned SAM/BAM reads with Subread's `exactSNP` variant caller.
disable-model-invocation: true
user-invocable: true
---

# exact-snp

## Quick Start

- **Command:** `exactSNP -i <alignment.sam|bam> -g <reference.fa> -o <output.vcf>`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/exactSNP`
- **Full reference:** See [references/help.md](references/help.md) for complete options and examples

## When To Use This Tool

- Calling SNPs from read mapping results in SAM or BAM format
- Leveraging known annotated SNPs (e.g., dbSNP) to improve calling accuracy
- Outputting discovered variants in VCF format

## Common Patterns

```bash
# 1) Call SNPs from a SAM alignment
/home/vimalinx/miniforge3/envs/bio/bin/exactSNP \
  -i sample.sam \
  -g reference.fa \
  -o sample.vcf
```

```bash
# 2) Call SNPs from BAM with multiple threads and known SNP support
/home/vimalinx/miniforge3/envs/bio/bin/exactSNP \
  -i sample.bam \
  -b \
  -g reference.fa \
  -a known_snps.vcf.gz \
  -T 8 \
  -o sample.vcf
```

## Recommended Workflow

1. Prepare a sorted SAM/BAM alignment file and a single FASTA reference genome
2. Optionally obtain annotated SNPs in VCF format (gzipped accepted) to supply via `-a`
3. Run exactSNP with required inputs (`-i`, `-g`, `-o`), using `-b` if input is BAM
4. Review the output VCF file for discovered SNPs

## Guardrails

- Input alignment must be SAM or BAM; specify `-b` when using BAM format
- Reference genome must be a single FASTA file
- Adjust `-r` (minimum coverage) and `-Q` (q-value cutoff) to filter low-confidence calls
- The real executable name is `exactSNP`; `exact-snp` is only the skill folder name.
- Running the binary with no arguments prints the full usage banner, while `-v` is the real version flag (`exactSNP v2.1.1`).
- The output file is VCF, despite the built-in example still using a `.txt` suffix.

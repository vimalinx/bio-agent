---
name: sam2vcf-pl
description: Use when converting old `samtools pileup -c` output into VCF and filtering for SNP-only or indel-only calls.
disable-model-invocation: true
user-invocable: true
---

# sam2vcf-pl

## Quick Start

- **Command:** `sam2vcf.pl [OPTIONS] < in.pileup > out.vcf`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/sam2vcf.pl`
- **Reference:** See [references/help.md](references/help.md)

## When To Use This Tool

- Convert legacy `samtools pileup -c` text output into VCF.
- Filter calls down to SNPs only with `-s` or indels only with `-i`.
- Keep reference alleles in the output with `-R` when a downstream comparison expects them.
- Rescue older pileup-based workflows that predate current `bcftools` calling conventions.

## Common Patterns

```bash
# 1) Convert old pileup output to VCF
samtools pileup -c ref.fa alignments.bam | sam2vcf.pl > calls.vcf
```

```bash
# 2) Emit SNPs only
samtools pileup -c ref.fa alignments.bam | sam2vcf.pl -s > snps.vcf
```

```bash
# 3) Emit indels and provide the reference sequence explicitly
samtools pileup -c ref.fa alignments.bam | sam2vcf.pl -i -r ref.fa > indels.vcf
```

## Recommended Workflow

1. Generate pileup input from an older `samtools pileup -c`-style workflow rather than modern `mpileup` defaults.
2. Decide whether you need all calls, SNPs only, or indels only before conversion.
3. Provide `-r ref.fa` whenever indels may appear in the input.
4. Inspect the resulting header and a few representative records before mixing this legacy VCF into newer pipelines.

## Guardrails

- This script expects legacy pileup text on stdin and emits VCFv3.3, not modern VCF4 output.
- `-r/--refseq` is required when indels are present.
- `--help` works, but `--version` is not implemented and exits as an unknown parameter.
- Do not combine `-s` and `-i`; treat them as mutually exclusive filters.

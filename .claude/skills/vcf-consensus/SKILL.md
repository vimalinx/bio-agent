---
name: vcf-consensus
description: Use when applying VCF variants to a reference FASTA to generate a consensus sequence.
disable-model-invocation: true
user-invocable: true
---

# vcf-consensus

## Quick Start
- **Command**: `cat ref.fa | vcf-consensus [OPTIONS] in.vcf.gz > out.fa`
- **Local executable**: `/home/vimalinx/miniforge3/envs/bio/bin/vcf-consensus`
- **Full reference**: See `references/help.md`

## When To Use This Tool

- Apply variants from a VCF onto a reference FASTA to create a consensus sequence.
- Produce sample-specific consensus from a multi-sample VCF.
- Emit haplotype-specific consensus or IUPAC-coded ambiguity consensus.
- Use it for targeted region reconstruction after extracting the exact reference segment you want.

## Common Patterns

```bash
# 1) Apply all variants to a reference segment
samtools faidx ref.fa chr1:1000-2000 \
  | vcf-consensus calls.vcf.gz \
  > consensus.fa
```

```bash
# 2) Make sample-specific consensus
samtools faidx ref.fa chr1:1000-2000 \
  | vcf-consensus -s SAMPLE1 calls.vcf.gz \
  > sample1.consensus.fa
```

```bash
# 3) Emit haplotype 1 or IUPAC consensus
samtools faidx ref.fa chr1:1000-2000 \
  | vcf-consensus -H 1 calls.vcf.gz \
  > hap1.fa
```

## Recommended Workflow

1. Decide which reference interval or contig you actually want to reconstruct.
2. Stream the matching FASTA sequence into stdin, ideally using `samtools faidx`.
3. Apply variants from the compressed VCF with optional sample or haplotype selection.
4. Inspect the resulting FASTA header and sequence length before treating it as final biological truth.

## Guardrails

- Reference FASTA comes from stdin; the tool does not read the FASTA by filename.
- The usual usage expects a compressed `.vcf.gz`.
- For targeted consensus, the FASTA header is expected in `>chr:from-to` style when using region slices.
- If the VCF has multiple samples, omitting `-s` applies all variants together, which is often not what you want.

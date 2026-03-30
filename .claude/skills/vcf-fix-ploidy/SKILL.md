---
name: vcf-fix-ploidy
description: Use when VCF files have incorrect ploidy annotations for sex chromosomes or mitochondrial DNA, particularly when processing samples with known sex but mismatched genotype fields.
disable-model-invocation: true
user-invocable: true
---

# vcf-fix-ploidy

## Quick Start
- **Command**: `cat input.vcf | vcf-fix-ploidy [OPTIONS] > output.vcf`
- **Local executable**: `/home/vimalinx/miniforge3/envs/bio/bin/vcf-fix-ploidy`
- **Full reference**: See `references/help.md`

## When To Use This Tool

- Repair genotype ploidy for sex chromosomes and mitochondrial DNA after a caller emitted inconsistent diploid-style genotypes.
- Adjust male/female expectations on X, Y, and MT using either a sample-sex file or an assumed default.
- Optionally fix genotype likelihood vectors to match the corrected ploidy.

## Common Patterns

```bash
# 1) Fix ploidy using a sample-sex file
cat input.vcf \
  | vcf-fix-ploidy -s samples.txt \
  > fixed.vcf
```

```bash
# 2) Assume female sex for unspecified samples
cat input.vcf \
  | vcf-fix-ploidy -s samples.txt -a F \
  > fixed.vcf
```

```bash
# 3) Also adjust genotype likelihoods
cat input.vcf \
  | vcf-fix-ploidy -s samples.txt -l \
  > fixed.vcf
```

## Recommended Workflow

1. Prepare a sample-sex file with one `sample_name [M|F]` pair per line.
2. Decide whether the default ploidy rules match your reference build and sex-chromosome conventions.
3. Stream the VCF through `vcf-fix-ploidy`, adding `-a` if the sex list is incomplete.
4. Validate a few representative X, Y, and MT records before propagating the fixed file further.

## Guardrails

- Input is stdin-driven; do not try to pass the VCF as a positional filename.
- If `-s` is incomplete, you need `-a` to define the assumed sex for missing samples.
- The built-in ploidy rules are reference- and convention-specific; override them with `-p` if your build differs.
- `-l/--fix-likelihoods` changes more than the GT field, so only use it when downstream tools care about PL/GL consistency.

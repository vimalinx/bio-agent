---
name: vcfutils-pl
description: Use when working with VCF file utilities from the bcftools bioconda package.
disable-model-invocation: true
user-invocable: true
---

# vcfutils-pl

## Quick Start
- **Command**: `vcfutils.pl <command> [arguments]`
- **Local executable**: `/home/vimalinx/miniforge3/envs/bio/bin/vcfutils.pl`
- **Reference**: See [references/help.md](references/help.md) for detailed usage

## When To Use This Tool

- Run legacy VCF helper subcommands bundled with the `bcftools` toolchain.
- Subset samples, list sample names, or fill `AC/AN` counts in VCF records.
- Compute quick quality statistics or apply the legacy `varFilter`.
- Convert all-site VCF output into consensus FASTQ with `vcf2fq`.

## Common Patterns

```bash
# 1) List sample names in a VCF
vcfutils.pl \
  listsam \
  cohort.vcf
```

```bash
# 2) Fill AC/AN fields from genotypes
vcfutils.pl \
  fillac \
  cohort.vcf \
  > cohort.with-ac.vcf
```

```bash
# 3) Apply the legacy short-variant filter helper
vcfutils.pl \
  varFilter \
  cohort.vcf \
  > cohort.filtered.vcf
```

```bash
# 4) Build a consensus FASTQ from an all-site VCF
vcfutils.pl \
  vcf2fq \
  all-sites.vcf \
  > consensus.fq
```

## Recommended Workflow

1. Start by choosing the subcommand that matches the task, because `vcfutils.pl` is a command multiplexer rather than a single-purpose tool.
2. Validate whether the chosen subcommand expects ordinary VCF input, an all-site VCF, a `.fai`, or bcftools-specific annotations.
3. Run the subcommand and redirect output into a new file, because most modes write transformed text to stdout.
4. Re-validate the resulting VCF/FASTQ before plugging it into downstream analysis.

## Guardrails

- The first argument must be a subcommand such as `listsam`, `fillac`, `qstats`, `varFilter`, or `vcf2fq`; `-h`, `--help`, and `--version` are not valid top-level help flags.
- `fillac` expects the `GT` field to be present and to appear first in the FORMAT column.
- `vcf2fq` is intended for all-site, position-sorted VCF input and will complain about unsorted data.
- `varFilter` and some related commands rely on annotations produced by the SAMtools/BCFtools legacy calling pipeline.

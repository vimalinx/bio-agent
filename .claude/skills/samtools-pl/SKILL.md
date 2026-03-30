---
name: samtools-pl
description: Use when working with samtools.pl, a Perl CLI utility installed by the bioconda samtools package.
disable-model-invocation: true
user-invocable: true
---

# samtools-pl

## Quick Start
- **Command**: `samtools.pl <command> [arguments]`
- **Local executable**: `/home/vimalinx/miniforge3/envs/bio/bin/samtools.pl`
- **Reference**: See [references/help.md](references/help.md) for detailed usage information

## When To Use This Tool

- Run legacy helper subcommands bundled with SAMtools.
- Compute alignment lengths from CIGAR strings with `showALEN`.
- Filter legacy consensus pileup variant calls with `varFilter`.
- Convert legacy `pileup -c` output into FASTQ-like consensus sequence with `pileup2fq`.

## Common Patterns

```bash
# 1) Append alignment length derived from the CIGAR string
samtools.pl \
  showALEN \
  alignments.sam
```

```bash
# 2) Filter SNPs and short indels from legacy cns-pileup output
samtools.pl \
  varFilter \
  calls.cns-pileup \
  > calls.filtered.txt
```

```bash
# 3) Convert legacy pileup consensus output into FASTQ
samtools.pl \
  pileup2fq \
  calls.cns-pileup \
  > consensus.fq
```

## Recommended Workflow

1. Start by choosing the subcommand, because `samtools.pl` is a small helper-script collection rather than a single analysis tool.
2. Confirm the input format matches the chosen subcommand, especially for the legacy `cns-pileup`-based modes.
3. Run the helper and redirect the text output to a new file for inspection.
4. Validate the output before using it in modern SAM/BAM/VCF workflows, since these helpers target older SAMtools pipelines.

## Guardrails

- The first argument must be a subcommand such as `showALEN`, `varFilter`, or `pileup2fq`; `-h`, `--help`, and `--version` are not valid top-level actions.
- `varFilter` and `pileup2fq` operate on legacy `cns-pileup` output, not modern VCF or mpileup-by-default formats.
- `showALEN` reads SAM-like alignment text and derives an alignment length from the CIGAR string.
- This is a legacy helper script; check whether a modern native `samtools` or `bcftools` subcommand would be more appropriate before building new pipelines around it.

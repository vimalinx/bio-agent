---
name: blast2sam-pl
description: Use when converting legacy plain-text blastn output into SAM records for downstream SAM/BAM-compatible tooling.
disable-model-invocation: true
user-invocable: true
---

# blast2sam-pl

## Quick Start

- **Command**: `blast2sam.pl [-s] [-d] input.blast > output.sam`
- **Local executable**: `/home/vimalinx/miniforge3/envs/bio/bin/blast2sam.pl`
- **Full reference**: See [references/help.md](references/help.md)

## When To Use This Tool

- Convert legacy default-format `blastn` text output into SAM records.
- Bridge older BLAST workflows into `samtools` or other SAM/BAM-aware tooling.
- Emit aligned query sequence with `-s` when downstream tools need SAM field 10 populated.
- Emit dummy quality scores with `-d` when a downstream parser insists on SAM field 11.

## Common Patterns

```bash
# 1) Convert legacy BLASTN text output into headerless SAM
blast2sam.pl \
  alignments.blast > alignments.sam
```

```bash
# 2) Include aligned query sequence plus dummy qualities
blast2sam.pl \
  -sd \
  alignments.blast > alignments.with-seq.sam
```

```bash
# 3) Add a SAM header afterwards for downstream tools that require one
blast2sam.pl -sd alignments.blast > alignments.sam
samtools view -hT reference.fa alignments.sam > alignments.with-header.sam
```

## Recommended Workflow

1. Generate legacy `blastn` output in the default pairwise text format, not tabular or XML output.
2. Convert it with `blast2sam.pl`, adding `-s` if downstream tools need sequence and `-d` if they also need quality strings.
3. Add a SAM header separately if the next tool expects one.
4. Inspect a few records before batch conversion, especially strand flag, position, CIGAR, and sequence fields.

## Guardrails

- This parser is tailored to legacy plain-text `blastn` output; it is not the right tool for BLAST tabular, XML, JSON, or generic BLAST+ `-outfmt` outputs.
- `--help` works via Perl `Getopt::Std`, but `-help` is wrong here and is split into `-h -e -l -p`, which produces unknown-option errors.
- `-s` prints the aligned query sequence, not necessarily the original full read sequence from FASTQ input.
- `-d` fills SAM field 11 with dummy `I` characters (Phred 40 style); use that only when fake quality scores are acceptable.
- Output is headerless and queries without alignments are omitted rather than emitted as unmapped SAM records.

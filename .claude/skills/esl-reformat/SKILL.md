---
name: esl-reformat
description: Use when you need to convert sequence files between different formats such as FASTA, Stockholm, A2M, Clustal, or Phylip.
disable-model-invocation: true
user-invocable: true
---

# esl-reformat

## Quick Start

- **Command**: `esl-reformat [-options] <format> <seqfile>`
- **Local executable**: `/home/vimalinx/miniforge3/envs/bio/bin/esl-reformat`
- **Full reference**: See `references/help.md` for complete format options

## When To Use This Tool

- Use `esl-reformat` when you need to convert sequence or alignment files between Easel-supported formats.
- It is appropriate for both unaligned sequence files and aligned MSA formats such as Stockholm, AFA, Clustal, and Phylip.
- Use it when downstream HMMER/Easel tools require a specific format or when you want to normalize case, alphabet, gaps, or naming during conversion.
- It is also handy for simple alignment cleanup such as dropping all-gap columns with `--mingap` or all gapped columns with `--nogap`.

## Common Patterns

```bash
# Convert Stockholm alignment to aligned FASTA
esl-reformat afa alignment.sto > alignment.afa

# Convert FASTA DNA to RNA alphabet
esl-reformat -r fasta transcripts.fa > transcripts.rna.fa

# Remove all-gap columns from an alignment during conversion
esl-reformat --mingap stockholm alignment.sto > alignment.trimmed.sto

# Rename sequences sequentially in the output
esl-reformat --rename seq fasta sequences.fa > renamed.fa
```

## Recommended Workflow

1. Identify your input sequence file and desired output format
2. Check available options: `esl-reformat -h`
3. Run conversion: `esl-reformat <format> <seqfile> > output.ext`
4. Verify output format and sequence integrity

## Guardrails

- Use `-h` for help; `--help` and `--version` are not valid options
- Output format must match one of the supported formats exactly
- Input file must contain recognizable sequence data in a supported format
- Some options only make sense for alignments (`--mingap`, `--nogap`) or for specific output formats (for example `--namelen` with PHYLIP)

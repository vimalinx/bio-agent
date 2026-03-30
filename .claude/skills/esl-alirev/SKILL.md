---
name: esl-alirev
description: Use when you need to reverse sequences in a multiple sequence alignment file. Part of the Easel toolkit distributed with HMMER.
disable-model-invocation: true
user-invocable: true
---

# esl-alirev

## Quick Start

- **Command:** `esl-alirev [-options] <msafile>`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/esl-alirev`
- **Full reference:** See [references/help.md](references/help.md) for detailed options (use `esl-alirev -h` to view)

## When To Use This Tool

- Use `esl-alirev` when an alignment must be reverse-complemented as an alignment rather than as individual raw sequences.
- It is appropriate for DNA or RNA MSAs where the reverse orientation is needed for comparison or downstream analysis.
- Use it when you need the output alignment preserved in a chosen MSA format via `--outformat`.
- This is not a generic nucleotide reverse-complement tool for unaligned FASTA; it is alignment-oriented.

## Common Patterns

```bash
# Reverse-complement an RNA alignment
esl-alirev --rna alignment.sto > alignment.rev.sto

# Reverse-complement a DNA alignment and emit aligned FASTA
esl-alirev --dna --outformat afa alignment.sto > alignment.rev.afa

# Declare the input format explicitly
esl-alirev --informat stockholm --rna alignment.sto > alignment.rev.sto
```

## Recommended Workflow

1. Verify your input MSA file format is supported by Easel
2. Run `esl-alirev -h` to review available options
3. Execute `esl-alirev [options] <msafile>` on your alignment
4. Validate the output alignment contains reversed sequences as expected

## Guardrails

- Use `-h` (not `--help` or `--version`) to access help
- Ensure input file is a valid multiple sequence alignment
- Check output integrity after reversal operations
- Set `--dna` or `--rna` explicitly so the reverse-complement logic uses the correct alphabet

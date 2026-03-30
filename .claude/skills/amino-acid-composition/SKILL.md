---
name: amino-acid-composition
description: Use when counting amino-acid letters in raw protein sequence lines inside simple EDirect text pipelines.
disable-model-invocation: true
user-invocable: true
---

# amino-acid-composition

CLI tool from the Entrez Direct (EDirect) package for computing amino acid composition of protein sequences.

## Quick Start

- **Command:** `printf 'ACDE\n' | PATH=/home/vimalinx/miniforge3/envs/bio/bin:$PATH /home/vimalinx/miniforge3/envs/bio/bin/amino-acid-composition`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/amino-acid-composition`
- **Full reference:** See [references/help.md](references/help.md) for complete options and examples

## When To Use This Tool

- Count amino-acid letters in one raw sequence line at a time.
- Emit a fixed 26-row three-letter abbreviation table for each input line.
- Do quick composition checks in lightweight EDirect or shell pipelines where a full FASTA parser would be overkill.

## Common Patterns

```bash
# 1) Count amino acids in a single raw sequence line
printf 'ACDE\n' | \
  PATH=/home/vimalinx/miniforge3/envs/bio/bin:$PATH \
  /home/vimalinx/miniforge3/envs/bio/bin/amino-acid-composition
```

```bash
# 2) Strip FASTA headers first if your input came from a FASTA file
grep -v '^>' proteins.fa | \
  PATH=/home/vimalinx/miniforge3/envs/bio/bin:$PATH \
  /home/vimalinx/miniforge3/envs/bio/bin/amino-acid-composition
```

## Recommended Workflow

1. Feed only raw sequence lines on stdin.
2. Remove FASTA headers and any non-sequence metadata before running the tool.
3. Interpret each 26-row block as the composition for one input line.
4. Aggregate across lines separately if you need per-file rather than per-line totals.

## Guardrails

- This script does not parse FASTA records. A header line such as `>p1` will be treated as sequence text and counted.
- Non-letter characters are stripped, output is case-insensitive, and each input line is processed independently.
- The wrapper depends on the EDirect helper `sort-uniq-count`, so keep the bio / EDirect bin directory on `PATH`.
- Output covers all 26 alphabet letters via three-letter labels (`Ala`, `Asx`, `Xle`, `Pyl`, `Sec`, `Xxx`, `Glx`, etc.), not just the canonical 20 amino acids.

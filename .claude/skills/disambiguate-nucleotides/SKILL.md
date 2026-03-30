---
name: disambiguate-nucleotides
description: Use when expanding IUPAC ambiguous nucleotide strings into all concrete DNA sequences in shell or EDirect pipelines.
disable-model-invocation: true
user-invocable: true
---

# disambiguate-nucleotides

## Quick Start

- **Command:** `echo RCCGGY | disambiguate-nucleotides`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/disambiguate-nucleotides`
- **Reference:** See [references/help.md](references/help.md)

## When To Use This Tool

- Expand ambiguous IUPAC nucleotide patterns into all concrete DNA strings.
- Enumerate primer or motif variants before downstream searching or filtering.
- Normalize lowercase input to uppercase expanded output in shell pipelines.
- Use as a lightweight stdin filter inside EDirect-style text workflows.

## Common Patterns

```bash
# 1) Expand a single ambiguous motif
echo RCCGGY | disambiguate-nucleotides
```

```bash
# 2) Expand one pattern per line from a file
cat motifs.txt | disambiguate-nucleotides
```

```bash
# 3) Feed expanded sequences into a downstream search
echo ATNG | disambiguate-nucleotides | grep '^AT'
```

## Recommended Workflow

1. Supply one ambiguous nucleotide pattern per input line on stdin.
2. Expand the patterns, then inspect the output size before feeding it into downstream tools.
3. Pipe the concrete sequences into the next filter, matcher, or accession workflow.
4. Keep the original ambiguous query as provenance if the expansion space becomes large.

## Guardrails

- This tool is a stdin/stdout filter and prints nothing until input arrives.
- There is no built-in `-h`, `--help`, or `--version` interface; even `-h` is treated as ordinary input text.
- Ambiguity codes such as `N`, `B`, `D`, `H`, and `V` can expand combinatorially, so output size can explode quickly.
- Output is uppercased, sorted, and deduplicated.

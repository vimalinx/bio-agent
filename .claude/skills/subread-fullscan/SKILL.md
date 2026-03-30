---
name: subread-fullscan
description: Use when scanning a reference index for all high-similarity genomic locations of one specific read sequence string.
disable-model-invocation: true
user-invocable: true
---

# subread-fullscan

## Quick Start

- **Command:** `subread-fullscan [options] -i <index_name> <read_string>`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/subread-fullscan`
- **Reference:** See `references/help.md`; local no-argument execution is the most useful way to see usage text

## When To Use This Tool

- Use `subread-fullscan` when you want to probe where one literal read sequence could map across the whole indexed genome.
- It is a diagnostic or exploratory tool, not a bulk FASTQ aligner.
- Reach for it when validating whether a short sequence is repetitive, checking match specificity at a chosen identity threshold, or debugging why a read behaves oddly in the main aligner.

## Common Patterns

```bash
# Scan the genome for all high-similarity hits to one read sequence
subread-fullscan -i ref_index ACGTACGTACGTACGT
```

```bash
# Tighten the minimum matched fraction
subread-fullscan -i ref_index -m 0.95 ACGTACGTACGTACGT
```

## Recommended Workflow

1. Make sure the relevant Subread index already exists and note its basename.
2. Provide the query as a literal read string, not a FASTQ filename.
3. Start with the default match threshold, then increase `-m` if too many repetitive hits are returned.
4. Use the result as a debugging or interpretive aid before changing cohort-wide alignment settings.

## Guardrails

- The final argument is a literal read sequence string. This command does not take a FASTQ or FASTA file as input.
- `-i` expects the index basename, not the reference FASTA.
- Local testing shows that running with no arguments prints useful usage text, while `--help` and `--version` are not real help paths.
- `-m` is a fraction of matched bases, not a count.

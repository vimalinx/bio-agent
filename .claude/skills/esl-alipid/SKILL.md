---
name: esl-alipid
description: Use when calculating pairwise percent identities from multiple sequence alignments in FASTA or Stockholm format.
disable-model-invocation: true
user-invocable: true
---

# esl-alipid

## Quick Start

- **Command:** `esl-alipid [options] <alignment_file>`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/esl-alipid`
- **Full reference:** See [references/help.md](references/help.md) for complete options and usage

## When To Use This Tool

- Use `esl-alipid` when you need pairwise percent-identity measurements across all sequence pairs in an alignment.
- It is useful for diagnosing redundancy, alignment diversity, and whether an MSA should be clustered, filtered, or split before downstream modeling.
- Use it on aligned sequence files, not raw unaligned FASTA collections.
- In this environment the binary is currently blocked by the missing `libopenblas.so.0`, so treat the syntax below as documented behavior pending library repair.

## Common Patterns

```bash
# Compute pairwise percent identities for an alignment
esl-alipid alignment.sto

# Suppress the header in machine-oriented output
esl-alipid --noheader alignment.sto

# Force alphabet interpretation if guessing is ambiguous
esl-alipid --amino alignment.sto
esl-alipid --dna alignment.sto
```

## Recommended Workflow

1. Prepare a multiple sequence alignment file (FASTA or Stockholm format)
2. Run `esl-alipid <alignment_file>` to compute pairwise PIDs
3. Review output to assess sequence diversity or redundancy
4. Use results to guide filtering, clustering, or downstream analysis decisions

## Guardrails

- Ensure input file is a valid multiple sequence alignment (not unaligned sequences)
- Verify library dependencies are available (requires libopenblas)
- Check that all sequences in the alignment use the same alphabet
- If automatic alphabet detection fails, force the correct alphabet with `--amino`, `--dna`, or `--rna`

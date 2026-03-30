---
name: rnalalifold
description: Use when predicting locally stable secondary structures from multiple sequence alignments of RNA
disable-model-invocation: true
user-invocable: true
---

# rnalalifold

## Quick Start

- **Command**: `RNALalifold [options] <file1.aln>`
- **Local executable**: `/home/vimalinx/miniforge3/envs/bio/bin/RNALalifold`
- **Full reference**: See [references/help.md](references/help.md) for complete options and details

## When To Use This Tool

- Scan an RNA multiple sequence alignment for locally stable consensus structures.
- Find short structured elements inside long aligned regions instead of folding whole transcripts globally.
- Tune the maximum base-pair span for locality-sensitive searches.
- Export hit-specific alignments or CSV summaries for downstream review.

## Common Patterns

```bash
# 1) Scan an alignment for local consensus structures
RNALalifold family.aln
```

```bash
# 2) Tighten the local window size
RNALalifold -L 100 family.aln
```

```bash
# 3) Emit CSV plus per-hit alignment outputs
RNALalifold --csv --aln hits family.aln > local_hits.txt
```

## Recommended Workflow

1. Prepare input as a multiple sequence alignment file (MSA) in supported format
2. Set maximum base pair span with `-L` if different from default 70
3. Run `RNALalifold` with appropriate options (e.g., `--threshold`, `--csv`, `--aln` for output)
4. Review output consensus structures and energy values per hit

## Guardrails

- Input must be an aligned RNA sequence file (MSA); verify format matches `-f` option if specified
- Memory usage scales as O(n+L*L) and CPU time as O(n*L*L) where L is maxBPspan
- Default threshold of -0.1 kcal/mol per nucleotide filters weak structure hits; adjust with `--threshold` if needed

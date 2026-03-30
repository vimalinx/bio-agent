---
name: clustalw
description: Use when performing multiple sequence alignments on protein or nucleotide sequences, generating phylogenetic trees, or producing alignment output in various formats.
disable-model-invocation: true
user-invocable: true
---

# clustalw

## Quick Start
- **Command:** `clustalw -infile=seqs.fa -align`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/clustalw`
- **Full reference:** See `references/help.md`

## When To Use This Tool

- Build multiple sequence alignments for protein or nucleotide sequences.
- Generate CLUSTAL-style guide trees or distance trees as part of alignment workflows.
- Convert between alignment output formats such as CLUSTAL, FASTA, PHYLIP, NEXUS, and GCG.
- Merge alignments or add sequences with profile-alignment workflows.

## Common Patterns

```bash
# 1) Align FASTA sequences and write a CLUSTAL alignment
clustalw \
  -infile=seqs.fa \
  -align \
  -outfile=seqs.aln \
  -output=clustal
```

```bash
# 2) Align DNA sequences and write a PHYLIP tree
clustalw \
  -infile=markers.fa \
  -type=dna \
  -align \
  -tree \
  -outputtree=phylip
```

```bash
# 3) Merge two existing alignments by profile alignment
clustalw \
  -profile \
  -profile1=alignment1.aln \
  -profile2=alignment2.aln \
  -outfile=merged.aln
```

## Recommended Workflow

1. Decide whether you are doing a fresh alignment, tree generation from an existing alignment, or profile alignment between two existing alignments.
2. Set `-type=protein` or `-type=dna` explicitly when auto-detection would be ambiguous.
3. Run the alignment and inspect the emitted alignment file plus any guide-tree outputs such as `.dnd`.
4. If the downstream goal is rigorous phylogenetic inference, treat the CLUSTAL tree as a quick guide and move to a dedicated tree-inference tool afterward.

## Guardrails

- `clustalw` expects its classic long-option style such as `-infile=...`; bare GNU-style `--help`, `--version`, and `-h` are not valid help invocations.
- Use `-help`, `-fullhelp`, or `-options` to inspect available parameters.
- Do not run `clustalw` with no arguments in automation; it can drop into its legacy interactive behavior instead of doing useful batch work.
- The tree output is primarily a guide/distance tree, not a substitute for model-based maximum-likelihood phylogeny.

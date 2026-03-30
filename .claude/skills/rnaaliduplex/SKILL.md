---
name: rnaaliduplex
description: Use when predicting conserved RNA-RNA interactions between two CLUSTAL alignments to identify evolutionary conserved binding sites, hybridization energies, and duplex structures.
disable-model-invocation: true
user-invocable: true
---

# rnaaliduplex

## Quick Start

- **Command**: `RNAaliduplex [options] <file1.aln> <file2.aln>`
- **Local executable**: `/home/vimalinx/miniforge3/envs/bio/bin/RNAaliduplex`
- **Full reference**: See `references/help.md` for complete options and details

## When To Use This Tool

- Predict conserved RNA-RNA interactions between two homologous alignments.
- Score duplexes while preserving evolutionary signal across matched sequence sets.
- Search for optimal and suboptimal binding sites between a probe alignment and a target alignment.
- Keep analysis focused on inter-molecular pairing only.

## Common Patterns

```bash
# 1) Predict the best conserved interaction between two alignments
RNAaliduplex probe.aln target.aln
```

```bash
# 2) Report suboptimal interactions within an energy band
RNAaliduplex -e 5 probe.aln target.aln
```

```bash
# 3) Sort reported interactions by energy
RNAaliduplex -e 10 -s probe.aln target.aln > duplexes.txt
```

## Recommended Workflow

1. Prepare two CLUSTAL format alignment files with equal numbers of sequences in matching order
2. Run `RNAaliduplex <file1.aln> <file2.aln>` to compute conserved duplex structures
3. Use `-e <range>` to explore suboptimal structures within an energy range of the optimum (kcal/mol)
4. Parse stdout output containing dot-bracket structures with "&" separator, position ranges, and energies in kcal/mol

## Guardrails

- Both input alignments must have equal numbers of sequences in identical order (1st sequence in file1 pairs with 1st in file2)
- Only inter-molecular base pairs are calculated; for general folding use RNAcofold
- Output is written to stdout; redirect to file to capture results

---
name: rnaconsensus
description: Use when predicting RNA secondary structures for single sequences using information from multiple sequence alignments of homologous sequences.
disable-model-invocation: true
user-invocable: true
---

# rnaconsensus

## Quick Start

- **Command:** `RNAconsensus [-a filename] [-o OUTPUT] [--turn TURN] {hardcons,softcons} ...`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/RNAconsensus`
- **Full reference:** See `references/help.md` for complete options and details

## When To Use This Tool

- Predict single-sequence structures using consensus information from a homologous alignment.
- Map an RNAalifold consensus structure onto each sequence with hard constraints.
- Drive `RNAfold -C`-style per-sequence predictions from an alignment-derived consensus.
- Use the softer probabilistic strategy when hard constraints are too brittle.

## Common Patterns

```bash
# 1) Produce hard constraints from an alignment plus RNAalifold output
RNAconsensus -a family.aln hardcons family.alifold > constraints.txt
```

```bash
# 2) Derive hard constraints from an RNAalifold dot plot
RNAconsensus -a family.aln hardcons -d alidot.ps -t 0.95 > constraints.txt
```

```bash
# 3) Run the soft-constraint strategy directly
RNAconsensus -a family.aln -o softcons.txt softcons
```

## Recommended Workflow

1. Prepare a multiple sequence alignment file of homologous sequences
2. Choose a prediction strategy: `hardcons` (legacy refold.pl mode) or `softcons` (RNAsoftcons mode)
3. Run `RNAconsensus -a <alignment_file> -o <output> <strategy>`
4. Review output secondary structure predictions

## Guardrails

- Requires a multiple sequence alignment file via `-a` flag
- Must specify either `hardcons` or `softcons` strategy
- Use `--turn` to set minimum hairpin length if needed
- `--version` is not implemented in this argparse wrapper even though `--help` works

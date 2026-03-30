---
name: esl-ssdraw
description: Use when converting a Stockholm RNA or DNA alignment plus a PostScript structure template into colored secondary-structure diagrams.
disable-model-invocation: true
user-invocable: true
---

# esl-ssdraw

## Quick Start

- **Command:** `esl-ssdraw [options] <msafile> <SS postscript template> <output postscript file name>`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/esl-ssdraw`
- **Full reference:** See `references/help.md`

## When To Use This Tool

- Use `esl-ssdraw` when you need PostScript secondary-structure figures colored by alignment statistics, posterior probabilities, masks, or individual aligned sequences.
- It is designed for Stockholm RNA/DNA alignments that already carry RF annotation and a separate PostScript template describing the consensus structure layout.
- Reach for summary-diagram options such as `--cons`, `--info`, `--mutinfo`, `--prob`, or `--rf` when building alignment-level figures.
- Use `--indi` when you want one or more per-sequence diagrams instead of alignment-summary pages.

## Common Patterns

```bash
# Draw the default summary page set
esl-ssdraw alignment.sto template.ps summary.ps

# Restrict output to selected alignment-summary diagrams
esl-ssdraw --cons --info --prob alignment.sto template.ps stats.ps

# Draw individual-sequence pages
esl-ssdraw --indi alignment.sto template.ps individuals.ps

# Mark masked RF positions and also export tabular per-position values
esl-ssdraw --mask rf.mask --tabfile per-position.tsv alignment.sto template.ps masked.ps
```

## Recommended Workflow

1. Prepare a Stockholm alignment with `#=GC RF` annotation; include `#=GR PP` or individual sequence information only if you need those overlays.
2. Make sure the PostScript template matches the RF length of the first alignment in the file.
3. Start with the default output or choose specific pages explicitly.
4. Add `--tabfile` if you want the numeric per-position statistics alongside the PostScript figure.
5. Review the generated `.ps` file with a PostScript viewer or convert it downstream as needed.

## Guardrails

- Only the first alignment in `msafile` is drawn.
- Input must be Stockholm with RF annotation and RNA or DNA sequences.
- Summary-diagram options are incompatible with `--indi`.
- `--small` requires one-line-per-sequence Pfam-style alignment formatting.
- The generated PostScript output is not itself a reusable template for future `esl-ssdraw` runs.
- `-h` works; `--help` and `--version` are rejected by the local executable.

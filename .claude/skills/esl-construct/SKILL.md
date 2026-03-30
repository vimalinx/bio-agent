---
name: esl-construct
description: Use when inspecting, comparing, or rebuilding consensus RNA/DNA secondary-structure annotation in Stockholm alignments.
disable-model-invocation: true
user-invocable: true
---

# esl-construct

## Quick Start

- **Command:** `esl-construct [options] <msafile>`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/esl-construct`
- **Full reference:** See `references/help.md` for `--help` failure behavior and `esl-construct -h` output

## When To Use This Tool

- Use `esl-construct` when a Stockholm RNA/DNA alignment already contains individual structure annotation (`#=GR SS`), consensus structure annotation (`#=GC SS_cons`), or both, and you need to inspect how they agree or conflict.
- Use it to summarize which sequences carry structures and how many basepairs overlap with or conflict against `SS_cons`.
- Reach for structure-definition modes when you need to derive a replacement consensus structure from individual annotations: `-x`, `-r`, `-c`, `--indi`, `--ffreq`, or `--fmin`.
- Use `-l` and `--lmax` when you want a separate list of sequences that conflict with the current consensus structure.

## Common Patterns

```bash
# Summarize existing structure annotation and conflicts
esl-construct alignment.sto

# Verbosely list conflicting individual basepairs
esl-construct -v alignment.sto

# Build a maximal non-conflicting consensus structure
esl-construct -x -o consensus.sto alignment.sto

# Use one named sequence's structure as the new consensus and RF annotation
esl-construct --indi seq42 --rfindi -o from-seq.sto alignment.sto

# Remove consensus basepairs that conflict with any individual structure
esl-construct -r -o pruned.sto alignment.sto
```

## Recommended Workflow

1. Confirm the input alignment is Stockholm format, contains RNA or DNA sequences, and carries WUSS-compatible structure annotation.
2. Run the default mode or add `-v` to inspect how individual structures compare to any existing `SS_cons`.
3. Choose a consensus-definition strategy only after checking the conflict profile.
4. When rebuilding `SS_cons`, add `-o <file>` and optionally `--pfam` if you want non-interleaved Pfam-style Stockholm output.
5. Review the new `SS_cons` and any updated `RF` annotation before using the alignment downstream.

## Guardrails

- Input must be Stockholm format and contain RNA or DNA, not protein sequences.
- `-h` works; `--help` and `--version` are rejected by the local executable.
- Any of `-x`, `-r`, `-c`, `--indi`, `--ffreq`, or `--fmin` requires `-o`.
- `--rfc` only applies with `-c`, and `--rfindi` only applies with `--indi`.
- Vienna dot-parentheses are accepted, but the tool interprets structure annotation in WUSS terms; malformed structure tags will break the workflow.

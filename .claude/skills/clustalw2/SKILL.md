---
name: clustalw2
description: Use when running legacy ClustalW 2.1 multiple-sequence-alignment workflows, guide-tree calculations, or interactive alignment sessions from the command line.
disable-model-invocation: true
user-invocable: true
---

# clustalw2

## Quick Start

- **Command:** `clustalw2 -INFILE=seqs.fa -ALIGN`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/clustalw2`
- **Help entry points:** `clustalw2 -HELP`, `clustalw2 -CHECK`, `clustalw2 -FULLHELP`

## When To Use This Tool

- Run ClustalW 2.1 multiple sequence alignments from a legacy workflow.
- Build guide trees or percent-identity matrices with ClustalW's own CLI.
- Convert sequence files between supported alignment/output formats.
- Enter the older interactive terminal menu when you explicitly want that interface.

## Common Patterns

```bash
# 1) Show the concise command reference
clustalw2 -HELP
```

```bash
# 2) Run a standard multiple alignment
clustalw2 -INFILE=seqs.fa -ALIGN
```

```bash
# 3) Calculate a tree from an existing alignment
clustalw2 -INFILE=aligned.aln -TREE
```

## Recommended Workflow

1. Prefer noninteractive flags such as `-INFILE=...` and `-ALIGN` for reproducible runs.
2. Use `-HELP` or `-FULLHELP` to review the older option syntax before launching a large job.
3. Set output-related flags deliberately if you do not want the default CLUSTAL alignment output.
4. Use the interactive mode only when you actually want menu-driven operation.

## Guardrails

- `-h` and `--help` are not valid help flags here; they produce unknown-option errors.
- A bare `clustalw2` invocation enters the interactive menu and waits for choices.
- This CLI uses legacy uppercase single-dash options such as `-INFILE=...`, `-ALIGN`, `-TREE`, `-OUTPUT=...`.
- Default output format is CLUSTAL unless you override it with `-OUTPUT=`.
- The local build reports itself as `CLUSTAL 2.1`.

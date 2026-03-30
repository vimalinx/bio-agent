---
name: hmmfetch
description: Use when you need to extract specific HMM profiles from an HMM database file by name, or index an HMM file for faster lookups.
disable-model-invocation: true
user-invocable: true
---

# hmmfetch

## Quick Start
- **Command:** `hmmfetch [options] <hmmfile> <key>`
- **Local executable**: `/home/vimalinx/miniforge3/envs/bio/bin/hmmfetch`
- **Version:** HMMER 3.4 / Easel 0.49
- **Full reference:** See `references/help.md`

## When To Use This Tool

- Extract one named model from a combined HMM library.
- Pull many models from a large collection using a key list.
- Create an `.ssi` index once so repeated model lookups are fast.
- Split a large HMM set into smaller, task-specific subsets before scanning or searching.

## Common Patterns

```bash
# 1) Index an HMM library once for fast retrieval
hmmfetch --index Pfam-A.hmm
```

```bash
# 2) Fetch a single HMM by name or accession
hmmfetch Pfam-A.hmm PF00069 > PF00069.hmm
```

```bash
# 3) Fetch many models from a key list
hmmfetch \
  -f \
  Pfam-A.hmm \
  ids.txt \
  > subset.hmm
```

## Recommended Workflow

1. Index the source HMM file first if you expect repeated extractions.
2. Use exact model identifiers from the library header lines.
3. Fetch one model by key or many with `-f` and a plain-text key file.
4. Save the subset immediately and use it for downstream `hmmpress`, `hmmscan`, or curation.

## Guardrails

- `--index` creates a sidecar `<hmmfile>.ssi` file.
- `-f` changes the meaning of the second positional argument from a single key to a keyfile.
- `-O` writes to a file named after the requested key, which is convenient but easy to scatter across the current directory.
- Use `-h` for help; `--help` and `--version` are not valid here.

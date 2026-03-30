---
name: blst2tkns
description: Use when turning EDirect-style BLAST XML alignment blocks into a token stream for downstream shell or xtract-based parsing.
disable-model-invocation: true
user-invocable: true
---

# blst2tkns

EDirect shell wrapper over `xtract` that reads `Seq-align-set_E` XML and emits a compact label/value token stream for exon-alignment records.

## Quick Start

- **Command:** `blst2tkns`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/blst2tkns`
- **Environment prerequisite:** add `/home/vimalinx/miniforge3/envs/bio/bin` to `PATH` so sibling tools such as `xtract` are resolvable

## When To Use This Tool

- Convert `Seq-align-set_E` XML into a lighter token stream for shell pipelines.
- Pull out per-alignment values such as running index, score, start, stop, strand, and nested `parts/*` content.
- Bridge BLAST-derived XML that already lives in an EDirect / `xtract` workflow into simpler downstream parsing.
- Use this only for the expected XML shape; it is not a generic BLAST tabular, plain-text, or FASTA converter.

## Common Patterns

```bash
# 1) Tokenize an existing Seq-align-set_E XML file
export PATH=/home/vimalinx/miniforge3/envs/bio/bin:$PATH

blst2tkns < seq-align-set.xml > align.tokens.txt
```

```bash
# 2) Inspect the first emitted tokens before scaling up
export PATH=/home/vimalinx/miniforge3/envs/bio/bin:$PATH

blst2tkns < seq-align-set.xml | sed -n '1,30p'
```

## Recommended Workflow

1. Confirm the upstream XML actually contains `Seq-align-set_E` records before blaming the wrapper for empty output.
2. Activate the bio environment or prepend `/home/vimalinx/miniforge3/envs/bio/bin` to `PATH` so `xtract` is available.
3. Run the wrapper on a small sample and inspect the emitted labels before wiring it into a larger pipeline.
4. Feed the token stream to your next shell / EDirect stage once the field order matches what you expect.

## Guardrails

- The script is just a one-line `xtract` recipe. Without the bio bin directory on `PATH`, it fails immediately with `xtract: command not found`.
- There is no standalone help path here. With dependencies available, `blst2tkns -help` still falls through to `xtract` and errors on missing input.
- With `xtract` available but no XML input, the live failure is `No data supplied to xtract from stdin or file`.
- Source inspection shows it hard-codes emission of `index`, `score`, `start`, `stop`, `strand`, nested `parts/*` tokens, and a terminating `end 0` marker. If your XML schema differs, output may be partial or empty.

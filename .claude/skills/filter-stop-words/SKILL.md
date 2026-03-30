---
name: filter-stop-words
description: Use when processing text or queries in Entrez workflows to remove common stop words from input streams
disable-model-invocation: true
user-invocable: true
---

# filter-stop-words

## Quick Start

- **Command**: `tokenize | filter-stop-words`
- **Local executable**: `/home/vimalinx/miniforge3/envs/bio/bin/filter-stop-words`
- **Full reference**: See [references/help.md](references/help.md)

## When To Use This Tool

- Remove common stop words from a one-token-per-line text stream.
- Clean tokenized search/query text before downstream term processing.
- Replace removed stop words with `+` markers when you need placeholder positions in the stream.

## Common Patterns

```bash
# 1) Remove stop words from a token stream
printf 'the\ngene\nand\nmarker\n' | filter-stop-words
```

```bash
# 2) Replace removed stop words with plus signs
printf 'the\ngene\nand\nmarker\n' | filter-stop-words -plus
```

## Recommended Workflow

1. Tokenize the text so each candidate word is on its own line.
2. Pipe that stream into `filter-stop-words`.
3. Decide whether you want removed words dropped entirely or replaced with `+` via `-plus`.
4. Feed the cleaned token stream into the next text-processing stage.

## Guardrails

- Filtering is line-oriented. If you feed full phrases instead of one token per line, the stop-word list will not behave as expected.
- The wrapper has no real `--help` / `--version` interface.
- The first command-line token is always consumed by the script; normal use should stick to no argument or `-plus`.
- In default mode removed stop words disappear completely, which can change query semantics if positional placeholders matter.

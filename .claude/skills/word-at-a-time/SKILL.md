---
name: word-at-a-time
description: Use when tokenizing free text into lowercase one-word-per-line output by stripping non-alphanumeric separators.
disable-model-invocation: true
user-invocable: true
---

# word-at-a-time

Tiny shell tokenizer. It replaces non-alphanumeric characters with spaces, trims leading spaces, lowercases the stream, and then emits one token per line with `fmt -w 1`.

## Quick Start

- **Command:** `... | word-at-a-time`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/word-at-a-time`
- **Implementation core:** `sed | tr | fmt -w 1`

## When To Use This Tool

- Breaking free text into one lowercase token per line
- Normalizing titles, abstracts, or labels before stop-word filtering or counting
- Feeding text into downstream line-oriented word tools such as `filter-stop-words` or `sort-uniq-count`
- Reusing a fixed tokenizer instead of rewriting the same `sed | tr | fmt` pipeline

## Common Patterns

```bash
# Tokenize a text snippet
printf 'DNA-repair, 2024!\nSecond_line\n' | word-at-a-time
```

```bash
# Count normalized word frequencies
cat article.txt | word-at-a-time | sort-uniq-count-rank
```

```bash
# Filter stop words after tokenization
cat article.txt | word-at-a-time | filter-stop-words
```

## Recommended Workflow

1. Feed plain text through stdin.
2. Tokenize with `word-at-a-time`.
3. Chain immediately into downstream filters or counters if you need analysis rather than raw tokens.
4. Preserve the raw source elsewhere if punctuation or case matters, because this tool destroys both.

## Guardrails

- There is no real `-h`, `--help`, or `--version` interface; passing flags without stdin yields no useful metadata.
- The tokenizer strips punctuation and underscores by replacing every non-alphanumeric character with a space.
- Output is always lowercased.
- In local testing, `printf 'DNA-repair, 2024!\nSecond_line\n' | word-at-a-time` emitted `dna`, `repair`, `2024`, `second`, `line`.

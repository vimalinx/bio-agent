---
name: pair-at-a-time
description: Use when turning a plain-text stream into adjacent lowercase word pairs for EDirect-style text mining, token-neighbor extraction, or lightweight bigram generation.
disable-model-invocation: true
user-invocable: true
---

# pair-at-a-time

## Quick Start

- **Command:** `pair-at-a-time`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/pair-at-a-time`
- **I/O shape:** reads plain text on stdin and writes adjacent token pairs on stdout

## When To Use This Tool

- Convert free text into adjacent word pairs for simple co-occurrence or neighbor analysis.
- Normalize punctuation and case before downstream counting, filtering, or sorting.
- Chain after XML / text extraction steps in lightweight EDirect shell pipelines.
- Keep using shell text tools instead of pulling text into Python just to make bigrams.
- Not for paired-end sequencing reads; this is a text-stream wrapper, not a genomics read-pair utility.

## Common Patterns

```bash
# 1) Adjacent pairs from a sentence
printf 'Alpha beta gamma\n' | pair-at-a-time
```

```bash
# 2) Punctuation is stripped and tokens are lowercased
printf 'BRCA1, TP53; EGFR\n' | pair-at-a-time
```

```bash
# 3) Downstream counting of repeated neighboring pairs
xtract -pattern DocumentSummary -element Title |
pair-at-a-time |
sort | uniq -c | sort -nr
```

## Recommended Workflow

1. Feed the tool plain text on stdin, usually after `xtract`, `sed`, `tr`, or another shell extractor.
2. Assume punctuation will be discarded and alphabetic text lowercased before pairing.
3. Capture stdout directly into `sort`, `uniq -c`, or other downstream shell filters.
4. If record boundaries matter, split and process each record separately before calling this wrapper.

## Guardrails

- There is no real option parsing: `-h` or `--help` produce no useful built-in help text.
- The script depends on the companion helper `word-at-a-time` being on `PATH`; invoking `pair-at-a-time` by absolute path alone can still fail with `word-at-a-time: command not found`.
- Non-alphanumeric characters are converted to spaces and all alphabetic characters are lowercased.
- Consecutive duplicate tokens are collapsed by `uniq` before pairing, so `foo foo bar` becomes `foo bar`.
- Original line / record boundaries are not preserved; the wrapper effectively pairs across the flattened token stream.

---
name: gm2ranges
description: Use when converting BLAST/genomic-map alignment summaries into compact strand-and-range tables for later interval fusion.
disable-model-invocation: true
user-invocable: true
---

# gm2ranges

## Quick Start

- **Command:** `printf 'acc1 score 1|10 5|3 plus|minus\n' | /home/vimalinx/miniforge3/envs/bio/bin/gm2ranges`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/gm2ranges`
- **Full reference:** See [references/help.md](references/help.md) for complete usage details

## When To Use This Tool

- Turn pipe-delimited start/span/strand alignment summaries into comma-joined genomic ranges.
- Prepare interval strings for downstream helpers such as `fuse-ranges`.
- Collapse per-hit dense segment fields into one summarized row with a segment count and an overall strand label.

## Common Patterns

```bash
# 1) Convert one row of starts/spans/strands into a compact range summary
printf 'acc1 score 1|10 5|3 plus|minus\n' | \
  /home/vimalinx/miniforge3/envs/bio/bin/gm2ranges
```

```bash
# 2) Use in the intended EDirect map pipeline
cat smear.asn | \
  blst2gm | \
  /home/vimalinx/miniforge3/envs/bio/bin/gm2ranges | \
  grep minus | \
  cut -f 2-
```

## Recommended Workflow

1. Start from rows that already contain accession, score, start-list, span-list, and strand-list columns.
2. Run `gm2ranges` as a stdin-to-stdout transformer.
3. Inspect the emitted segment count, aggregate strand label, and comma-joined range list.
4. Feed the range list into downstream normalization or fusion steps if you need canonical interval coordinates.

## Guardrails

- The wrapper expects at least five whitespace-delimited columns; shorter rows are silently skipped.
- Minus-strand segments are emitted as descending `stop..start` strings (for example `12..10`), so further normalization is usually needed.
- The aggregate strand label becomes `mixed` when both plus and minus segments appear in the same row.
- There is no built-in help or version mode.

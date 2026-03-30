---
name: accn-at-a-time
description: Use when splitting mixed accession-like text into one lowercase token per line in EDirect-style text pipelines.
disable-model-invocation: true
user-invocable: true
---

# accn-at-a-time

## Quick Start

- **Command:** `printf 'NM_001, XP_002 foo-bar\n' | /home/vimalinx/miniforge3/envs/bio/bin/accn-at-a-time`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/accn-at-a-time`
- **Full reference:** See [references/help.md](references/help.md) for complete usage details

## When To Use This Tool

- Break mixed text into one token per line before batching or lookup.
- Normalize accession-like identifiers to lowercase while preserving letters, digits, underscores, and dots.
- Clean up free-form text blobs before feeding them into downstream EDirect helpers.

## Common Patterns

```bash
# 1) Split a mixed line of identifiers into one token per line
printf 'NM_001, XP_002 foo-bar\n' | \
  /home/vimalinx/miniforge3/envs/bio/bin/accn-at-a-time
```

```text
nm_001
xp_002
foo
bar
```

```bash
# 2) Normalize, deduplicate, and sort tokens before later batching
cat messy_ids.txt | \
  /home/vimalinx/miniforge3/envs/bio/bin/accn-at-a-time | \
  sort -u
```

## Recommended Workflow

1. Feed the raw text stream on stdin.
2. Inspect a few emitted tokens to confirm the split points match what you meant.
3. Deduplicate or validate the resulting identifiers separately if your downstream step needs stricter accession semantics.
4. Batch the cleaned list with tools such as `join-into-groups-of` only after checking the normalization step.

## Guardrails

- This is just a text normalizer: it does not validate that the emitted tokens are real accessions.
- Output is always lowercased.
- Any character outside `[A-Za-z0-9_.]` becomes a split point, so hyphens and slashes will break tokens apart.
- The script has no built-in help or version mode.

---
name: just-top-hits
description: Use when keeping only the first N query groups from a first-column-grouped tabular hit table.
disable-model-invocation: true
user-invocable: true
---

# just-top-hits

## Quick Start

- **Command**: `cat hits.tsv | /home/vimalinx/miniforge3/envs/bio/bin/just-top-hits 2`
- **Local executable**: `/home/vimalinx/miniforge3/envs/bio/bin/just-top-hits`
- **Full reference**: See [references/help.md](references/help.md) for complete usage details

## When To Use This Tool

- Keep only the earliest query groups from a table already grouped by column 1.
- Trim a long hit table down to the first 1, 2, or N query blocks without re-ranking scores.
- Use as a cheap early-stop filter when the table is already ordered the way you want.

## Common Patterns

```bash
# 1) Keep only the first query group (default limit = 1)
cat hits.tsv | \
  /home/vimalinx/miniforge3/envs/bio/bin/just-top-hits
```

```bash
# 2) Keep the first two grouped query blocks
cat hits.tsv | \
  /home/vimalinx/miniforge3/envs/bio/bin/just-top-hits 2
```

## Recommended Workflow

1. Sort or group your hit table by the first column before using this tool.
2. Decide how many leading groups you want to preserve.
3. Pipe the grouped table through `just-top-hits`.
4. Verify that the retained groups are the ones you intended before downstream analysis.

## Guardrails

- This tool does not compute "top hits" by score. It simply keeps rows until the first-column key has changed N times.
- The limit counts first-column groups, not rows.
- All rows within each retained group are preserved.
- If the table is not already grouped in the desired order by column 1, the output will not match biological "best hit" expectations.

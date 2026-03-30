---
name: join-into-groups-of
description: Use when batching newline-separated IDs into fixed-size comma-separated groups for EDirect calls or other list-limited APIs.
disable-model-invocation: true
user-invocable: true
---

# join-into-groups-of

CLI tool from the entrez-direct bioconda package that groups input lines into batches of a specified size using xargs.

## Quick Start

- **Command:** `join-into-groups-of <group_size>`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/join-into-groups-of`
- **Reference:** See [references/help.md](references/help.md) for detailed usage

## When To Use This Tool

- Batch large ID lists into comma-separated chunks.
- Respect API or wrapper limits by controlling how many IDs appear in each emitted group.
- Prepare EDirect-friendly comma-joined ID batches from one-record-per-line input.

## Common Patterns

```bash
# 1) Group IDs into batches of 200
cat ids.txt | \
  /home/vimalinx/miniforge3/envs/bio/bin/join-into-groups-of 200
```

```bash
# 2) Use the default batch size (10000)
cat ids.txt | \
  /home/vimalinx/miniforge3/envs/bio/bin/join-into-groups-of
```

```text
a,b,c
```

## Recommended Workflow

1. Start from a newline-separated list with no embedded whitespace inside individual IDs.
2. Pick a group size that matches the downstream tool or API limit.
3. Pipe each emitted comma-joined line into the next query step.
4. Keep the final short batch; the tool does not pad or discard remainders.

## Guardrails

- With no positional argument, the default batch size is `10000`.
- Output groups are comma-separated, not space-separated.
- The implementation uses `xargs`, so embedded spaces or tabs inside records will be tokenized and destroyed.
- There is no dedicated help or version mode; unsupported flags are forwarded into the `xargs -n` code path rather than handled cleanly.

---
name: exclude-uid-lists
description: Use when subtracting one Entrez or NCBI UID file from another and keeping only IDs unique to the first file.
disable-model-invocation: true
user-invocable: true
---

# exclude-uid-lists

## Quick Start

- **Command**: `exclude-uid-lists <keep-list> <exclude-list>`
- **Local executable**: `/home/vimalinx/miniforge3/envs/bio/bin/exclude-uid-lists`
- **Full reference**: See `references/help.md` for detailed options and usage

## When To Use This Tool

- Remove already seen or unwanted IDs from a primary UID file.
- Keep only FILE1 entries that do not appear in FILE2.
- Filter out processed, withdrawn, or blacklisted identifiers before a downstream fetch.
- Use this instead of `difference-uid-lists` when direction matters.

## Common Patterns

```bash
# 1) Remove already processed UIDs from a fresh search result
exclude-uid-lists current.ids processed.ids > todo.ids
```

```bash
# 2) Drop a blacklist from a master UID list
exclude-uid-lists all_hits.ids blacklist.ids > filtered.ids
```

```bash
# 3) Count the remaining UIDs after subtraction
exclude-uid-lists source.ids remove.ids | wc -l
```

## Recommended Workflow

1. Put the source IDs in the first file and the IDs to remove in the second file.
2. Run `exclude-uid-lists` and redirect the output to a new keep-list.
3. Inspect the count or first few IDs before downstream fetching.
4. Feed the filtered list into `efetch`, `xtract`, or another local-archive step.

## Guardrails

- The real implementation is `comm -23 <(sort "$1") <(sort "$2") | sort -n`, so the result is directional: FILE1 minus FILE2.
- The wrapper sorts both inputs internally, so original ordering is lost.
- This command expects exactly two files and has no clean built-in help/version behavior.
- Passing `--help` or `--version` can still trigger `sort` / `comm` errors because the wrapper interprets them as file arguments.

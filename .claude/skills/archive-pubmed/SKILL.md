---
name: archive-pubmed
description: Use when maintaining a local PubMed XML archive for offline literature search, indexing, or bulk processing.
disable-model-invocation: true
user-invocable: true
---

# archive-pubmed

## Quick Start

- **Command**: `archive-pubmed [download|verify|missing|index]`
- **Local executable**: `/home/vimalinx/miniforge3/envs/bio/bin/archive-pubmed`
- **Full reference**: See [references/help.md](references/help.md) for detailed documentation

## When To Use This Tool

- Maintain a local PubMed XML archive for offline literature search, text mining, or batch analysis.
- Backfill missing baseline/update files after interrupted refreshes.
- Verify downloaded gzip packages before rebuilding the search/posting layers.
- Rebuild local PubMed postings after the archive content changes.

## Common Patterns

```bash
# 1) Download new PubMed files and populate the local archive
export EDIRECT_LOCAL_ARCHIVE=/data/edirect
archive-pubmed
```

```bash
# 2) Check which PubMed packages are missing locally
archive-pubmed -missing
```

```bash
# 3) Rebuild the local PubMed search/posting structures
archive-pubmed -index
```

## Recommended Workflow

1. Set `EDIRECT_LOCAL_ARCHIVE` and confirm the archive root is writable before starting.
2. Make sure the required helper commands for drive setup and versioned-record refresh are present.
3. Run `archive-pubmed` to download new files and populate the archive.
4. Use `-verify` or `-missing` if the refresh was interrupted or you suspect archive gaps.
5. Run `-index` only after the data files are stable, then inspect the timing summary before using the local archive with other EDirect tools.

## Guardrails

- `--help` and `--version` are not safe inspection switches; they still run archive setup and can emit real helper/env failures.
- The script requires `EDIRECT_LOCAL_ARCHIVE`, `pm-setup`, `pm-prepare`, and `pm-refresh`.
- `-clean`, `-scrub`, `-scour`, `-erase`, and `-zap` are destructive maintenance modes and must be run separately from `-index`.
- Mixed-year archive states can force a cleanup path before reindexing; the script explicitly tells you to `-zap` or `-scour` in some stale-data scenarios.
- `-stem` and `-strict` change how text is normalized and indexed, so record them in reproducible workflows.

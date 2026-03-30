---
name: archive-pids
description: Use when maintaining a local PubMed-to-PMCID postings archive for offline identifier crosswalks in EDirect workflows.
disable-model-invocation: true
user-invocable: true
---

# archive-pids

## Quick Start

- **Command:** `archive-pids [daily|-index]`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/archive-pids`
- **Full reference:** See [references/help.md](references/help.md) for complete documentation

## When To Use This Tool

- Build a local postings archive for the PubMed `PMCID` field.
- Support offline PMID-to-PMCID style lookups inside a populated local EDirect archive.
- Refresh the PMCID posting data after PubMed metadata updates.
- Keep this identifier crosswalk in the same archive layout used by the rest of the PubMed local-data tools.

## Common Patterns

```bash
# 1) Refresh the local PMCID postings archive
export EDIRECT_LOCAL_ARCHIVE=/data/edirect
archive-pids
```

```bash
# 2) Rebuild incremental index and invert layers after a refresh
archive-pids daily
```

```bash
# 3) Rebuild merged postings for downstream local queries
archive-pids -index
```

## Recommended Workflow

1. Set `EDIRECT_LOCAL_ARCHIVE` and verify the target archive tree is writable.
2. Confirm `pm-setup`, `pm-prepare`, and the local Go toolchain are available.
3. Run `archive-pids` to refresh the underlying PMCID data.
4. Follow with `daily` or `-index` as a separate maintenance command when you need refreshed postings.
5. Check the timing summary before assuming the archive is ready for local identifier lookups.

## Guardrails

- `--help` and `--version` are not safe here; they still execute archive setup and prerequisite checks.
- The script depends on `EDIRECT_LOCAL_ARCHIVE`, `pm-setup`, `pm-prepare`, and a working local `go` compiler.
- Cleaning and indexing must be separate commands.
- Cleanup aliases remove local scratch content, so treat them as destructive maintenance.
- This tool is for building the local PMCID postings archive, not for extracting a one-off ID list from stdin.

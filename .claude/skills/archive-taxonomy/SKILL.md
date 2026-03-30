---
name: archive-taxonomy
description: Use when maintaining a local NCBI Taxonomy archive for offline lineage and taxon lookups in EDirect workflows.
disable-model-invocation: true
user-invocable: true
---

# archive-taxonomy

## Quick Start

- **Command**: `archive-taxonomy [daily|-index]`
- **Local executable**: `/home/vimalinx/miniforge3/envs/bio/bin/archive-taxonomy`
- **Full reference**: See [references/help.md](references/help.md) for detailed usage

## When To Use This Tool

- Build a local NCBI Taxonomy archive for offline taxon, lineage, and rank lookups.
- Refresh taxonomy records after the upstream taxdump changes.
- Rebuild postings so local EDirect searches can query taxonomy fields without going back to NCBI.
- Use this when you want taxonomy data to live inside the same EDirect local-archive structure as other databases.

## Common Patterns

```bash
# 1) Refresh the local taxonomy archive
export EDIRECT_LOCAL_ARCHIVE=/data/edirect
archive-taxonomy
```

```bash
# 2) Rebuild only the incremental index and invert layers
archive-taxonomy daily
```

```bash
# 3) Rebuild the full local taxonomy postings set
archive-taxonomy -index
```

## Recommended Workflow

1. Set `EDIRECT_LOCAL_ARCHIVE` and confirm the archive root is writable.
2. Make sure the required EDirect helpers and local Go toolchain are available.
3. Run `archive-taxonomy` to download the taxdump and populate the local archive.
4. Follow with `daily` or `-index` as a separate command when you need refreshed search/posting layers.
5. Check the `DAT`, `DWN`, `POP`, `IDX`, `INV`, `COL`, `MRG`, and `PST` timing blocks before relying on the rebuilt archive.

## Guardrails

- `--help` and `--version` are not metadata-only; they still run real archive setup logic.
- The script depends on `EDIRECT_LOCAL_ARCHIVE`, `pm-setup`, `pm-prepare`, and a working local `go` compiler.
- Cleaning and indexing must be run as separate invocations.
- The cleanup ladder (`-clean`, `-scrub`, `-scour`, `-erase`, `-zap`) is destructive and removes progressively more of the local taxonomy archive.
- Default FTP mode may try Aspera-backed transfer; pick `-https` or `-ftp` explicitly if transport behavior matters.

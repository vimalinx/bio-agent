---
name: archive-nmcds
description: Use when building or refreshing a local RefSeq NM CDS archive for offline accession and coding-sequence lookups.
disable-model-invocation: true
user-invocable: true
---

# archive-nmcds

## Quick Start

- **Command:** `archive-nmcds [-index|-clean|-scrub|-scour|-erase|-zap]`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/archive-nmcds`
- **Full reference:** See `references/help.md` for complete documentation

## When To Use This Tool

- Build a local RefSeq NM mRNA/CDS archive for offline accession-driven sequence work.
- Generate the master accession list and CDS offset table that EDirect uses during local archive population.
- Refresh local RefSeq source records, then rebuild index and posting layers for offline lookups.
- Repair or reset broken archive state with the staged cleanup levels when a rebuild is required.

## Common Patterns

```bash
# 1) Download RefSeq mRNA files and rebuild the local archive content
export EDIRECT_LOCAL_ARCHIVE=/data/edirect
archive-nmcds
```

```bash
# 2) Force HTTPS transfer instead of the default FTP / Aspera path
archive-nmcds -https
```

```bash
# 3) Rebuild incremental index, invert, merge, and postings layers
archive-nmcds -index
```

## Recommended Workflow

1. Set `EDIRECT_LOCAL_ARCHIVE` and confirm the archive root is writable.
2. Ensure the supporting EDirect helper commands are present before starting a rebuild.
3. Run `archive-nmcds` to stage source files, generate accession/CDS tables, and populate the archive.
4. Use `-index` as a separate follow-up step when you need refreshed search/posting structures.
5. Reach for `-clean`, `-scrub`, `-scour`, `-erase`, or `-zap` only when you truly need to tear down stale layers before rebuilding.

## Guardrails

- `--help` and `--version` are not metadata switches here; they still walk through setup, download, and generation code paths.
- The script needs `EDIRECT_LOCAL_ARCHIVE`, `pm-setup`, and `pm-prepare` to be available.
- Cleanup levels are hierarchical and destructive: `-clean` removes incremental/index state, while `-zap` removes the source records and the remaining archive tree.
- Cleaning and indexing must be separate invocations.
- Archive generation creates accession and CDS-offset side tables, so allow time and disk space beyond the raw downloads.

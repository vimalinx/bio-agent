---
name: archive-pmc
description: Use when maintaining a local PubMed Central full-text archive for offline PMC search or bulk processing.
disable-model-invocation: true
user-invocable: true
---

# archive-pmc

## Quick Start

- **Command:** `archive-pmc [download|verify|missing|index]`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/archive-pmc`
- **Full reference:** See `references/help.md` for complete usage details

## When To Use This Tool

- Maintain a local PubMed Central full-text archive for offline article mining.
- Backfill missing PMC packages or verify an existing local archive after interrupted transfers.
- Rebuild local posting structures once the local PMC content is stable.
- Prefer this over ad hoc PMC file mirroring when you want the standard EDirect archive layout.

## Common Patterns

```bash
# 1) Download and populate the local PMC archive
export EDIRECT_LOCAL_ARCHIVE=/data/edirect
archive-pmc
```

```bash
# 2) Check for missing PMC packages after a failed or partial sync
archive-pmc -missing
```

```bash
# 3) Rebuild local search/posting structures
archive-pmc -index
```

## Recommended Workflow

1. Set `EDIRECT_LOCAL_ARCHIVE` and confirm the local archive root is writable.
2. Ensure the EDirect helper commands needed for drive setup are available.
3. Run `archive-pmc` to fetch and populate the local archive.
4. If a transfer was interrupted, use `-verify` or `-missing` before rebuilding postings.
5. Run `-index` only after the local content looks complete, then inspect the timing summary for `DAT`, `DWN`, `POP`, `IDX`, `INV`, `COL`, `MRG`, and `PST`.

## Guardrails

- `--help` and `--version` are not metadata-only; they still run archive setup and can emit missing-helper or missing-environment errors.
- The script requires `EDIRECT_LOCAL_ARCHIVE`, `pm-setup`, and `pm-prepare`.
- `download`, `verify`, `missing`, and `index` are distinct modes; use them deliberately instead of assuming a no-arg run will validate everything.
- The cleanup ladder (`-clean`, `-scrub`, `-scour`, `-erase`, `-zap`) is destructive and must be run separately from `-index`.
- `-stem` changes the generated text index content, so record it if you need reproducible local search behavior.

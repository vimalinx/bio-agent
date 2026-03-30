---
name: archive-nihocc
description: Use when maintaining a local NIH Open Citation Collection archive for offline citation-link lookups in EDirect workflows.
disable-model-invocation: true
user-invocable: true
---

# archive-nihocc

## Quick Start

- **Command**: `archive-nihocc [daily|-index]`
- **Local executable**: `/home/vimalinx/miniforge3/envs/bio/bin/archive-nihocc`
- **Full reference**: See [references/help.md](references/help.md) for detailed documentation

## When To Use This Tool

- Build a local NIH Open Citation Collection snapshot for offline PMID citation-link lookups.
- Refresh local `CITED` / `CITES` posting files after the upstream OCC bundle changes.
- Keep citation data in the standard EDirect archive layout instead of managing ad hoc zip downloads by hand.
- Rebuild index, invert, merge, and posting layers when downstream local search commands need updated citation edges.

## Common Patterns

```bash
# 1) Download or refresh the local OCC archive
export EDIRECT_LOCAL_ARCHIVE=/data/edirect
archive-nihocc
```

```bash
# 2) Incrementally rebuild index and invert layers after new data arrives
archive-nihocc daily
```

```bash
# 3) Rebuild the full local search/postings structures
archive-nihocc -index
```

## Recommended Workflow

1. Set `EDIRECT_LOCAL_ARCHIVE` and confirm the archive root is writable before invoking the script.
2. Make sure the supporting EDirect helpers and a local Go toolchain are available.
3. Run `archive-nihocc` to refresh the downloaded OCC bundle in the archive tree.
4. Follow with `daily` or `-index` as a separate command, depending on whether you need only incremental rebuilds or a full postings refresh.
5. Review the `DWN`, `IDX`, `INV`, `MRG`, and `PST` timing lines before trusting the local archive.

## Guardrails

- `--help` and `--version` are not metadata-only here; they still enter archive setup logic and fail if prerequisites are missing.
- The script requires `EDIRECT_LOCAL_ARCHIVE`, `pm-setup`, `pm-prepare`, and a working local `go` compiler.
- Cleaning and indexing are mutually exclusive in one invocation; run cleanup commands separately from `daily` / `-index`.
- The cleanup aliases (`clean`, `scrub`, `scour`, `scratch`, `erase`) remove local scratch material and should be treated as destructive maintenance.
- The OCC zip download is large and the script warns it can take hours; do not treat this like a lightweight helper command.

---
name: expand-current
description: Use when expanding and rebuilding the local EDirect PubMed `Current` archive plus its derived index layers.
disable-model-invocation: true
user-invocable: true
---

# expand-current

CLI tool for expanding and indexing current PubMed archive files for local EDirect operations.

## Quick Start

- **Command**: `EDIRECT_LOCAL_ARCHIVE=/path/to/local/archive PATH=/home/vimalinx/miniforge3/envs/bio/bin:$PATH /home/vimalinx/miniforge3/envs/bio/bin/expand-current`
- **Local executable**: `/home/vimalinx/miniforge3/envs/bio/bin/expand-current`
- **Full reference**: See [references/help.md](references/help.md) for complete documentation

## When To Use This Tool

- Refresh the local `Current` PubMed archive inside an EDirect local archive installation.
- Expand `*.xml.gz` current-archive files into indexed XML and rebuild derived merged / indexed / inverted layers.
- Maintain a local offline-style PubMed archive workflow after new archive content arrives.

## Common Patterns

```bash
# 1) Expand and rebuild the current local PubMed archive
EDIRECT_LOCAL_ARCHIVE=/data/edirect-archive \
PATH=/home/vimalinx/miniforge3/envs/bio/bin:$PATH \
  /home/vimalinx/miniforge3/envs/bio/bin/expand-current
```

```bash
# 2) Run inside a maintenance script after archive synchronization
export EDIRECT_LOCAL_ARCHIVE=/data/edirect-archive
export PATH=/home/vimalinx/miniforge3/envs/bio/bin:$PATH
/home/vimalinx/miniforge3/envs/bio/bin/expand-current
```

## Recommended Workflow

1. Confirm `EDIRECT_LOCAL_ARCHIVE` resolves to a real local archive tree before running anything.
2. Make sure companion commands such as `rchive`, `pm-collect`, and `xtract` are available.
3. Run `expand-current` during a maintenance window, because it deletes previous derived index files before rebuilding them.
4. Verify that fresh XML files and rebuilt index layers exist before pointing downstream local queries at the archive.

## Guardrails

- This is an operational maintenance script, not a safe metadata probe.
- It deletes prior `*.e2x*`, `*.inv*`, and `*.mrg*` files under the derived archive layers before rebuilding them.
- In the current environment, a missing `EDIRECT_LOCAL_ARCHIVE` or missing helpers such as `pm-collect` can still lead to noisy partial execution and a final `EXIT 0`, so pre-flight checks matter.
- Sufficient disk space is required because compressed current-archive XML is expanded into plain XML during the rebuild.

---
name: archive-nlmnlp
description: Use when maintaining a local NLM NLP concept archive over PubMed for offline chemical, disease, gene, or GeneRIF lookups.
disable-model-invocation: true
user-invocable: true
---

# archive-nlmnlp

## Quick Start

- **Command**: `archive-nlmnlp [daily|-index]`
- **Local executable**: `/home/vimalinx/miniforge3/envs/bio/bin/archive-nlmnlp`
- **Full reference**: See [references/help.md](references/help.md) for complete documentation

## When To Use This Tool

- Build a local PubMed concept archive backed by PubTator Central, GeneRIF, and gene metadata files.
- Support offline lookup of chemical, disease, gene, synonym, and GeneRIF-derived postings in EDirect workflows.
- Refresh the archive after upstream concept files change, then rebuild postings in the usual EDirect layout.
- Use this instead of stitching together the PubTator and GeneRIF files manually.

## Common Patterns

```bash
# 1) Refresh the local NLM NLP extras and archive over HTTPS
export EDIRECT_LOCAL_ARCHIVE=/data/edirect
archive-nlmnlp -https
```

```bash
# 2) Rebuild only the incremental index and invert layers
archive-nlmnlp daily
```

```bash
# 3) Rebuild merged postings for downstream local searching
archive-nlmnlp -index
```

## Recommended Workflow

1. Set `EDIRECT_LOCAL_ARCHIVE` and confirm the archive root exists and is writable.
2. Make sure `pm-setup`, `pm-prepare`, and the local Go toolchain are available.
3. Run `archive-nlmnlp` or `archive-nlmnlp -https` to stage the latest PubTator / GeneRIF support files.
4. Follow with `daily` or `-index` as a separate command when you need refreshed postings.
5. Check the `DWN`, `IDX`, `INV`, `MRG`, and `PST` timing blocks to confirm each stage actually ran.

## Guardrails

- `--help` and `--version` are not safe inspection switches; they still trigger archive setup and prerequisite checks.
- The script depends on `EDIRECT_LOCAL_ARCHIVE`, `pm-setup`, `pm-prepare`, and a local `go` compiler.
- Default transport may try the FTP / Aspera path; use `-https` or `-ftp` explicitly if you need predictable transfer behavior.
- Cleaning and indexing must be run separately.
- The cleanup aliases remove scratch data, so do not use them casually on a populated archive.

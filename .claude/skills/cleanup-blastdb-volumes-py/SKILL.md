---
name: cleanup-blastdb-volumes-py
description: Use when managing BLAST database storage by removing unnecessary volume files to reclaim disk space.
disable-model-invocation: true
user-invocable: true
---

# cleanup-blastdb-volumes-py

## Quick Start
- **Command:** `cleanup-blastdb-volumes.py -db <dbname> -dbtype <prot|nucl> [-dry-run]`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/cleanup-blastdb-volumes.py`
- **Full reference:** See `references/help.md`

## When To Use This Tool

- Remove orphaned BLAST database volumes after database updates or alias changes.
- Reclaim disk space when a `.pal` or `.nal` alias DB no longer references all volumes on disk.
- Audit what would be deleted first with `-dry-run`.
- Resolve clutter in BLAST DB directories found through `BLASTDB` or NCBI config lookup.

## Common Patterns

```bash
# 1) Preview cleanup for a protein alias database
cleanup-blastdb-volumes.py \
  -db nr \
  -dbtype prot \
  -dry-run
```

```bash
# 2) Remove extra nucleotide volumes after review
cleanup-blastdb-volumes.py \
  -db nt \
  -dbtype nucl
```

```bash
# 3) Verbose preview when the DB is discovered via BLASTDB
BLASTDB=/data/blastdb \
cleanup-blastdb-volumes.py \
  -db swissprot \
  -dbtype prot \
  -dry-run \
  -verbose
```

## Recommended Workflow

1. Confirm the target database is an alias-style BLAST DB with a `.pal` or `.nal` file.
2. Run `-dry-run` first and inspect the extra volumes listed from the alias file's `DBLIST`.
3. Re-run without `-dry-run` only after confirming the leftover volumes are genuinely stale.
4. Finish with `blastdbcheck` or a representative BLAST query if the database is business-critical.

## Guardrails

- This script cleans alias databases; if there is no `.pal` or `.nal` file, it exits without doing useful work.
- Database lookup is path-sensitive: it searches the current directory, `BLASTDB`, and `.ncbirc` / `ncbi.ini` configuration.
- Always use `-dry-run` first because the non-dry mode deletes files immediately.
- The cleanup removes companion files for orphaned volumes, not just the `.pin` / `.nin` index stub.
- Both `-db` and `-dbtype` are required.

---
name: update-blastdb-pl
description: Use when downloading or updating pre-formatted BLAST databases from NCBI or cloud providers (AWS, GCP)
disable-model-invocation: true
user-invocable: true
---

# update-blastdb-pl

## Quick Start
- **Command:** `update_blastdb.pl [options] <blastdb> ...`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/update_blastdb.pl`
- **Full reference:** See `references/help.md`

## When To Use This Tool

- Download official pre-formatted BLAST databases instead of building your own with `makeblastdb`.
- Refresh local copies of databases such as `nt`, `nr`, or taxonomic subsets.
- Discover which prebuilt databases NCBI exposes with `--showall`.
- Pull from `ncbi`, `aws`, or `gcp` depending on your environment and bandwidth path.

## Common Patterns

```bash
# 1) List available databases with human-readable metadata
update_blastdb.pl --showall pretty
```

```bash
# 2) Download and decompress from NCBI into the current directory
update_blastdb.pl \
  --source ncbi \
  --decompress \
  nt
```

```bash
# 3) Download version 4 archives from a cloud mirror
update_blastdb.pl \
  --source aws \
  --blastdb_version 4 \
  swissprot
```

## Recommended Workflow

1. Change into the directory where the database archives or extracted DB should live before running the script.
2. Use `--showall pretty` or `--showall tsv` to confirm the exact database names and metadata.
3. Pick `--source` and `--blastdb_version` intentionally rather than relying on defaults in production workflows.
4. After download, validate the resulting DB with `blastdbcheck` before using it in large search jobs.

## Guardrails

- This script writes into the current working directory, so run it from a dedicated BLAST DB location.
- `--decompress` only applies to `--source ncbi`; it does not give the same behavior for AWS or GCP downloads.
- `curl` is required for cloud-provider retrieval.
- `--quiet` suppresses diagnostics and overrides `--verbose`, so avoid it while troubleshooting.
- `--force` only forces re-download behavior; it does not validate or repair a damaged extracted database.

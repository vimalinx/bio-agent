---
name: blastdbcheck
description: Use when verifying integrity and validity of BLAST databases before using them in search pipelines or troubleshooting database corruption issues.
disable-model-invocation: true
user-invocable: true
---

# blastdbcheck

## Quick Start
- **Command:** `blastdbcheck -db <dbname> -dbtype <prot|nucl> [options]`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/blastdbcheck`
- **Full reference:** See `references/help.md`

## When To Use This Tool

- Validate a BLAST database before running expensive searches.
- Diagnose corruption, missing files, or inconsistent volumes in an existing BLAST DB.
- Audit a whole directory tree of databases with `-dir` and `-recursive`.
- Enforce metadata expectations such as taxonomy IDs with `-must_have_taxids`.

## Common Patterns

```bash
# 1) Quick integrity check of one protein database
blastdbcheck \
  -db swissprot \
  -dbtype prot \
  -verbosity 2
```

```bash
# 2) Exhaustive validation of a critical nucleotide database
blastdbcheck \
  -db nt \
  -dbtype nucl \
  -full \
  -verbosity 3
```

```bash
# 3) Sweep a directory of databases recursively
blastdbcheck \
  -dir /data/blastdb \
  -recursive \
  -verbosity 1
```

## Recommended Workflow

1. Decide whether you are checking one database (`-db`) or scanning a directory (`-dir`).
2. Set `-dbtype` explicitly when the database name is ambiguous instead of relying on `guess`.
3. Start with the default summary mode, then escalate to `-full`, `-random`, `-stride`, or `-ends` depending on how much confidence you need.
4. Treat any failures as a database maintenance problem and repair or re-download the BLAST DB before running downstream searches.

## Guardrails

- Use BLAST+ style flags such as `-help` and `-version`; the common GNU-style `--help` pattern is wrong here.
- `-db` is incompatible with `-dir` and `-recursive`.
- `-full` is incompatible with sampling modes such as `-stride`, `-random`, and `-ends`.
- `-must_have_taxids` is a policy check, not a repair step; older or custom databases may fail it legitimately.
- `-cdd_delta` is only meaningful for CDD / DELTA-BLAST related databases.

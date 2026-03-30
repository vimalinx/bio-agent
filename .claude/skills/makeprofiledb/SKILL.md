---
name: makeprofiledb
description: Use when creating PSSM databases for rpsblast, cobalt, or deltablast searches. Formats position-specific scoring matrices into BLAST-compatible profile databases.
disable-model-invocation: true
user-invocable: true
---

# makeprofiledb

## Quick Start
- **Command:** `makeprofiledb -in <pssm_list> -out <db_name>`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/makeprofiledb`
- **Version:** 2.17.0+
- **Full reference:** See `references/help.md`

## When To Use This Tool

- Build a BLAST-compatible profile database from a list of scoremat or PSSM files.
- Prepare RPS, DELTA, or COBALT profile databases for downstream searches or alignments.
- Package a custom domain collection so `rpsblast` or `deltablast` can use it locally.

## Common Patterns

```bash
# 1) Build a reverse-position-specific domain database
makeprofiledb \
  -in pssm.list \
  -out custom_rps \
  -dbtype rps \
  -title "Custom RPS database"
```

```bash
# 2) Build a DELTA-BLAST profile database
makeprofiledb \
  -in pssm.list \
  -out custom_delta \
  -dbtype delta
```

```bash
# 3) Build from binary scoremats instead of text scoremats
makeprofiledb \
  -in binary_pssm.list \
  -binary \
  -out custom_rps
```

## Recommended Workflow

1. Assemble a plain-text list file naming the PSSM/scoremat inputs.
2. Choose the correct output `-dbtype` for the downstream tool you intend to use.
3. Build the database and verify that the BLAST profile DB sidecar files were created.
4. Test the resulting profile DB with `rpsblast` or `deltablast` before distributing it further.

## Guardrails

- `-in` is required and must point to a list file, not directly to a single PSSM payload.
- `-dbtype` defaults to `rps`; set it explicitly if you actually want `delta` or `cobalt`.
- In this tool, `-force` means use the command-line threshold; it is not an overwrite switch.
- `-taxid` and `-taxid_map` are mutually exclusive.
- Use `-help` rather than `--help`; `--version` also errors in this BLAST+ build.

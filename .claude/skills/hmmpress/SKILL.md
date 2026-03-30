---
name: hmmpress
description: Use when preparing profile HMM databases for use with hmmpgmd (HMMER daemon) by creating compressed binary index files.
disable-model-invocation: true
user-invocable: true
---

# hmmpress

## Quick Start
- **Command:** `hmmpress [-options] <hmmfile>`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/hmmpress`
- **Version:** HMMER 3.4
- **Full reference:** `references/help.md`

## When To Use This Tool

- Prepare a text HMM database for repeated `hmmscan` use.
- Create the binary sidecar files that accelerate HMM database access.
- Re-press a database after rebuilding or concatenating HMMs.
- This is a database-preparation step, not a search step.

## Common Patterns

```bash
# 1) Press an HMM database once
hmmpress Pfam-A.hmm
```

```bash
# 2) Force regeneration of pressed sidecar files
hmmpress -f custom_models.hmm
```

## Recommended Workflow

1. Build or collect all text-format HMMs into one database file.
2. Run `hmmpress` once on that file.
3. Confirm the `.h3m`, `.h3i`, `.h3f`, and `.h3p` sidecars appear beside the source `.hmm`.
4. Use the pressed database with `hmmscan` for repeated annotation jobs.

## Guardrails

- `hmmpress` prepares sidecar indexes for faster HMM database access and is primarily relevant to `hmmscan` workflows.
- The original `.hmm` file must remain in place; `hmmpress` does not replace it.
- Use `-f` if you intentionally want to overwrite previous pressed files.
- Use `-h` for help; `--help` and `--version` are not valid here.

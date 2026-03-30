---
name: rpsblast
description: Use when searching protein sequences against conserved domain databases like CDD using reverse position-specific BLAST
disable-model-invocation: true
user-invocable: true
---

# rpsblast

## Quick Start
- **Command:** `rpsblast -query <input> -db <rpsdb> -out <output> -outfmt 6`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/rpsblast`
- **Version:** 2.17.0+
- **Full reference:** See `references/help.md`

## When To Use This Tool

- Annotate protein queries against conserved-domain PSSM databases such as CDD.
- Detect domain composition and family membership in predicted proteins.
- Prefer `rpsblast` when the target is a reverse-position-specific domain database, not a general protein sequence database.
- Prefer `deltablast` when you want domains to seed a PSSM and then search a protein database.

## Common Patterns

```bash
# 1) Standard conserved-domain annotation run
rpsblast \
  -query proteins.fa \
  -db cdd_db \
  -outfmt "6 qaccver saccver evalue bitscore qstart qend sstart send qcovhsp" \
  -evalue 1e-3 \
  -max_target_seqs 20 \
  -num_threads 8
```

```bash
# 2) Keep BLAST comments in the output for easier manual review
rpsblast \
  -query proteins.fa \
  -db cdd_db \
  -outfmt 7
```

## Recommended Workflow

1. Confirm the query set is protein and the target database is an RPS/PSSM database.
2. Save machine-readable output with explicit columns.
3. Interpret domain calls in the context of whole-domain architecture, not just the top single domain hit.
4. Compare odd results to `hmmscan` or `deltablast` when the database or sensitivity assumptions differ.

## Guardrails

- The query must be protein, and `-db` must point to an RPS/PSSM domain database rather than a standard BLAST protein DB.
- Use `-help` rather than `--help`; `--version` also errors in this BLAST+ build.
- `-remote` is incompatible with local threading.
- Set `-outfmt`, `-evalue`, and `-max_target_seqs` explicitly for reproducible annotation pipelines.

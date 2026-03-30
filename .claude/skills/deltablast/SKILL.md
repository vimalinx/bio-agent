---
name: deltablast
description: Use when performing domain-enhanced protein sequence similarity searches to detect remote homologs using conserved domain databases.
disable-model-invocation: true
user-invocable: true
---

# deltablast

## Quick Start
- **Command:** `deltablast`
- **Local executable**: `/home/vimalinx/miniforge3/envs/bio/bin/deltablast`
- **Version:** 2.17.0+
- **Full reference:** See `references/help.md`

## When To Use This Tool

- Search protein queries for distant homologs when ordinary `blastp` is not sensitive enough.
- Leverage conserved-domain hits to seed a PSSM before searching a protein database.
- Save PSSMs for later inspection or reuse in iterative workflows.
- Prefer ordinary `blastp` for straightforward close homolog searches and `psiblast` when you want fully iterative profile refinement.

## Common Patterns

```bash
# 1) Domain-enhanced search against a protein database
deltablast \
  -query query.fa \
  -db prot_db \
  -rpsdb cdd_delta \
  -outfmt "6 qaccver saccver pident length evalue bitscore qcovhsp" \
  -evalue 1e-3 \
  -max_target_seqs 20 \
  -num_threads 8
```

```bash
# 2) Save the generated PSSM for downstream inspection
deltablast \
  -query query.fa \
  -db prot_db \
  -rpsdb cdd_delta \
  -num_iterations 2 \
  -out_pssm query.pssm
```

```bash
# 3) Tighten sequence and domain inclusion thresholds
deltablast \
  -query query.fa \
  -db prot_db \
  -rpsdb cdd_delta \
  -inclusion_ethresh 1e-4 \
  -domain_inclusion_ethresh 1e-3
```

## Recommended Workflow

1. Start with protein queries and confirm that both the target protein database and the RPS domain database are available locally.
2. Save machine-readable output and, when useful, the generated PSSM.
3. Tune inclusion thresholds and iteration count only after examining the first-pass behavior.
4. Compare suspicious results to a plain `blastp` run so the domain enhancement is actually helping.

## Guardrails

- DELTA-BLAST expects protein queries and protein search databases.
- `-rpsdb` is central to the method and is incompatible with `-remote` and `-subject` in this build.
- `-num_iterations` is not available with `-remote`.
- Use `-help` rather than `--help`; `--version` also errors here.

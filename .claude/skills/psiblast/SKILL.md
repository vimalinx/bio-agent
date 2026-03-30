---
name: psiblast
description: Use when detecting distant protein homologs via iterative profile-based searches, building position-specific scoring matrices (PSSMs), or refining sequence similarity searches beyond standard BLASTP.
disable-model-invocation: true
user-invocable: true
---

# psiblast

## Quick Start
- **Command:** `psiblast`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/psiblast`
- **Version:** 2.17.0+
- **Full reference:** See `references/help.md` for complete options and usage details

## When To Use This Tool

- Detect distant protein homologs that plain `blastp` may miss.
- Build a PSSM for reuse in later searches.
- Restart from an existing PSSM or MSA checkpoint.
- Use only when you are prepared to monitor profile drift across iterations.

## Common Patterns

```bash
# 1) Iterative distant-homology search with saved PSSM
psiblast \
  -query query.fa \
  -db prot_db \
  -num_iterations 5 \
  -evalue 1e-3 \
  -inclusion_ethresh 1e-3 \
  -out_pssm query.pssm \
  -outfmt 7
```

```bash
# 2) Save an ASCII PSSM for inspection or downstream tools
psiblast \
  -query query.fa \
  -db prot_db \
  -num_iterations 3 \
  -out_ascii_pssm query.ascii.pssm
```

```bash
# 3) Restart from an existing checkpoint
psiblast \
  -in_pssm query.pssm \
  -db prot_db \
  -num_iterations 2 \
  -outfmt 6
```

## Recommended Workflow

1. Start from a high-confidence protein query or curated alignment.
2. Set `-inclusion_ethresh` conservatively so poor hits do not contaminate the profile.
3. Inspect each iteration's accepted hits before trusting convergence.
4. Save the final PSSM if the profile will be reused or compared later.

## Guardrails
- Input must be protein sequence, protein MSA, or protein PSSM, never nucleotide query sequence.
- More iterations are not always better; false positives can poison the profile early.
- `-evalue` controls reporting, while `-inclusion_ethresh` controls what enters the next-round model.
- Save checkpoints (`-out_pssm`, `-out_ascii_pssm`) if the iterative result matters scientifically.

---
name: rpstblastn
description: Use when searching nucleotide sequences against protein domain profile databases (PSSMs) to detect conserved domains via position-specific scoring.
disable-model-invocation: true
user-invocable: true
---

# rpstblastn

## Quick Start
- **Command:** `rpstblastn -query <nucleotide.fasta> -db <pssm_db> -out <results.out>`
- **Local executable**: `/home/vimalinx/miniforge3/envs/bio/bin/rpstblastn`
- **Version:** 2.17.0+
- **Full reference:** See `references/help.md`

## When To Use This Tool

- Search nucleotide queries against conserved-domain PSSM databases without translating and extracting ORFs manually first.
- Detect protein-domain content in transcripts, contigs, or genomic intervals.
- Prefer `rpsblast` if the query is already protein, and `blastx` if the target is a full protein sequence database rather than a domain database.

## Common Patterns

```bash
# 1) Standard translated domain search against a PSSM database
rpstblastn \
  -query contigs.fa \
  -db cdd_db \
  -query_gencode 11 \
  -outfmt "6 qaccver saccver evalue bitscore qstart qend sstart send qcovhsp" \
  -evalue 1e-3 \
  -max_target_seqs 20 \
  -num_threads 8
```

```bash
# 2) Restrict the search to one query strand
rpstblastn \
  -query contigs.fa \
  -db cdd_db \
  -strand plus \
  -outfmt 7
```

## Recommended Workflow

1. Start from nucleotide FASTA queries and a valid PSSM domain database.
2. Set the query genetic code and strand explicitly when the biology is not generic nuclear DNA.
3. Emit tabular output with explicit fields for downstream parsing.
4. Interpret hits as conserved-domain evidence, not as full-length protein orthology by themselves.

## Guardrails

- `-db` must be a PSSM/profile database, not a standard nucleotide or protein BLAST DB.
- Use `-help` rather than `--help`; `--version` errors in this BLAST+ build.
- `-remote` is incompatible with local threading.
- Translated domain searches can be noisy on raw contigs, so set `-query_gencode`, `-strand`, `-outfmt`, and `-evalue` deliberately.

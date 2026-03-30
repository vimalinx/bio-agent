---
name: makeblastdb
description: Use when creating BLAST databases from FASTA sequence files for use with blastn, blastp, blastx, or other BLAST search tools.
disable-model-invocation: true
user-invocable: true
---

# makeblastdb

## Quick Start
- **Command:** `makeblastdb`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/makeblastdb`
- **Version:** 2.17.0+
- **Full reference:** See `references/help.md` for complete option documentation

## When To Use This Tool

- Build local BLAST databases from FASTA before `blastn`, `blastp`, or `tblastn`.
- Create nucleotide (`nucl`) or protein (`prot`) databases with stable names.
- Enable identifier-aware retrieval with `-parse_seqids`.
- Attach taxonomy with `-taxid` or `-taxid_map` when downstream filtering requires it.

## Common Patterns

```bash
# 1) Build a nucleotide database
makeblastdb \
  -in transcripts.fa \
  -dbtype nucl \
  -out transcripts_db \
  -parse_seqids
```

```bash
# 2) Build a protein database
makeblastdb \
  -in proteins.fa \
  -dbtype prot \
  -out proteins_db \
  -parse_seqids
```

```bash
# 3) Build a taxonomy-aware database
makeblastdb \
  -in proteins.fa \
  -dbtype prot \
  -out proteins_db \
  -parse_seqids \
  -taxid_map seqid_to_taxid.tsv
```

## Recommended Workflow

1. Decide database molecule type up front: `nucl` or `prot`.
2. Use `-parse_seqids` if you will retrieve by accession or use taxonomy mapping later.
3. Keep the database basename stable so pipeline code does not chase renamed indexes.
4. Validate the created database immediately with a small BLAST query or `blastdbcmd -info`.

## Guardrails
- `-dbtype` is required and must be exactly `nucl` or `prot`.
- `-taxid_map` requires `-parse_seqids`.
- BLAST DB version defaults to `5`; keep that consistent across a workflow unless you have a compatibility reason not to.
- If you skip `-parse_seqids`, later `blastdbcmd` retrieval by sequence ID may be painful or impossible.

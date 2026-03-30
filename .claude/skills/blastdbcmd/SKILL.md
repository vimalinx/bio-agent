---
name: blastdbcmd
description: Use when retrieving sequences or metadata from local BLAST databases, looking up entries by identifier or taxonomy, or inspecting database contents.
disable-model-invocation: true
user-invocable: true
---

# blastdbcmd

## Quick Start
- **Command:** `blastdbcmd`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/blastdbcmd`
- **Version:** 2.17.0+
- **Full reference:** See [references/help.md](references/help.md) for complete options

## When To Use This Tool

- Inspect a BLAST database after building it.
- Retrieve one or many sequences by identifier from a local BLAST DB.
- Export taxonomy summaries or database metadata.
- Sanity-check that `makeblastdb` produced what your pipeline expects.

## Common Patterns

```bash
# 1) Inspect database metadata
blastdbcmd -db proteins_db -info
```

```bash
# 2) Retrieve one entry in FASTA format
blastdbcmd \
  -db proteins_db \
  -entry XP_123456.1 \
  -outfmt "%f"
```

```bash
# 3) Retrieve many entries from a batch file
blastdbcmd \
  -db proteins_db \
  -entry_batch ids.txt \
  -outfmt "%f" \
  -out hits.fa
```

```bash
# 4) Export taxonomy summary
blastdbcmd -db proteins_db -tax_info
```

## Recommended Workflow

1. Use `-info` first to confirm the database type and metadata.
2. Retrieve by `-entry` or `-entry_batch` only if the DB was built with usable sequence IDs.
3. Use `-outfmt` deliberately; `%f` is the common FASTA choice for sequence export.
4. For taxonomic inspection, use `-tax_info` rather than trying to parse raw metadata blobs.

## Guardrails
- `-entry`, `-entry_batch`, `-info`, `-metadata`, and `-tax_info` are mutually exclusive modes.
- Range and strand selection only make sense for nucleotide sequence retrieval.
- `-entry all` can dump an entire database, which is often much larger than expected.
- If retrieval by accession fails, the underlying DB may have been built without `-parse_seqids`.

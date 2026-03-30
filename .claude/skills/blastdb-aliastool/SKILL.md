---
name: blastdb-aliastool
description: Use when creating BLAST database aliases, converting GI files to binary format, or aggregating multiple BLAST databases into a single virtual database.
disable-model-invocation: true
user-invocable: true
---

# blastdb-aliastool

## Quick Start
- **Command**: `blastdb_aliastool -db dbname -gilist ids.txt -out alias_name`
- **Local executable**: `/home/vimalinx/miniforge3/envs/bio/bin/blastdb_aliastool`
- **Version:** 2.17.0+
- **Full reference:** See `references/help.md`

## When To Use This Tool

- Create a virtual alias that points to a restricted subset of an existing BLAST database.
- Aggregate multiple BLAST databases of the same molecule type into one logical database.
- Convert legacy GI or SeqID lists into binary list formats for faster reuse.
- Build taxon-, accession-, or curated-subset views without rebuilding the source BLAST DB.

## Common Patterns

```bash
# 1) Restrict a protein database by sequence IDs
blastdb_aliastool \
  -db nr \
  -dbtype prot \
  -seqidlist ids.txt \
  -out nr_subset \
  -title "NR subset"
```

```bash
# 2) Aggregate several protein databases into one alias
blastdb_aliastool \
  -dblist "db1 db2 db3" \
  -dbtype prot \
  -out combined_db \
  -title "Combined BLAST DB"
```

```bash
# 3) Convert a text seqid list into binary form
blastdb_aliastool \
  -seqid_file_in ids.txt \
  -seqid_db nr \
  -seqid_dbtype prot \
  -seqid_file_out ids.bsl
```

## Recommended Workflow

1. Decide whether you are restricting one database, aggregating several databases, or converting a list format.
2. Prepare the needed list files and confirm the source BLAST DB type (`nucl` or `prot`).
3. Create the alias or binary list file and then test it immediately with a small BLAST query.
4. Keep the alias definition next to the source databases so it stays resolvable in downstream environments.

## Guardrails

- The executable on disk is named `blastdb_aliastool`, even though this skill is named `blastdb-aliastool`.
- Aggregated databases must all be the same molecule type; the tool does not validate that for you.
- `-gilist`, `-seqidlist`, `-taxidlist`, and `-oid_masks` are alternative restriction modes, not options you usually combine.
- `-dblist` and `-dblist_file` require `-out`, `-dbtype`, and `-title`.
- GI-based workflows are legacy; prefer SeqID or taxonomy-based restriction for modern pipelines when possible.

---
name: blastn-vdb
description: Use when searching nucleotide sequences against SRA/VDB databases using BLAST. Invokes blastn_vdb for nucleotide-nucleotide alignment with SRA accessions.
disable-model-invocation: true
user-invocable: true
---

# blastn-vdb

## Quick Start
- **Command:** `blastn_vdb -query query.fa -db <SRA_or_WGS_name> [options]`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/blastn_vdb`
- **Full reference:** See `references/help.md`

## When To Use This Tool

- Run nucleotide BLAST directly against SRA or WGS-backed VDB data sources.
- Search sequencing reads or aligned reference sequences without first building a local BLAST DB.
- Control whether the search targets unaligned reads, aligned reference sequences, or both via `-sra_mode`.
- Keep a BLASTN-like workflow while operating in the VDB / SRA ecosystem.

## Common Patterns

```bash
# 1) Search an accession's unaligned reads with tabular output
blastn_vdb \
  -query query.fa \
  -db SRR123456 \
  -sra_mode 0 \
  -outfmt 6 \
  -evalue 1e-10 \
  -num_threads 8
```

```bash
# 2) Search aligned reference sequences only
blastn_vdb \
  -query query.fa \
  -db SRR123456 \
  -sra_mode 1 \
  -out results.txt
```

```bash
# 3) Include filtered reads and cap hit count
blastn_vdb \
  -query query.fa \
  -db SRR123456 \
  -include_filtered_reads \
  -max_target_seqs 20 \
  -outfmt "6 qaccver saccver pident length evalue bitscore"
```

## Recommended Workflow

1. Confirm the target accession or VDB source is available and that you really want SRA-backed search rather than a local BLAST database.
2. Set `-sra_mode` deliberately: `0` for unaligned reads, `1` for aligned reference sequences, `2` for both.
3. Use explicit `-outfmt`, `-evalue`, and `-max_target_seqs` settings so results remain predictable across runs.
4. Start with a small query set before scaling up to larger accession-backed searches.

## Guardrails

- `-db` here is an SRA or WGS source name, not a standard local BLAST database path.
- The default task is `megablast`; override `-task` if you need `blastn-short`, `dc-megablast`, or another mode.
- Use BLAST+ style flags such as `-help` and `-version`; the usual `--help` pattern is wrong in this build.
- `-num_descriptions` and `-num_alignments` are incompatible with `-max_target_seqs`.
- `-include_filtered_reads` and `-sra_mode` can materially change the search universe, so record them in reproducible workflows.

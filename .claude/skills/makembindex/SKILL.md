---
name: makembindex
description: Use when you need to create a BLAST database index for faster search operations on BLAST databases.
disable-model-invocation: true
user-invocable: true
---

# makembindex

## Quick Start
- **Command:** `makembindex -input <db_or_fasta> -output <index_prefix> [options]`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/makembindex`
- **Full reference:** See `references/help.md`

## When To Use This Tool

- Build a BLAST database index as an explicit performance or infrastructure step.
- Tune index construction parameters such as `-nmer`, `-stride`, `-volsize`, or `-ws_hint`.
- Generate an index from either an existing BLAST DB or FASTA input, depending on `-iformat`.
- Inspect available masking filters with `-show_filters` before using `-db_mask`.

## Common Patterns

```bash
# 1) Build an index from an existing BLAST database
makembindex \
  -input nt \
  -iformat blastdb \
  -output nt.mbidx
```

```bash
# 2) Dry-run a custom index configuration
makembindex \
  -input ref.fa \
  -iformat fasta \
  -output ref.mbidx \
  -nmer 12 \
  -stride 4 \
  -dryrun
```

```bash
# 3) List masking filters available in the source BLAST DB
makembindex \
  -input nt \
  -show_filters
```

## Recommended Workflow

1. Decide whether the source is a BLAST database or FASTA and set `-iformat` deliberately.
2. Start with a conservative index build, then only tune `-nmer`, `-stride`, `-volsize`, or `-ws_hint` if you have a concrete search-performance reason.
3. Use `-dryrun` first when testing parameters on large databases.
4. Keep the index artifacts alongside the database they were built from and rebuild them if the underlying DB changes.

## Guardrails

- This is an advanced BLAST infrastructure tool, not a routine prerequisite for every BLAST database.
- `-output` is incompatible with `-show_filters`.
- `-db_mask` requires `-input` and only makes sense when the source DB actually carries masking metadata.
- `-legacy` and `-old_style_index` are compatibility switches; do not enable them casually.
- Use BLAST+ flag style such as `-help` and `-version`, not `--help`.

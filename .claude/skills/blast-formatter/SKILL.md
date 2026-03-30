---
name: blast-formatter
description: Use when you need to reformat BLAST archive files into different output formats (tabular, HTML, custom) without re-running the BLAST search.
disable-model-invocation: true
user-invocable: true
---

# blast-formatter

## Quick Start
- **Command:** `blast_formatter -archive <archive.asn> -outfmt <format> -out <output>`
- **Local executable**: `/home/vimalinx/miniforge3/envs/bio/bin/blast_formatter`
- **Version:** 2.17.0+
- **Full reference:** See `references/help.md`

## When To Use This Tool

- Reformat a saved BLAST archive (`outfmt 11`) into tabular, XML, JSON, SAM, pairwise text, or HTML output.
- Render the same search result in multiple formats without recomputing the alignment search.
- Pull results by RID after a remote BLAST job finishes.
- Define custom tabular field lists once the archive already exists.

## Common Patterns

```bash
# 1) Reformat a saved archive as tabular output
blast_formatter \
  -archive search.asn \
  -outfmt "6 qaccver saccver pident length evalue bitscore" \
  -out hits.tsv
```

```bash
# 2) Generate an HTML report from the same archive
blast_formatter \
  -archive search.asn \
  -html \
  -outfmt 0 \
  -out report.html
```

```bash
# 3) Retrieve and format a completed remote search by RID
blast_formatter \
  -rid RID_VALUE \
  -outfmt 5 \
  -out result.xml
```

## Recommended Workflow

1. Save BLAST searches as archive format (`-outfmt 11`) whenever you may want multiple downstream renderings.
2. Reformat the archive into the specific machine-readable or human-readable representation you need.
3. Use custom field lists with `-outfmt 6`, `7`, `10`, `17`, or `20` instead of accepting defaults blindly.
4. Keep the original archive so you can regenerate other views later.

## Guardrails

- `-archive` and `-rid` are mutually exclusive inputs.
- This tool does not rerun BLAST; it only formats an archive or completed remote request.
- `-max_target_seqs` cannot be combined with `-num_descriptions` or `-num_alignments`.
- The command name on disk is `blast_formatter` even though this skill is named `blast-formatter`.

---
name: flatten-gtf
description: Use when you need to flatten exon-like GTF/GFF features into SAF meta-features for Subread or featureCounts workflows.
disable-model-invocation: true
user-invocable: true
---

# flatten-gtf

## Quick Start

- **Command**: `flattenGTF -a <input.gtf> -o <output.saf>`
- **Local executable**: `/home/vimalinx/miniforge3/envs/bio/bin/flattenGTF`
- **Full reference**: See [references/help.md](references/help.md)

## When To Use This Tool

- Convert GTF or GFF annotations into SAF for Subread-family tools.
- Flatten overlapping exon-like intervals into meta-features grouped by `gene_id` or another chosen attribute.
- Prepare annotation files for `featureCounts` workflows that prefer SAF over raw GTF/GFF parsing.

## Common Patterns

```bash
# 1) Default flattening: exon features grouped by gene_id
/home/vimalinx/miniforge3/envs/bio/bin/flattenGTF \
  -a genes.gtf \
  -o genes.saf
```

```bash
# 2) Flatten a different feature type or grouping attribute
/home/vimalinx/miniforge3/envs/bio/bin/flattenGTF \
  -a annotation.gff3 \
  -o cds_by_tx.saf \
  -t CDS \
  -g transcript_id
```

```bash
# 3) Keep exon boundaries while still producing non-overlapping output
/home/vimalinx/miniforge3/envs/bio/bin/flattenGTF \
  -a genes.gtf \
  -o genes.keep_edges.saf \
  -C
```

## Recommended Workflow

1. Start from an annotation built against the same assembly as your alignments.
2. Decide whether the defaults (`-t exon`, `-g gene_id`) match the downstream counting unit you want.
3. Write SAF to a new file with `-o` and inspect a few rows before large batch counting.
4. If merged intervals look too coarse, retry with `-C` to preserve exon edges.

## Guardrails

- `flattenGTF` is the actual binary name; `flatten-gtf` is just the skill folder name.
- `-a` and `-o` are mandatory, and the tool writes SAF to disk rather than stdout.
- `--help` and `--version` are not standard GNU modes here; they print `unrecognized option` and then fall through to the usage banner.
- Defaults are `-t exon` and `-g gene_id`; if those attributes are absent the run will fail rather than guess.

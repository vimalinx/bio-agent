---
name: split-at-intron
description: Use when processing genomic sequences that require splitting at intron boundaries as part of Entrez Direct workflows.
disable-model-invocation: true
user-invocable: true
---

# split-at-intron

## Quick Start
- **Command:** `cat alignment-tags.tsv | split-at-intron`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/split-at-intron`
- **Full reference:** See [references/help.md](references/help.md) for complete usage details

## When To Use This Tool

- Split an Entrez Direct tag/value alignment stream into exon-like genomic spans.
- Convert long alignment event streams into comma-separated genomic intervals around large intronic skips.
- Post-process EDirect alignment summaries rather than ordinary BED/GFF/VCF files.

## Common Patterns

```bash
# 1) Split an EDirect tag/value stream at large genomic insertions
cat alignment-tags.tsv | split-at-intron
```

```bash
# 2) Minimal illustrative event stream
cat <<'EOF' | split-at-intron
index	1
score	95
start	1000
strand	plus
match	80
genomic-ins	120
match	50
end	0
EOF
```

## Recommended Workflow

1. Make sure the upstream step emits the expected tab-separated tag/value stream with fields like `index`, `score`, `start`, `strand`, `match`, `genomic-ins`, and `end`.
2. Pipe that stream into `split-at-intron`; the tool does not take ordinary interval files or command-line arguments.
3. Inspect the emitted interval list to confirm that large genomic insertions were split into separate segments.
4. Feed the resulting coordinate strings only into downstream code that understands this EDirect-style output format.

## Guardrails

- This tool reads stdin and expects a very specific Entrez Direct tag/value event stream; it is not a generic intron splitter for BED, GFF, or FASTA.
- In the bundled script, only `genomic-ins` events of length `>= 30` trigger a split; shorter insertions are absorbed into the current span.
- The output format is a compact coordinate representation, not a standard BED file.
- If the upstream stream is missing tags such as `start`, `strand`, or `end`, the output will be incomplete or meaningless.

---
name: fasta-sanitize-pl
description: Use when sanitizing FASTA or FASTQ record names so they conform to SAM-compatible reference / read-name character rules.
disable-model-invocation: true
user-invocable: true
---

# fasta-sanitize-pl

## Quick Start

- **Command:** `zcat input.fa.gz | /home/vimalinx/miniforge3/envs/bio/bin/fasta-sanitize.pl > output.fa`
- Local executable: `/home/vimalinx/miniforge3/envs/bio/bin/fasta-sanitize.pl`
- Reference: [references/help.md](references/help.md)

## When To Use This Tool

- Rewrite invalid FASTA / FASTQ record names before alignment or downstream SAM / VCF generation.
- Keep reference names consistent with SAM naming constraints early in the workflow.
- Sanitize both FASTA and FASTQ headers with one streaming pass.

## Common Patterns

```bash
# 1) Sanitize a FASTA stream before indexing or alignment
zcat input.fa.gz | \
  /home/vimalinx/miniforge3/envs/bio/bin/fasta-sanitize.pl \
  > clean.fa
```

```bash
# 2) Sanitize FASTQ headers in a streaming pipeline
zcat reads.fq.gz | \
  /home/vimalinx/miniforge3/envs/bio/bin/fasta-sanitize.pl \
  > clean.fq
```

## Recommended Workflow

1. Run it before alignment or any step that depends on consistent SAM-compatible names.
2. Capture stdout to a new FASTA / FASTQ file.
3. Watch stderr for `Renaming reference ...` messages.
4. Rebuild any downstream indices from the sanitized file rather than mixing old names with new ones.

## Guardrails

- The tool does not support `--help` or `--version` flags; it expects file arguments.
- It autodetects FASTQ by `@` headers and handles quality blocks, not just FASTA.
- Only the first whitespace-delimited token in the header is sanitized as the record name; trailing descriptive text is preserved.
- Valid names pass through unchanged, so not every file will emit rename messages on stderr.

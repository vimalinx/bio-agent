---
name: bowtie2-inspect-l
description: Use when you need to inspect or extract information from a Bowtie 2 large index (.bt2l) file, including reference sequence names, lengths, or FASTA sequences.
disable-model-invocation: true
user-invocable: true
---

# bowtie2-inspect-l

## Quick Start

- **Command**: `bowtie2-inspect-l <bt2_base>`
- **Local executable**: `/home/vimalinx/miniforge3/envs/bio/bin/bowtie2-inspect-l`
- **Full reference**: See [references/help.md](references/help.md) for complete options and details

## When To Use This Tool

- Use `bowtie2-inspect-l` when you know the target index is a Bowtie 2 large index (`.bt2l`) and want to inspect it directly.
- It is useful for checking reference names, emitting a summary, or reconstructing FASTA from a large index without relying on wrapper auto-detection.
- Use it when troubleshooting large-index-specific behavior or when the generic inspector is not explicit enough about which index flavor to read.
- In normal usage, the `bowtie2-inspect` wrapper is usually preferable.

## Common Patterns

```bash
# Summarize a large Bowtie 2 index
bowtie2-inspect-l -s ref_large

# List reference names only
bowtie2-inspect-l -n ref_large

# Recover FASTA from a large index
bowtie2-inspect-l ref_large > ref_large.fa

# Save summary output to a file
bowtie2-inspect-l -s ref_large -o ref_large.summary.txt
```

## Recommended Workflow

1. Identify the bt2 base name (filename minus `.1.bt2l` or `.2.bt2l` extension)
2. Run `bowtie2-inspect-l -s <bt2_base>` to get a summary of the index
3. Use `-n` to list reference sequence names only, or default for FASTA output
4. Redirect output to a file with `-o <filename>` if needed

## Guardrails

- Input must be a Bowtie 2 large index (`.bt2l` format), not standard `.bt2`
- The `<bt2_base>` argument excludes the trailing `.1.bt2l`/`.2.bt2l` extension
- Use `bowtie2-inspect` (without `-l`) for standard non-large indexes
- The direct executable prints a wrapper warning on startup; that is expected and not itself an error

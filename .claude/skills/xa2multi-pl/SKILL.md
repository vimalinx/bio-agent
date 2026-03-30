---
name: xa2multi-pl
description: Use when expanding BWA `XA:Z` alternate-alignment tags in SAM records into separate secondary SAM alignments for downstream tools.
disable-model-invocation: true
user-invocable: true
---

# xa2multi-pl

Tiny Perl filter for BWA SAM output. For every alignment line containing `XA:Z:...`, it prints the original line unchanged and appends one extra SAM record per alternate hit, marking those records as secondary alignments and copying the mismatch count into `NM:i`.

## Quick Start

- **Command:** `xa2multi.pl [input.sam]`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/xa2multi.pl`
- **Input style:** SAM on stdin or as filenames on the command line

## When To Use This Tool

- Converting BWA alternate hits from compact `XA:Z` tags into explicit SAM records
- Preparing alignments for downstream tools that ignore or discard `XA` optional fields
- Inspecting or counting alternate mappings as ordinary SAM records
- Normalizing legacy BWA output before later SAM/BAM processing

## Common Patterns

```bash
# Expand XA-tagged alignments from a SAM file
xa2multi.pl input.sam > expanded.sam
```

```bash
# Stream from stdin into another SAM/BAM step
samtools view -h input.bam | xa2multi.pl | samtools view -b -o expanded.bam
```

```text
Observed in local testing:
primary line: unchanged
alternate hits: emitted with flags 256 / 272 and NM:i copied from the XA field
```

## Recommended Workflow

1. Start from BWA SAM output that actually contains `XA:Z` tags.
2. Run `xa2multi.pl` before downstream tools that expect each alignment as its own SAM record.
3. Redirect stdout to a new SAM/BAM stream because the script never edits files in place.
4. Validate a few records afterward to confirm the expected number of alternate alignments were emitted.

## Guardrails

- The script has no built-in `-h` or `--version`; it simply reads stdin or filenames via Perl's `<>` operator.
- It only reacts to lines containing `XA:Z:`. All other lines, including SAM headers, are printed unchanged.
- Source inspection shows each alternate alignment is emitted as a secondary record with `0x100` set, `MAPQ` forced to `0`, and `TLEN` forced to `0`.
- If the alternate orientation differs from the primary alignment, the script reverse-complements the sequence and reverses the quality string.
- The source includes `# FIXME: TLEN/ISIZE is not calculated!`, so do not treat inferred template length as trustworthy after expansion.

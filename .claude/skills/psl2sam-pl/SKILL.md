---
name: psl2sam-pl
description: Use when converting UCSC PSL alignments into SAM and controlling the simple alignment score calculation.
disable-model-invocation: true
user-invocable: true
---

# psl2sam-pl

## Quick Start

- **Command:** `psl2sam.pl [-a INT] [-b INT] [-q INT] [-r INT] input.psl > output.sam`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/psl2sam.pl`
- **Reference:** See [references/help.md](references/help.md)

## When To Use This Tool

- Convert UCSC PSL alignments into SAM.
- Recalculate an `AS:i` alignment score from PSL match, mismatch, and gap counts.
- Preserve clipped alignment structure when translating PSL block coordinates into SAM CIGAR strings.
- Use simple PSL-to-SAM conversion when you do not need a full splice-aware aligner rerun.

## Common Patterns

```bash
# 1) Convert PSL to SAM with default scoring
psl2sam.pl \
  alignments.psl > alignments.sam
```

```bash
# 2) Use custom score weights for matches, mismatches, gap opens, and extensions
psl2sam.pl \
  -a 2 -b 4 -q 5 -r 1 \
  alignments.psl > rescored.sam
```

```bash
# 3) Stream PSL from stdin
cat alignments.psl | psl2sam.pl > alignments.sam
```

## Recommended Workflow

1. Confirm the input is ordinary PSL and not PSLX or some downstream PSL-derived report.
2. Decide whether the default score weights are acceptable or whether you need explicit `-a`, `-b`, `-q`, and `-r` values.
3. Convert to SAM, then inspect a few long-gap records to confirm the CIGAR output is acceptable for your downstream use.
4. If the PSL represents spliced transcript alignments, verify whether this simple converter is sufficient before using the result in splice-aware analyses.

## Guardrails

- `-a`, `-b`, `-q`, and `-r` only change the computed `AS:i` score; they do not alter the underlying alignment coordinates.
- The script does not emit reference-skip `N` operators in CIGAR strings, so intron-like PSL gaps are represented as insertions/deletions instead of splice skips.
- Help comes from Perl `Getopt::Std`, so `--help` works generically but `-help` is the wrong pattern for this script family.
- Output is plain SAM records without a SAM header.

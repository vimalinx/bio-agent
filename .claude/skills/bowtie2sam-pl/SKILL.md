---
name: bowtie2sam-pl
description: Use when converting legacy Bowtie text output into SAM and retaining only the best alignment per read.
disable-model-invocation: true
user-invocable: true
---

# bowtie2sam-pl

## Quick Start

- **Command:** `bowtie2sam.pl alignments.bowtie > alignments.sam`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/bowtie2sam.pl`
- **Reference:** See [references/help.md](references/help.md)

## When To Use This Tool

- Convert legacy tab-delimited Bowtie output into SAM.
- Collapse multiple Bowtie hits for a read down to a single best-hit SAM record.
- Preserve Bowtie-provided read sequence and quality strings while moving into SAM-compatible tooling.
- Use this only for old Bowtie text output, not for Bowtie's native SAM mode.

## Common Patterns

```bash
# 1) Convert a Bowtie output file into SAM
bowtie2sam.pl \
  alignments.bowtie > alignments.sam
```

```bash
# 2) Stream Bowtie output directly into the converter
bowtie index reads.fq | bowtie2sam.pl > alignments.sam
```

```bash
# 3) Group by read name first if the Bowtie output was reordered
sort -k1,1 alignments.bowtie | bowtie2sam.pl > alignments.best.sam
```

## Recommended Workflow

1. Confirm the input is legacy Bowtie text output rather than SAM emitted with Bowtie's own `-S` mode.
2. Keep alignments grouped by read name so the script can compare all hits for a read together.
3. Convert to SAM, then inspect a few records to confirm the chosen best hit and MAPQ behavior are sensible for your data.
4. If you need all multimapping hits, stop and use a different conversion route instead of this script.

## Guardrails

- There is no real command-line help interface here: `--help` and `--version` are treated like filenames and can trigger file-open errors plus downstream warnings.
- The script emits one best alignment per read, not all reported Bowtie hits.
- Input should stay grouped by read name; otherwise best-hit selection can be wrong because the script resolves hits only within adjacent name blocks.
- Output is plain SAM records without a SAM header.

---
name: bedpe-to-bam
description: Use when converting BEDPE (or BED/GFF/VCF) feature records to BAM format for downstream analysis.
disable-model-invocation: true
user-invocable: true
---

# bedpe-to-bam

## Quick Start
- **Command:** `bedpeToBam -i pairs.bedpe -g genome.txt [options] > output.bam`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/bedpeToBam`
- **Full reference:** See `references/help.md`

## When To Use This Tool

- Convert paired-end interval records into BAM-like output.
- Represent pair geometry in BAM for downstream visualization or tooling compatibility.
- Assign a consistent mapping-quality field to synthetic BAM records.
- Produce uncompressed BAM output when piping directly into other tools.

## Common Patterns

```bash
# 1) Convert BEDPE to BAM
bedpeToBam \
  -i pairs.bedpe \
  -g genome.txt > pairs.bam
```

```bash
# 2) Set a custom mapping quality
bedpeToBam \
  -i pairs.bedpe \
  -g genome.txt \
  -mapq 60 > pairs.mapq60.bam
```

```bash
# 3) Stream uncompressed BAM
bedpeToBam \
  -i pairs.bedpe \
  -g genome.txt \
  -ubam > pairs.ubam
```

## Recommended Workflow

1. Confirm the input really represents paired features and that the genome file matches its coordinate system.
2. Use a clear mapping-quality policy if the BAM will be consumed by tools that inspect MAPQ.
3. Emit the BAM, then inspect a few records with `samtools view` or a browser.
4. Keep this as a format-conversion step rather than a substitute for real aligner-produced BAM when alignment semantics matter.

## Guardrails

- `-i` and `-g` are required.
- The help text is sparse; verify the exact input schema you are converting before trusting the resulting BAM semantics.
- Default mapping quality is `255`, which is a placeholder-like value rather than an inferred alignment score.
- `-ubam` changes the output stream format but not the record semantics.
- Prefer `-h` for help; GNU-style `--help` / `--version` calls on these wrappers are noisy.

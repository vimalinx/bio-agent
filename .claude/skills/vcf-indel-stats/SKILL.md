---
name: vcf-indel-stats
description: Use when calculating in-frame indel ratios from VCF files, optionally with exon annotations.
disable-model-invocation: true
user-invocable: true
---

# vcf-indel-stats

## Quick Start
- **Command**: `vcf-indel-stats [OPTIONS] < in.vcf > out.txt`
- **Local executable**: `/home/vimalinx/miniforge3/envs/bio/bin/vcf-indel-stats`
- **Full reference**: See `references/help.md`

## When To Use This Tool

- Estimate the in-frame fraction of indels in a VCF.
- Add exon-aware context to the in-frame calculation with a simple exon interval file.
- Produce a quick textual sanity check on indel frame behavior before deeper annotation.

## Common Patterns

```bash
# 1) Compute basic indel frame statistics
cat indels.vcf | vcf-indel-stats > indel_stats.txt
```

```bash
# 2) Use exon intervals for exon-aware stats
cat indels.vcf | vcf-indel-stats -e exons.tsv > indel_stats.txt
```

## Recommended Workflow

1. Start from a VCF that actually contains the indels you want to summarize.
2. If coding context matters, prepare a tab-separated exon file with 1-based inclusive intervals.
3. Stream the VCF into `vcf-indel-stats`, optionally with `-e`.
4. Treat the output as a rough descriptive statistic, then escalate to richer annotation if the result matters for interpretation.

## Guardrails

- Input comes from stdin.
- The exon file format is strict: `chr`, `from`, `to`, tab-separated, 1-based inclusive.
- This script currently reports in-frame ratio style summaries; it is not a full functional annotation engine.
- Use `-v` only for debugging or detailed logging, not as a substitute for validating the biological input set.

---
name: esl-alistat
description: Use when working with alignment files and needing statistics from HMMER's Easel toolkit.
disable-model-invocation: true
user-invocable: true
---

# esl-alistat

## Quick Start

- Command: `esl-alistat [options] <alignment_file>`
- Local executable: `/home/vimalinx/miniforge3/envs/bio/bin/esl-alistat`
- Reference: See [references/help.md](references/help.md) for detailed options

## When To Use This Tool

- Use `esl-alistat` when you need summary statistics on one or more multiple sequence alignments rather than on raw sequences.
- It is suited to alignment-level questions such as average identity, alignment length, composition, and annotation-derived information content summaries.
- Use it before HMM construction, masking, or curation when you want to inspect alignment quality and content.
- In this environment it is currently blocked by a shared-library issue, so treat it as documented-but-not-runnable until the dependency is repaired.

## Common Patterns

```bash
# Basic alignment statistics
esl-alistat alignment.sto

# Write a per-alignment list report
esl-alistat --list alns.list alignment.sto

# Export information-content and composition reports
esl-alistat --icinfo ic.txt --cinfo comp.txt alignment.sto

# Export pairwise-identity or posterior-probability related reports when present
esl-alistat --pcinfo pc.txt --psinfo ps.txt alignment.sto
```

## Recommended Workflow

1. Verify shared library dependencies are satisfied before use.
2. Start with a plain `esl-alistat <alignment_file>` run to confirm the binary works in the current environment.
3. Add report-output options such as `--list`, `--icinfo`, `--cinfo`, or `--bpinfo` only if the input alignment carries the needed annotation.
4. Review the generated reports before downstream masking, trimming, or HMM building.

## Guardrails

- Current installation missing libopenblas.so.0; may require environment repair
- Help text unavailable due to library loading error; rely on references/help.md
- Confirm HMMER package is fully installed and functional before use
- Options such as `--pcinfo`, `--psinfo`, `--iinfo`, and `--bpinfo` depend on specific alignment annotations and will fail if those annotations are absent

---
name: esl-alimanip
description: Use when manipulating multiple sequence alignment files using Easel tools from HMMER.
disable-model-invocation: true
user-invocable: true
---

# esl-alimanip

## Quick Start

- **Command:** `esl-alimanip`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/esl-alimanip`
- **Reference:** See `references/help.md` for full options and usage

## When To Use This Tool

- Use `esl-alimanip` when you need structural edits to an alignment that go beyond simple reformatting or column masking.
- It is intended for sequence removal/retention, reordering, trimming to subsequences, RF-related manipulations, annotation numbering, and other Stockholm/Pfam-centric alignment surgery.
- Use it when curating a multiple sequence alignment before HMM building or comparative analysis.
- In this environment it is currently blocked by a missing `libopenblas.so.0`, so treat the syntax below as documented behavior that cannot be executed until the library issue is fixed.

## Common Patterns

```bash
# Keep only sequences listed in a file
esl-alimanip --seq-k keep.txt alignment.sto > kept.sto

# Remove sequences listed in a file
esl-alimanip --seq-r remove.txt alignment.sto > filtered.sto

# Trim alignment sequences to subsequences from a companion file
esl-alimanip --trim subseqs.fa alignment.sto > trimmed.sto

# Add numbering over nongap RF columns
esl-alimanip --num-rf alignment.sto > numbered.sto
```

## Recommended Workflow

1. Verify the shared-library problem is resolved before relying on this tool in the current environment.
2. Choose one alignment-editing goal at a time: sequence keep/remove, trimming, reordering, RF/mask manipulation, or annotation conversion.
3. Apply the relevant option set to the source Stockholm/Pfam alignment and write to a new file rather than in place.
4. Validate the edited alignment with downstream Easel tools before further analysis.

## Guardrails

- Ensure shared library dependencies (libopenblas) are available in the environment
- Consult `references/help.md` for supported alignment formats and options
- Verify alignment integrity after any manipulation operation
- Many higher-level options depend on Stockholm/Pfam markup such as `#=GC RF`, `#=GR POST`, or per-sequence GS tags; absent annotation will make those modes fail

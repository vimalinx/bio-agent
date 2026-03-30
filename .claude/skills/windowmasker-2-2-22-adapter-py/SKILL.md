---
name: windowmasker-2-2-22-adapter-py
description: Use when adapting or converting WindowMasker output files for compatibility with different BLAST pipeline versions or formats.
disable-model-invocation: true
user-invocable: true
---

# windowmasker-2-2-22-adapter-py

## Quick Start
- **Command:** `windowmasker_2.2.22_adapter.py [--print-only] /path/to/windowmasker <old-style-options>`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/windowmasker_2.2.22_adapter.py`
- **Full reference:** See `references/help.md`

## When To Use This Tool

- Translate historical WindowMasker 2.2.22-era command lines into the newer option style.
- Preserve old pipeline invocations while moving to a newer `windowmasker` binary.
- Preview the translated command with `--print-only` before executing it.
- Handle old `mask`, `-mk_counts true`, and `-convert true` style invocations without manually rewriting every option.

## Common Patterns

```bash
# 1) Print the translated command without running it
windowmasker_2.2.22_adapter.py \
  --print-only \
  /home/vimalinx/miniforge3/envs/bio/bin/windowmasker \
  -mk_counts true \
  -in genome.fa \
  -out counts.obinary
```

```bash
# 2) Translate and execute an old masking command
windowmasker_2.2.22_adapter.py \
  /home/vimalinx/miniforge3/envs/bio/bin/windowmasker \
  -ustat counts.obinary \
  -in genome.fa \
  -out intervals.txt \
  -outfmt interval
```

```bash
# 3) Translate an old convert-mode command
windowmasker_2.2.22_adapter.py \
  --print-only \
  /home/vimalinx/miniforge3/envs/bio/bin/windowmasker \
  -convert true \
  -in wm.out \
  -out converted.out
```

## Recommended Workflow

1. Treat this as a migration helper for old WindowMasker command lines, not as a primary masking tool.
2. Start with `--print-only` and compare the translated command to the current `windowmasker -help` output.
3. Keep the actual `windowmasker` executable path explicit; the adapter passes it through unchanged.
4. Once translation looks correct, run the real `windowmasker` command or let the adapter execute it for you.

## Guardrails

- This script uses Python 2 syntax; in the current workspace it fails under Python 3, and `python2` is not available on PATH.
- The first non-flag argument must be the target `windowmasker` executable; the adapter does not discover it for you.
- `--print-only` is the safe default because the adapter will otherwise execute the translated command via `os.system`.
- The adapter silently drops or preserves old options based on mode (`mask`, `mk_counts`, or `convert`), so always inspect the translated command before trusting it.
- If you are already on a modern pipeline, prefer calling `windowmasker` directly instead of introducing this compatibility shim.

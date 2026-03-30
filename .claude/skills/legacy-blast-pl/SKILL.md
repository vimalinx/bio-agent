---
name: legacy-blast-pl
description: Use when converting NCBI C toolkit BLAST command lines to NCBI C++ toolkit equivalents.
disable-model-invocation: true
user-invocable: true
---

# legacy-blast-pl

## Quick Start
- **Command:** `legacy_blast.pl <legacy_program> <legacy_args> [--print_only] [--path /path/to/blast/bin]`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/legacy_blast.pl`
- **Full reference:** See `references/help.md`

## When To Use This Tool

- Translate old NCBI C toolkit BLAST command lines into BLAST+ / C++ toolkit equivalents.
- Preserve historical reproducibility when old pipeline logs mention `blastall`, `formatdb`, `fastacmd`, or related legacy programs.
- Preview modern replacement commands with `--print_only` before executing them.
- Use it as a migration helper, not as a routine front end for new BLAST workflows.

## Common Patterns

```bash
# 1) Preview a blastall-to-BLAST+ translation
legacy_blast.pl \
  blastall -p blastp -i query.fa -d nr -e 1e-5 \
  --print_only \
  --path /home/vimalinx/miniforge3/envs/bio/bin
```

```bash
# 2) Preview a formatdb migration
legacy_blast.pl \
  formatdb -i proteins.fa -p T \
  --print_only \
  --path /home/vimalinx/miniforge3/envs/bio/bin
```

```bash
# 3) Execute the translated command directly
legacy_blast.pl \
  fastacmd -d nr -s NP_414543 \
  --path /home/vimalinx/miniforge3/envs/bio/bin
```

## Recommended Workflow

1. Identify the original legacy command exactly as it appeared in historical documentation or scripts.
2. Use `--print_only` first and review the translated BLAST+ command for semantic drift.
3. Point `--path` at the BLAST+ binaries you actually want to use on this machine.
4. Replace the old command permanently once the translated command has been validated on a small example.

## Guardrails

- Script-level options such as `--print_only` and `--path` must use double dashes and appear at the end of the legacy command line.
- The default binary path is `/usr/bin`, which is usually wrong in this workspace; prefer `--path /home/vimalinx/miniforge3/envs/bio/bin`.
- Supported legacy applications are limited to the ones hard-coded in the script, including `blastall`, `megablast`, `blastpgp`, `bl2seq`, `rpsblast`, `fastacmd`, `formatdb`, and `seedtop`.
- Translation is not guaranteed to be biologically identical; inspect the generated command, especially filtering, scoring, and formatting options.
- `--version` only works as the first and only argument to the script.

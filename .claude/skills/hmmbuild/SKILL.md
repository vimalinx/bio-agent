---
name: hmmbuild
description: Use when turning curated multiple-sequence alignments into profile HMM files for HMMER search or database-preparation workflows.
disable-model-invocation: true
user-invocable: true
---

# hmmbuild

## Quick Start
- **Command:** `hmmbuild [options] <hmm_out> <msa_file>`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/hmmbuild`
- **Package:** HMMER 3.4
- **Reference:** See `references/help.md` for the current startup failure; option details below are grounded in the local man page

## When To Use This Tool

- Build a profile HMM from a curated multiple-sequence alignment.
- Create the model that will later be searched with `hmmsearch`.
- Turn seed alignments into reusable family or domain detectors.
- Use only when the alignment quality is good enough to justify a model.

## Common Patterns

```bash
# Build a profile HMM from one curated alignment
hmmbuild kinase.hmm kinase_alignment.sto
```

```bash
# Force nucleotide alphabet when autodetection would be ambiguous
hmmbuild --dna dna_family.hmm dna_alignment.sto
```

```bash
# Save the annotated Stockholm alignment that hmmbuild actually used
hmmbuild -O annotated.sto family.hmm seed_alignment.sto
```

```bash
# Name a single model explicitly
hmmbuild -n KinaseDomain kinase.hmm kinase_alignment.sto
```

## Recommended Workflow

1. Start from a real multiple-sequence alignment, not raw unaligned FASTA.
2. Inspect the alignment for bad fragments, frameshifts, or unrelated sequences before model building.
3. Decide whether consensus columns should be inferred automatically (`--fast`, default) or taken from reference annotation (`--hand`).
4. Build the HMM, and optionally capture the annotated Stockholm alignment with `-O` so you can review weights and chosen consensus columns.
5. Test the resulting model with `hmmsearch` or `hmmstat`, then run `hmmpress` if the model will become part of a scan database.

## Guardrails

- The input must be an alignment, not a bag of unaligned sequences.
- Garbage in, garbage out: poor alignment quality produces misleading models.
- On this workstation, the current local binary is presently failing with a missing `libopenblas.so.0`; use the local man page conservatively until that library issue is fixed.
- `msa_file` may be `-` to read from stdin, but `hmm_out` cannot be `-` because stdout is used for other textual output.
- `-n` only applies when building a single alignment; with multi-alignment input, each alignment needs its own annotated name.
- `--hand` relies on reference annotation already present in the alignment.
- Keep model validation separate from model construction so thresholds can be tuned honestly.

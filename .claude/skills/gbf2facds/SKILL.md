---
name: gbf2facds
description: Use when converting GenBank format files to FASTA coding sequences (CDS) for downstream sequence analysis.
disable-model-invocation: true
user-invocable: true
---

# gbf2facds

## Quick Start

- **Command:** `gbf2facds -na < records.gbf > cds.fna`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/gbf2facds`
- **Reference:** See `references/help.md` for detailed usage

## When To Use This Tool

- Extract CDS sequences from GenBank flatfiles in FASTA form.
- Choose nucleotide CDS output (`-na`) or translated protein output (`-aa`) from the same GenBank input.
- Flatten GenBank CDS annotations into FASTA records for downstream alignment, clustering, or annotation QC.

## Common Patterns

```bash
# 1) Extract nucleotide CDS sequences
gbf2facds -na < records.gbf > cds.fna
```

```bash
# 2) Extract translated CDS protein sequences
gbf2facds -aa < records.gbf > cds.faa
```

## Recommended Workflow

1. Prepare GenBank format input files
2. Pick `-na` for nucleotide CDS or `-aa` for protein translation output.
3. Run `gbf2facds` on a representative sample and inspect the FASTA headers.
4. Use extracted CDS for downstream bioinformatics analyses

## Guardrails

- `--help` and `--version` are rejected as unrecognized arguments; the only real switches are the nucleotide/protein selectors.
- The wrapper depends on `gbf2info` and `xtract`, so the broader EDirect toolchain must be on `PATH`.
- FASTA headers include accession, protein_id, gene, product, location, and `gbkey`, so downstream parsers should expect metadata-rich headers rather than bare accessions.

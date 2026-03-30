---
name: get-species-taxids-sh
description: Use when resolving taxonomy names or taxids into BLAST-filterable NCBI taxonomy IDs with the NCBI helper script.
disable-model-invocation: true
user-invocable: true
---

# get-species-taxids-sh

## Quick Start

- **Command:** `get_species_taxids.sh`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/get_species_taxids.sh`
- **Full reference:** [references/help.md](references/help.md)

## When To Use This Tool

- Retrieving taxonomy IDs at or below a specified taxonomy rank using `-t <taxonomy ID>`
- Looking up taxonomy information for an organism using `-n <Scientific Name, Common Name or Keyword>`

## Common Patterns

```bash
# 1) Expand a taxid to all taxids at or below that taxonomy level
PATH=/home/vimalinx/miniforge3/envs/bio/bin:$PATH \
  /home/vimalinx/miniforge3/envs/bio/bin/get_species_taxids.sh -t 9606
```

```bash
# 2) Search taxonomy by scientific or common name
PATH=/home/vimalinx/miniforge3/envs/bio/bin:$PATH \
  /home/vimalinx/miniforge3/envs/bio/bin/get_species_taxids.sh -n "human"
```

## Recommended Workflow

1. Identify the target organism or taxonomic group by scientific name, common name, or keyword.
2. Use `-n` to search and confirm the correct taxonomy entry.
3. Use `-t` with the confirmed taxonomy ID to retrieve all taxids at or below that level.
4. Use the resulting taxid list to filter downstream BLAST database queries.

## Guardrails

- The real executable uses underscores: `get_species_taxids.sh`.
- Dependency checks run before normal usage output. In a shell where `esearch`, `efetch`, and `esummary` are not on `PATH`, even a no-argument run fails before showing help.
- `-t` and `-n` are mutually exclusive.
- `-t` returns sorted taxids, while `-n` emits a formatted taxonomy summary rather than a bare taxid list.

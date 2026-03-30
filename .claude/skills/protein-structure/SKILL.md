---
name: protein-structure
description: Use when planning or staging protein-structure prediction or structure-design work in this workspace, especially when deciding between missing local predictors and the repos that are actually present.
allowed-tools:
  - Read
  - Write
  - Bash(python:*)
  - Bash(docker:*)
context: fork
agent: general-purpose
---

# protein-structure

Workspace-level gateway for structure-oriented work. In this repo, the strongest local assets are the checked-out `RFdiffusion` and `evo2` repositories plus Docker, not a ready-to-run AlphaFold/ColabFold desktop stack.

## Quick Start

- **Available local assets:** `/home/vimalinx/Projects/bio_studio/repositories/active/RFdiffusion`, `/home/vimalinx/Projects/bio_studio/repositories/active/evo2`, `/usr/bin/docker`
- **Fast availability check:** `command -v colabfold_batch pymol chimera chimerax foldseek mmseqs fpocket`
- **Current practical path:** use repo-backed Docker workflows rather than assuming local GUI prediction tools exist

## When To Use This Tool

- Deciding how to approach a protein-structure task in this workspace
- Routing between structure design (`RFdiffusion`) and sequence-model analysis (`evo2`)
- Auditing whether local structure-prediction tools are actually installed before planning around them
- Staging follow-on structure workflows once prerequisites are satisfied

## Common Patterns

```bash
# Check which structure tools are really installed
command -v colabfold_batch pymol chimera chimerax foldseek mmseqs fpocket
```

```bash
# Use the local RFdiffusion repo for generative design
cd /home/vimalinx/Projects/bio_studio/repositories/active/RFdiffusion
./test_rfdiffusion.sh
```

```bash
# Inspect the local Evo 2 repo for sequence-model-based analysis
cd /home/vimalinx/Projects/bio_studio/repositories/active/evo2
python examples/run_evo2.py
```

## Recommended Workflow

1. Verify the required predictor or viewer is actually present before promising a structure workflow.
2. If you need generative backbone or binder design, start from the local `RFdiffusion` repo.
3. If you need sequence-model scoring or embeddings on DNA-scale inputs, evaluate whether Evo 2 is the right supporting asset.
4. Install missing prediction/visualization tools explicitly before planning around ColabFold, PyMOL, or Chimera-based steps.

## Guardrails

- `colabfold_batch`, `pymol`, `chimera`, `chimerax`, `foldseek`, `mmseqs`, and `fpocket` are not currently on `PATH` in this workspace.
- `RFdiffusion` is present locally, but its Docker image is not prebuilt yet.
- The local Evo 2 repo exists, but direct `import evo2` currently fails because `vortex` is missing.
- Do not present RFdiffusion as a native fold-prediction replacement; it is primarily a generative structure-design workflow.

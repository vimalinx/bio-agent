---
name: rfdiffusion
description: Use when working from the local RFdiffusion repository to generate protein backbones or binder designs through its Docker Compose workflows.
allowed-tools: Bash
---

# rfdiffusion

Workspace-local gateway for `/home/vimalinx/Projects/bio_studio/repositories/active/RFdiffusion`. The repo contains a Chinese quickstart, `test_rfdiffusion.sh`, `design_ebola_binder.sh`, a populated `models/` directory, and Docker/Compose entrypoints for inference.

## Quick Start

- **Repository:** `/home/vimalinx/Projects/bio_studio/repositories/active/RFdiffusion`
- **Primary smoke test:** `./test_rfdiffusion.sh`
- **Primary build step:** `docker compose build`

## When To Use This Tool

- Running RFdiffusion locally from the checked-out workspace repo
- Generating monomer or binder backbones with the repo's inference script
- Reusing the bundled `models/` directory and test harness
- Exploring the repo's Ebola binder design example

## Common Patterns

```bash
# Build the RFdiffusion container stack
cd /home/vimalinx/Projects/bio_studio/repositories/active/RFdiffusion
docker compose build
```

```bash
# Run the repo's built-in smoke test
cd /home/vimalinx/Projects/bio_studio/repositories/active/RFdiffusion
./test_rfdiffusion.sh
```

```bash
# Run direct inference through the repo's compose service
docker compose run --rm --entrypoint /bin/bash rfdiffusion -c \
  "python3 scripts/run_inference.py 'contigmap.contigs=[150-150]' inference.output_prefix=outputs/test_run/test inference.num_designs=1 inference.model_directory_path=/app/RFdiffusion/models inference.input_pdb=/app/RFdiffusion/examples/input_pdbs/1qys.pdb"
```

## Recommended Workflow

1. Work from the local RFdiffusion repo rather than stale absolute paths copied from older notes.
2. Build the Docker/Compose environment first.
3. Run `./test_rfdiffusion.sh` before attempting custom binder or motif jobs.
4. Only move on to custom scripts like `design_ebola_binder.sh` after the compose test succeeds.

## Guardrails

- Docker images are not prebuilt in this workspace. `docker image inspect rfdiffusion` failed with `No such image: rfdiffusion:latest`.
- The quickstart document still references `/media/vimalinx/Data/bio_studio/RFdiffusion`; the actual workspace repo is under `/home/vimalinx/Projects/bio_studio/repositories/active/RFdiffusion`.
- The quickstart notes GPU memory around `8GB+` for binder design.
- `test_rfdiffusion.sh` depends on Docker Compose and the repo's `models/` directory layout.
- RFdiffusion is a generative structure-design tool, not a drop-in sequence-to-structure predictor.

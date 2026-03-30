---
name: phage-design
description: Use when working from the local Evo 2 `phage_gen` project to design or analyze bacteriophage genomes, competition assays, or Gibson assembly fragments.
allowed-tools:
  - Read
  - Write
  - Bash(python:*)
  - Bash(docker:*)
context: fork
agent: bio-expert
---

# phage-design

Project-specific gateway for `/home/vimalinx/Projects/bio_studio/repositories/active/evo2/phage_gen`. The local repo contains pipeline scripts, analysis utilities, environment YAMLs, and reference data for phage genome design, especially the genome design filtering workflow described in the subproject README.

## Quick Start

- **Project root:** `/home/vimalinx/Projects/bio_studio/repositories/active/evo2/phage_gen`
- **Main pipeline script:** `pipelines/genome_design_filtering_pipeline.py`
- **Main config template:** `pipelines/genome_design_filtering_pipeline_config_template.yaml`

## When To Use This Tool

- Running the local phage genome design filtering project
- Analyzing phage competition experiments or designing Gibson assembly fragments
- Working with the PhiX174 reference assets bundled in `phage_gen/data/`
- Preparing phage-design experiments that depend on the Evo 2 local repo

## Common Patterns

```bash
# Enter the local phage_gen project
cd /home/vimalinx/Projects/bio_studio/repositories/active/evo2/phage_gen
```

```bash
# Copy the config template, edit it, then run the Python pipeline directly
cp pipelines/genome_design_filtering_pipeline_config_template.yaml my_run.yaml
python pipelines/genome_design_filtering_pipeline.py my_run.yaml
```

```bash
# Run downstream analysis utilities
python analysis/competition_analysis.py
python analysis/genome_gibson_assembly.py
```

## Recommended Workflow

1. Start from the `phage_gen` subproject, not from generic phage-design prose.
2. Read the local README and choose the relevant mode: genome-design filtering, competition analysis, Gibson assembly, or architecture visualization.
3. Copy and edit the bundled config template before launching the main pipeline.
4. Prepare the matching conda environments from `environments/` if you want the full workflow rather than just code inspection.

## Guardrails

- The bundled `genome_design_filtering_pipeline.sh` is a Slurm template with literal `/path/to/...` placeholders. It is not runnable as-is.
- The local README says you need conda environments derived from `environments/genome_design.yaml` and `environments/genome_visualization.yaml`.
- This project is a phage-genome design subproject inside the Evo 2 repo, so any deeper Evo 2 runtime issues still apply.
- Treat the bundled PhiX174 reference files and cited paper as examples/reference assets, not as proof that every target-host phage workflow is turnkey.

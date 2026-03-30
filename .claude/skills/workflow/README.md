# Workflow Skills

Workflow skills compose multiple atomic skills into a reusable task template.

## Use This Layer For

- RNA-seq workflow skeletons
- sequence search and annotation flows
- structure analysis and design flows

## Not For

- freeform orchestration across unrelated tasks
- single-tool wrappers
- policy and review checkpoints

## Design Rule

Workflow skills should define stage structure and candidate skill sets, but they should not own final routing authority. The orchestrator layer decides how and when the workflow is used.

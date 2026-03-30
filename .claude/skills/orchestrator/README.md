# Orchestrator Skills

Orchestrator skills are the control-plane layer of the Bio Skill System.

## Responsibilities

- normalize requests
- generate candidate plans
- compare or revise plans
- route stages to skill sets
- decide when to pause
- validate stage completion
- resume interrupted runs

## Design Rule

These skills should not do heavy domain execution themselves. Their job is to control decision flow, not to replace atomic or workflow skills.

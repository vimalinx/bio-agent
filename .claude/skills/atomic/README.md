# Atomic Skills

Atomic skills are the smallest executable units in the Bio Skill System.

## Use This Layer For

- A single CLI wrapper
- A single transformation step
- A single validation step with a narrow boundary

## Required Contract

Every atomic skill should declare:

- expected inputs
- expected outputs
- preconditions
- side effects
- whether user confirmation is required

## Default Rule

Legacy flat skills under `.claude/skills/<skill-name>/SKILL.md` are treated as `atomic` unless an explicit override or layered path says otherwise.

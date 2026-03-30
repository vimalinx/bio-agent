---
name: project-tree-builder
description: Use when generating or dry-running NCBI-style Unix C++ project trees with `project_tree_builder`.
disable-model-invocation: true
user-invocable: true
---

# project-tree-builder

Compiled NCBI project-tree builder shipped inside the BLAST package. The live `-help` output documents a three-argument interface around `<root> <subtree> <solution>` plus build-tree options such as `-dryrun`, `-extroot`, `-projtag`, `-dtdep`, and `-libdep`.

## Quick Start

- **Command:** `project_tree_builder <root> <subtree> <solution>`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/project_tree_builder`
- **Observed version:** `4.12.3` from BLAST `2.17.0`

## When To Use This Tool

- Generating NCBI C++ Toolkit-style Unix project trees
- Previewing a project-tree build with `-dryrun` before touching files
- Restricting tree generation to selected project tags or subtree lists
- Toggling dependency-analysis behavior for external or datatool-related builds

## Common Patterns

```bash
# Preview a tree build without making changes
project_tree_builder -dryrun /path/to/c++ src/corelib/ MySolution
```

```bash
# Limit generation to selected project tags
project_tree_builder -projtag 'core && !demo' /path/to/c++ src/corelib/ MySolution
```

```bash
# Read arguments from a file
project_tree_builder -args tree_builder.args /path/to/c++ src/corelib/ MySolution
```

## Recommended Workflow

1. Identify the NCBI-style C++ root, subtree (or subtree list file), and solution name you actually want to build.
2. Start with `-dryrun` so preconditions are checked before generating anything.
3. Add dependency or external-library switches only after the plain dry run looks correct.
4. Capture logs with `-logfile` if you need a reproducible record of the generation step.

## Guardrails

- The live help states that `root` should end with `c++`.
- `subtree` can be either a subtree path or a file containing a list of subtrees.
- `solution` is required even though this is the Unix tree builder; do not omit it.
- Single-dash control flags are the real interface here: `-h`, `-help`, `-version`, `-version-full`, `-dryrun`, etc.
- Live testing showed `project_tree_builder -dryrun . src/corelib test` could exit silently with status `0`, so lack of output is not proof that it did meaningful work.
- `-libdep` is typed as a Boolean in the help text and defaults to `true`.

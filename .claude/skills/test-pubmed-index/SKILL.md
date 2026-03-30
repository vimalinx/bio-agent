---
name: test-pubmed-index
description: Use when validating a local PubMed archive/postings installation configured through `EDIRECT_LOCAL_ARCHIVE` and related local EDirect helpers.
disable-model-invocation: true
user-invocable: true
---

# test-pubmed-index

EDirect shell smoke test for a local PubMed archive and postings setup. It relies on `xcommon.sh` to locate archive/postings/data folders, round-trips random PubMed titles through `xfetch` and `xsearch`, prints field/term diagnostics with `xinfo`, performs a local `cit2pmid -local` lookup, and climbs a MeSH tree using `meshconv.xml`.

## Quick Start

- **Command:** `test-pubmed-index`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/test-pubmed-index`
- **Critical environment:** `EDIRECT_LOCAL_ARCHIVE`

## When To Use This Tool

- Validating a full local PubMed archive/postings/data installation
- Troubleshooting local `xfetch`, `xsearch`, `xinfo`, or `cit2pmid -local` behavior
- Checking whether the archive, postings, and auxiliary data folders are all discoverable through EDirect local configuration
- Running a deeper local PubMed check than a simple one-command query

## Common Patterns

```bash
# Run against a configured local archive root
export EDIRECT_LOCAL_ARCHIVE=/path/to/local/archive
test-pubmed-index
```

```bash
# Save diagnostics for later inspection
export EDIRECT_LOCAL_ARCHIVE=/path/to/local/archive
test-pubmed-index > pubmed-index-check.txt
```

```bash
# Time the run externally
export EDIRECT_LOCAL_ARCHIVE=/path/to/local/archive
time test-pubmed-index
```

## Recommended Workflow

1. Set `EDIRECT_LOCAL_ARCHIVE` to the correct local archive root.
2. Run `test-pubmed-index` with no arguments.
3. Read early errors first: archive/postings/data folder failures usually make the later checks meaningless.
4. Only interpret the title-roundtrip and MeSH-tree sections after the environment-location steps succeed.

## Guardrails

- The script has no real help/version parser. `-h` and `--version` were treated like a normal run and triggered the full error cascade.
- Without `EDIRECT_LOCAL_ARCHIVE`, local testing produced repeated path errors, `Unable to get folder Postings for database pubmed`, `Unable to get folder Archive for database pubmed`, and `cat: /meshconv.xml: No such file or directory`.
- Source inspection shows the script depends on sibling helpers from `xcommon.sh`, especially `FindArchiveFolder`, `FindPostingsFolder`, and `FindDataFolder`.
- This is a broad local-environment smoke test, not a clean pass/fail API checker, so misconfiguration can surface as noisy mixed errors.

---
name: seq-cache-populate-pl
description: Use when populating an htslib/CRAM `REF_CACHE` directory from FASTA input or by scanning a directory tree for FASTA files.
disable-model-invocation: true
user-invocable: true
---

# seq-cache-populate-pl

Perl cache builder for htslib reference caching. It reads FASTA entries, uppercases and whitespace-strips the sequence, hashes the normalized sequence by MD5, and writes each entry into a `REF_CACHE`-style directory tree under the chosen root.

## Quick Start

- **Command:** `seq_cache_populate.pl -root <dir> input1.fasta ...`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/seq_cache_populate.pl`
- **Main output:** populated cache tree plus a printed `REF_CACHE=...` template

## When To Use This Tool

- Building a CRAM-compatible reference cache from FASTA files
- Precomputing MD5-keyed reference paths before `samtools`, `htslib`, or CRAM workflows
- Scanning a directory tree for FASTA-like files with `-find`
- Reusing an existing cache root and skipping entries that are already present

## Common Patterns

```bash
# Populate a cache from one FASTA file
seq_cache_populate.pl -root ref_cache reference.fa
```

```bash
# Scan a directory tree for FASTA-like files
seq_cache_populate.pl -root ref_cache -find refs/
```

```bash
# Use a deeper hash directory layout
seq_cache_populate.pl -root ref_cache -subdirs 15 reference.fa
```

## Recommended Workflow

1. Pick a cache root that downstream CRAM tools can read consistently.
2. Choose direct FASTA arguments, `-find <dir>`, or stdin if you want to stream one FASTA file through the script.
3. Run the script and capture the printed `REF_CACHE=...` template.
4. Export that `REF_CACHE` value in later `samtools` / `htslib` jobs that need reference lookup by MD5.

## Guardrails

- `-root <dir>` is mandatory. With no arguments, the script prints only the usage banner.
- The tool is a normal Perl script, so its only built-in usage path is the Perl `GetOptions` failure / missing-argument banner; there is no separate `--version`.
- Live testing showed cache entries created under MD5-derived hex paths such as `cache/f1/f8/f4bf...`, followed by a printed `Use environment REF_CACHE=.../%2s/%2s/%s`.
- Re-running against the same FASTA does not duplicate entries; it prints `Already exists: <md5> <seqid>` instead.
- `-find` only accepts candidate files whose first line looks like `>id` and whose second line matches a nucleotide alphabet regex.
- Source inspection shows `-subdirs 16` is rejected, but the error text misleadingly says it “should be less than 15”; local testing confirmed `-subdirs 15` still works.
- Large sequences spill to temporary files once buffered sequence length exceeds roughly `256 MiB`, and those temporary files are created under the chosen cache root.

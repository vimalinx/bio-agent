# xfilter Help Reference

- Command: `xfilter`
- Sources: conda_bioconda
- Local executable: `/home/vimalinx/miniforge3/envs/bio/bin/xfilter`
- Summary: CLI installed by bioconda package entrez-direct.
- Package names: entrez-direct

## Captured Version

```text
$ xfilter --version
ERROR: Must supply path to local data by setting EDIRECT_LOCAL_ARCHIVE environment variable
ERROR: Unrecognized option --version
```

## Captured Help

```text
$ xfilter --help
xfilter 24.0

USAGE: xfilter
       -query
       query arguments

EXAMPLES

  xfilter -query "2020:2025 [YEAR]"

  xsearch -db pubmed -query "Hoffmann PC [AUTH]" |
  elink -related |
  xfilter -query "Dopamine [MESH] AND Deficiency [SUBH]" |
  efetch -format apa
```

## Captured Man Page

```text
No man page captured.
```

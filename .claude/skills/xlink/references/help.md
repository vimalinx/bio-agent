# xlink Help Reference

- Command: `xlink`
- Sources: conda_bioconda
- Local executable: `/home/vimalinx/miniforge3/envs/bio/bin/xlink`
- Summary: CLI installed by bioconda package entrez-direct.
- Package names: entrez-direct

## Captured Version

```text
$ xlink --version
ERROR: Must supply path to local data by setting EDIRECT_LOCAL_ARCHIVE environment variable
ERROR: Insufficient arguments given to xlink
```

## Captured Help

```text
$ xlink --help
xlink 24.0

USAGE: xlink
       -target
       link argument

EXAMPLES

  xsearch -db pubmed -query "Havran W* [AUTH]" |
  xlink -target CITED |
  xfilter -query "2020:2025 [YEAR]" |
  xfetch |
  xtract -pattern PubmedArticle -histogram Journal/ISOAbbreviation |
  sort-table -nr |
  just-top-hits 10
```

## Captured Man Page

```text
No man page captured.
```

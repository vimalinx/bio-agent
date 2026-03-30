# xinfo Help Reference

- Command: `xinfo`
- Sources: conda_bioconda
- Local executable: `/home/vimalinx/miniforge3/envs/bio/bin/xinfo`
- Summary: CLI installed by bioconda package entrez-direct.
- Package names: entrez-direct

## Captured Version

```text
$ xinfo --version
ERROR: Must supply path to local data by setting EDIRECT_LOCAL_ARCHIVE environment variable
ERROR: Unrecognized option --version
```

## Captured Help

```text
$ xinfo --help
xinfo 24.0

USAGE: xinfo
       -count | -counts | -fields | -terms | -totals

EXAMPLES

  xinfo -db pubmed -fields

  xinfo -db pubmed -terms SUBH

  xinfo -db pubmed -count "catabolite repress*"

  xinfo -db pubmed -counts "catabolite repress*"

  xinfo -db pubmed -totals PROP

  xinfo -db pubmed -totals YEAR |
  print-columns '$2, $1, total += $1' |
  print-columns '$1, log($2)/log(10), log($3)/log(10)' |
  filter-columns '$1 >= 1800 && $1 < YR' |
  xy-plot annual-and-cumulative.png
```

## Captured Man Page

```text
No man page captured.
```

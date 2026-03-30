# xsearch Help Reference

- Command: `xsearch`
- Sources: conda_bioconda
- Local executable: `/home/vimalinx/miniforge3/envs/bio/bin/xsearch`
- Summary: CLI installed by bioconda package entrez-direct.
- Package names: entrez-direct

## Captured Version

```text
$ xsearch --version
ERROR: Must supply path to local data by setting EDIRECT_LOCAL_ARCHIVE environment variable
ERROR: Unrecognized option --version
```

## Captured Help

```text
$ xsearch --help
xsearch 24.0

USAGE: xsearch
       -query | -match | -exact | -title | -words | -pairs
       query arguments

EXAMPLES

  xsearch -query "(literacy AND numeracy) NOT (adolescent OR child)"

  xsearch -query "selective serotonin reuptake inhibit*"

  xsearch -query "vitamin c + + common cold"

  xsearch -query "vitamin c ~ ~ common cold"

  xsearch -query "C14.907.617.812* [TREE] AND 2015:2018 [YEAR]"

  xsearch -title "Genetic Control of Biochemical Reactions in Neurospora."

  xsearch -match "nucleotide sequences required for tn3 transposition immunity [PAIR]" |
  just-top-hits 1 | cut -f 2 |
  efetch -db pubmed -format abstract
```

## Captured Man Page

```text
No man page captured.
```

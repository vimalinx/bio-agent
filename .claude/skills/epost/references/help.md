# epost Help Reference

- Command: `epost`
- Sources: conda_bioconda
- Local executable: `/home/vimalinx/miniforge3/envs/bio/bin/epost`
- Summary: CLI installed by bioconda package entrez-direct.
- Package names: entrez-direct

## Captured Version

```text
$ epost --version
ERROR:  Unrecognized option --version
```

## Captured Help

```text
$ epost --help
epost 24.0

  -db        Database name
  -id        Unique identifier(s) or accession number(s)
  -format    uid or acc
  -input     Read identifier(s) from file instead of stdin

Examples

  echo 3OQZ_a | epost -db protein | efetch -format fasta

  epost -db protein -id 3OQZ_a | efetch -format fasta

  efetch -db protein -id 3OQZ_a -format fasta


  echo GCF_000001405.38 | epost -db assembly | efetch -format docsum

  epost -db assembly -id GCF_000001405.38 | efetch -format docsum

  efetch -db assembly -id GCF_000001405.38 -format docsum


  echo PRJNA257197 | epost -db bioproject | efetch -format docsum

  epost -db bioproject -id PRJNA257197 | efetch -format docsum

  efetch -db bioproject -id PRJNA257197 -format docsum
```

## Captured Man Page

```text
No man page captured.
```

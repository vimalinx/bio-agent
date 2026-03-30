# ace2sam Help Reference

- Command: `ace2sam`
- Sources: conda_bioconda
- Local executable: `/home/vimalinx/miniforge3/envs/bio/bin/ace2sam`
- Summary: CLI installed by bioconda package samtools.
- Package names: samtools

## Captured Version

```text
$ ace2sam --version
ace2sam: invalid option -- '-'
ace2sam: invalid option -- 'v'
ace2sam: invalid option -- 'e'
ace2sam: invalid option -- 'r'
ace2sam: invalid option -- 's'
ace2sam: invalid option -- 'i'
ace2sam: invalid option -- 'o'
ace2sam: invalid option -- 'n'

Usage:   ace2sam [-pc] <in.ace>

Options: -p     output padded SAM
         -c     write the contig sequence in SAM

Notes: 1. Fields must appear in the following order: (CO->[BQ]->(AF)->(RD->QA))
       2. The order of reads in AF and in RD must be identical
       3. Except in BQ, words and numbers must be separated by a single SPACE or TAB
       4. This program writes the headerless SAM to stdout and header to stderr
```

## Captured Help

```text
$ ace2sam --help
ace2sam: invalid option -- '-'
ace2sam: invalid option -- 'h'
ace2sam: invalid option -- 'e'
ace2sam: invalid option -- 'l'

Usage:   ace2sam [-pc] <in.ace>

Options: -p     output padded SAM
         -c     write the contig sequence in SAM

Notes: 1. Fields must appear in the following order: (CO->[BQ]->(AF)->(RD->QA))
       2. The order of reads in AF and in RD must be identical
       3. Except in BQ, words and numbers must be separated by a single SPACE or TAB
       4. This program writes the headerless SAM to stdout and header to stderr
```

## Captured Man Page

```text
No man page captured.
```

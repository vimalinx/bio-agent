# export2sam-pl Help Reference

- Command: `export2sam.pl`
- Sources: conda_bioconda
- Local executable: `/home/vimalinx/miniforge3/envs/bio/bin/export2sam.pl`
- Summary: CLI installed by bioconda package samtools.
- Package names: samtools

## Captured Version

```text
$ export2sam.pl --version
export2sam.pl version: 2.3.1
```

## Captured Help

```text
$ export2sam.pl --help
export2sam.pl converts GERALD export files to SAM format.

Usage: export2sam.pl --read1=FILENAME [ options ] | --version | --help

  --read1=FILENAME  read1 export file or '-' for stdin (mandatory)
                      (file may be gzipped with ".gz" extension)
  --read2=FILENAME  read2 export file or '-' for stdin
                      (file may be gzipped with ".gz" extension)
  --nofilter        include reads that failed the basecaller
                      purity filter
  --qlogodds        assume export file(s) use logodds quality values
                      as reported by OLB (Pipeline) prior to v1.3
                      (default: phred quality values)
```

## Captured Man Page

```text
No man page captured.
```

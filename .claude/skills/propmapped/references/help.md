# propmapped Help Reference

- Command: `propmapped`
- Sources: conda_bioconda
- Local executable: `/home/vimalinx/miniforge3/envs/bio/bin/propmapped`
- Summary: CLI installed by bioconda package subread.
- Package names: subread

## Captured Version

```text
$ propmapped --version
propmapped: unrecognized option '--version'

propMapped v2.1.1

  Calculate the proportion of mapped reads/fragments.

Usage:

  ./prommapped [options] -i <file>

Required arguments:

  -i <string>  An input file containing read mapping results. Both SAM or BAM
               formats are supported.

Optional arguments:

  -o <string>  Name of output file including mapping statistics.

  -f           If specified, fragments (read pairs) will be counted instead of
               individual reads. This option is only applicable for paired-end
               reads.

  -p           If specified, only properly paired reads will be counted. This
               option is only applicable for paired-end reads.
```

## Captured Help

```text
$ propmapped --help
propmapped: unrecognized option '--help'

propMapped v2.1.1

  Calculate the proportion of mapped reads/fragments.

Usage:

  ./prommapped [options] -i <file>

Required arguments:

  -i <string>  An input file containing read mapping results. Both SAM or BAM
               formats are supported.

Optional arguments:

  -o <string>  Name of output file including mapping statistics.

  -f           If specified, fragments (read pairs) will be counted instead of
               individual reads. This option is only applicable for paired-end
               reads.

  -p           If specified, only properly paired reads will be counted. This
               option is only applicable for paired-end reads.
```

## Captured Man Page

```text
No man page captured.
```

# repair Help Reference

- Command: `repair`
- Sources: conda_bioconda
- Local executable: `/home/vimalinx/miniforge3/envs/bio/bin/repair`
- Summary: CLI installed by bioconda package subread.
- Package names: subread

## Captured Version

```text
$ repair --version
repair: invalid option -- '-'

repair Version 2.1.1

  Find reads that are from the same pair in the input and then place them next
to each other in the output. A dummy read is added for each singleton read
that does not have a pair. The output file is compatible with featureCounts
program.

Usage:

  ./repair [options] -i <input_file> -o <output_file>


Required arguments:

  -i <string>  Name of input file. BAM format by default.

  -o <string>  Name of output file. The output file is in BAM format.

Optional arguments:

  -S           The input file is in SAM format.

  -c           Compress the output BAM file. This will reduce the size of BAM
               file, but will increase the time of retrieving reads from BAM
               file.

  -T <int>     Number of CPU threads. 8 by default.

  -d           Do not add dummy reads for singleton reads.

  -t           Do not include sequences and quality scores of reads in the
               output file.
```

## Captured Help

```text
$ repair --help
repair: invalid option -- '-'

repair Version 2.1.1

  Find reads that are from the same pair in the input and then place them next
to each other in the output. A dummy read is added for each singleton read
that does not have a pair. The output file is compatible with featureCounts
program.

Usage:

  ./repair [options] -i <input_file> -o <output_file>


Required arguments:

  -i <string>  Name of input file. BAM format by default.

  -o <string>  Name of output file. The output file is in BAM format.

Optional arguments:

  -S           The input file is in SAM format.

  -c           Compress the output BAM file. This will reduce the size of BAM
               file, but will increase the time of retrieving reads from BAM
               file.

  -T <int>     Number of CPU threads. 8 by default.

  -d           Do not add dummy reads for singleton reads.

  -t           Do not include sequences and quality scores of reads in the
               output file.
```

## Captured Man Page

```text
No man page captured.
```

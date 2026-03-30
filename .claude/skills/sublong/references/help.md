# sublong Help Reference

- Command: `sublong`
- Sources: conda_bioconda
- Local executable: `/home/vimalinx/miniforge3/envs/bio/bin/sublong`
- Summary: CLI installed by bioconda package subread.
- Package names: subread

## Captured Version

```text
$ sublong --version
Sublong v2.1.1

Usage:

./sublong [options] -i <index_name> -r <input> -o <output>

## Mandatory arguments:

 -i <string>   Base name of the index. The index must be built as a full index
               and has only one block.

 -r <string>   Name of an input read file. Acceptable formats include gzipped
               FASTQ and FASTQ (automatically identified).

 -o <string>   Name of an output file in BAM format.

## Optional arguments:
# input reads and output

 --SAMoutput   Save mapping results in SAM format.

# number of CPU threads

 -T <int>      Number of CPU threads used. 1 by default.

# others

 -v            Output version of the program.

 -X            Turn on the RNA-seq mode.

Refer to Users Manual for detailed description to the arguments.


sublong: unrecognized option '--version'
```

## Captured Help

```text
$ sublong --help
Sublong v2.1.1

Usage:

./sublong [options] -i <index_name> -r <input> -o <output>

## Mandatory arguments:

 -i <string>   Base name of the index. The index must be built as a full index
               and has only one block.

 -r <string>   Name of an input read file. Acceptable formats include gzipped
               FASTQ and FASTQ (automatically identified).

 -o <string>   Name of an output file in BAM format.

## Optional arguments:
# input reads and output

 --SAMoutput   Save mapping results in SAM format.

# number of CPU threads

 -T <int>      Number of CPU threads used. 1 by default.

# others

 -v            Output version of the program.

 -X            Turn on the RNA-seq mode.

Refer to Users Manual for detailed description to the arguments.


sublong: unrecognized option '--help'
```

## Captured Man Page

```text
No man page captured.
```

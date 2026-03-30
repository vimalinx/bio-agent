# quality-scores Help Reference

- Command: `qualityScores`
- Sources: conda_bioconda
- Local executable: `/home/vimalinx/miniforge3/envs/bio/bin/qualityScores`
- Summary: CLI installed by bioconda package subread.
- Package names: subread

## Captured Version

```text
$ qualityScores --version
qualityScores: unrecognized option '--version'

qualityScore Version 2.1.1

  Retrieve Phred score for read bases

Usage:

  ./qualityScores [options] -i <input_file> -o <output_file>

Required arguments:

  -i <string>  Name of input file including read data. The default format is
               Fastq.

  -o <string>  Name of output file that is a text file including Phred scores
               for each read base.

Optional arguments:

  --gzFASTQinput Input file is in gzipped Fastq format.

  --BAMinput     Input file is in BAM format.

  --SAMinput     Input file is in SAM format.

  --first-end    Use only first reads in paired-end data. Only applicable for
                 paired-end BAM/SAM input.

  --second-end   Use only second reads in paired-end data. Only applicable for
                 paired-end BAM/SAM input.

  --counted-reads <int> Total number of reads to be extracted from the input
                 file. 10,000 by default.

  --phred-offset <33|64> refer to subread aligner.
```

## Captured Help

```text
$ qualityScores --help
qualityScores: unrecognized option '--help'

qualityScore Version 2.1.1

  Retrieve Phred score for read bases

Usage:

  ./qualityScores [options] -i <input_file> -o <output_file>

Required arguments:

  -i <string>  Name of input file including read data. The default format is
               Fastq.

  -o <string>  Name of output file that is a text file including Phred scores
               for each read base.

Optional arguments:

  --gzFASTQinput Input file is in gzipped Fastq format.

  --BAMinput     Input file is in BAM format.

  --SAMinput     Input file is in SAM format.

  --first-end    Use only first reads in paired-end data. Only applicable for
                 paired-end BAM/SAM input.

  --second-end   Use only second reads in paired-end data. Only applicable for
                 paired-end BAM/SAM input.

  --counted-reads <int> Total number of reads to be extracted from the input
                 file. 10,000 by default.

  --phred-offset <33|64> refer to subread aligner.
```

## Captured Man Page

```text
No man page captured.
```

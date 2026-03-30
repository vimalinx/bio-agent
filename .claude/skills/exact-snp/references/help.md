# exact-snp Help Reference

- Command: `exactSNP`
- Sources: conda_bioconda
- Local executable: `/home/vimalinx/miniforge3/envs/bio/bin/exactSNP`
- Summary: CLI installed by bioconda package subread.
- Package names: subread

## Captured Version

```text
$ exactSNP --version
exactSNP: unrecognized option '--version'

Version 2.1.1

Usage:

  ./exactSNP [options] -i input -g reference_genome -o output 

Required arguments:

  -i <file>  Specify name of an input file including read mapping results. The
 [-b if BAM] format of input file can be SAM or BAM (-b needs to be specified
             if a BAM file is provided).

  -g <file>  Specify name of the file including all reference sequences. Only
             one single FASTA format file should be provided.

  -o <file>  Specify name of the output file. This program outputs a VCF format
             file that includes discovered SNPs.

Optional arguments:

  -a <file>  Provide a set of annotated SNPs (e.g. SNPs included in the dbSNP
             database). The supplied file should be in VCF format (gzipped file
             is accepted). Providing known SNPs to the program should improve
             its SNP calling performance. Note that the provided SNPs may or
             may not be called.

  -b         Indicate the input file provided via -i is in BAM format.

  -Q <int>   Specify the q-value cutoff for SNP calling at sequencing depth of
             50X. 12 by default. The corresponding p-value cutoff is 10^(-1*Q).
             Note that this program automatically adjusts the q-value cutoff
             according to the sequencing depth at each chromosomal location.

  -f <float> Specify the minimum fraction of mis-matched bases a SNP-containing
             location must have. Its value must between 0 and 1. 0 by default.

  -n <int>   Specify the minimum number of mis-matched bases a SNP-containing
             location must have. 1 by default.

  -r <int>   Specify the minimum number of mapped reads a SNP-containing
             location must have (ie. the minimum coverage). 1 by default.

  -x <int>   Specify the maximum depth a SNP location is allowed to have.
             1,000,000 reads by default. This option is useful for removing PCR
             artefacts.

  -s <int>   Specify the minimum base quality scores (Phred scores) read bases
             must satisfy to be used for SNP calling. 13 by default. Read bases
             with quality scores less than 13 will be excluded from the
             analysis.

  -t <int>   Specify the number of bases trimmed off from each end of the read.
             3 by default.

  -T <int>   Specify the number of threads. 1 by default.

  -v         output version of the program.

  -C <path>  Specify the path to save the temporary files.

Example:

  ./exactSNP -i my-alignment.sam -g mm10.fa -o my-SNPs.txt
```

## Captured Help

```text
$ exactSNP --help
exactSNP: unrecognized option '--help'

Version 2.1.1

Usage:

  ./exactSNP [options] -i input -g reference_genome -o output 

Required arguments:

  -i <file>  Specify name of an input file including read mapping results. The
 [-b if BAM] format of input file can be SAM or BAM (-b needs to be specified
             if a BAM file is provided).

  -g <file>  Specify name of the file including all reference sequences. Only
             one single FASTA format file should be provided.

  -o <file>  Specify name of the output file. This program outputs a VCF format
             file that includes discovered SNPs.

Optional arguments:

  -a <file>  Provide a set of annotated SNPs (e.g. SNPs included in the dbSNP
             database). The supplied file should be in VCF format (gzipped file
             is accepted). Providing known SNPs to the program should improve
             its SNP calling performance. Note that the provided SNPs may or
             may not be called.

  -b         Indicate the input file provided via -i is in BAM format.

  -Q <int>   Specify the q-value cutoff for SNP calling at sequencing depth of
             50X. 12 by default. The corresponding p-value cutoff is 10^(-1*Q).
             Note that this program automatically adjusts the q-value cutoff
             according to the sequencing depth at each chromosomal location.

  -f <float> Specify the minimum fraction of mis-matched bases a SNP-containing
             location must have. Its value must between 0 and 1. 0 by default.

  -n <int>   Specify the minimum number of mis-matched bases a SNP-containing
             location must have. 1 by default.

  -r <int>   Specify the minimum number of mapped reads a SNP-containing
             location must have (ie. the minimum coverage). 1 by default.

  -x <int>   Specify the maximum depth a SNP location is allowed to have.
             1,000,000 reads by default. This option is useful for removing PCR
             artefacts.

  -s <int>   Specify the minimum base quality scores (Phred scores) read bases
             must satisfy to be used for SNP calling. 13 by default. Read bases
             with quality scores less than 13 will be excluded from the
             analysis.

  -t <int>   Specify the number of bases trimmed off from each end of the read.
             3 by default.

  -T <int>   Specify the number of threads. 1 by default.

  -v         output version of the program.

  -C <path>  Specify the path to save the temporary files.

Example:

  ./exactSNP -i my-alignment.sam -g mm10.fa -o my-SNPs.txt
```

## Captured Man Page

```text
No man page captured.
```

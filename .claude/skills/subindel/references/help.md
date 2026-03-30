# subindel Help Reference

- Command: `subindel`
- Sources: conda_bioconda
- Local executable: `/home/vimalinx/miniforge3/envs/bio/bin/subindel`
- Summary: CLI installed by bioconda package subread.
- Package names: subread

## Captured Version

```text
$ subindel --version
SubIndel: detect short and long indels

Usage:
  subindel -i <SAM file> -g <subread index> -o <output VCF> {-d <expected fragment distance>} {-I <max indel length>} {--paired-end}

Example:
  subindel -i my_paired_end_reads.SAM -g my_index -o my_result -d 300 -I 200 --paired-end 


subindel: unrecognized option '--version'
```

## Captured Help

```text
$ subindel --help
SubIndel: detect short and long indels

Usage:
  subindel -i <SAM file> -g <subread index> -o <output VCF> {-d <expected fragment distance>} {-I <max indel length>} {--paired-end}

Example:
  subindel -i my_paired_end_reads.SAM -g my_index -o my_result -d 300 -I 200 --paired-end 


subindel: unrecognized option '--help'
```

## Captured Man Page

```text
No man page captured.
```

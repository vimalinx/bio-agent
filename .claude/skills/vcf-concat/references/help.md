# vcf-concat Help Reference

- Command: `vcf-concat`
- Sources: conda_bioconda
- Local executable: `/home/vimalinx/miniforge3/envs/bio/bin/vcf-concat`
- Summary: CLI installed by bioconda package vcftools.
- Package names: vcftools

## Captured Version

```text
$ vcf-concat --version
Unknown parameter "--version". Run -h for help.
 at /home/vimalinx/miniforge3/envs/bio/bin/vcf-concat line 32.
	main::error("Unknown parameter \"--version\". Run -h for help.\x{a}") called at /home/vimalinx/miniforge3/envs/bio/bin/vcf-concat line 73
	main::parse_params() called at /home/vimalinx/miniforge3/envs/bio/bin/vcf-concat line 11
```

## Captured Help

```text
$ vcf-concat --help
About: Convenience tool for concatenating VCF files (e.g. VCFs split by chromosome).
   In the basic mode it does not do anything fancy except for a sanity check that all
   files have the same columns.  When run with the -s option, it will perform a partial
   merge sort, looking at limited number of open files simultaneously.
Usage: vcf-concat [OPTIONS] A.vcf.gz B.vcf.gz C.vcf.gz > out.vcf
Options:
   -c, --check-columns              Do not concatenate, only check if the columns agree.
   -f, --files <file>               Read the list of files from a file.
   -p, --pad-missing                Write '.' in place of missing columns. Useful for joining chrY with the rest.
   -s, --merge-sort <int>           Allow small overlaps in N consecutive files.
   -h, -?, --help                   This help message.
```

## Captured Man Page

```text
No man page captured.
```

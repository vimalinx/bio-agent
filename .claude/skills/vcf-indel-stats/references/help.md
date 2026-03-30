# vcf-indel-stats Help Reference

- Command: `vcf-indel-stats`
- Sources: conda_bioconda
- Local executable: `/home/vimalinx/miniforge3/envs/bio/bin/vcf-indel-stats`
- Summary: CLI installed by bioconda package vcftools.
- Package names: vcftools

## Captured Version

```text
$ vcf-indel-stats --version
Unknown parameter "--version". Run -h for help.
 at /home/vimalinx/miniforge3/envs/bio/bin/vcf-indel-stats line 18.
	main::error("Unknown parameter \"--version\". Run -h for help.\x{a}") called at /home/vimalinx/miniforge3/envs/bio/bin/vcf-indel-stats line 41
	main::parse_params() called at /home/vimalinx/miniforge3/envs/bio/bin/vcf-indel-stats line 8
```

## Captured Help

```text
$ vcf-indel-stats --help
About: Currently calculates in-frame ratio.
Usage: vcf-indel-stats [OPTIONS] < in.vcf > out.txt
Options:
   -h, -?, --help                   This help message.
   -e, --exons <file>               Tab-separated file with exons (chr,from,to; 1-based, inclusive)
   -v, --verbose
```

## Captured Man Page

```text
No man page captured.
```

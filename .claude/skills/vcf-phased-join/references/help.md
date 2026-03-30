# vcf-phased-join Help Reference

- Command: `vcf-phased-join`
- Sources: conda_bioconda
- Local executable: `/home/vimalinx/miniforge3/envs/bio/bin/vcf-phased-join`
- Summary: CLI installed by bioconda package vcftools.
- Package names: vcftools

## Captured Version

```text
$ vcf-phased-join --version
Unknown parameter or non-existent file "--version". Run -h for help.
 at /home/vimalinx/miniforge3/envs/bio/bin/vcf-phased-join line 25.
	main::error("Unknown parameter or non-existent file \"--version\". Run -h fo"...) called at /home/vimalinx/miniforge3/envs/bio/bin/vcf-phased-join line 66
	main::parse_params() called at /home/vimalinx/miniforge3/envs/bio/bin/vcf-phased-join line 8
```

## Captured Help

```text
$ vcf-phased-join --help
About: The script takes multiple overlapping pre-phased chunks and concatenates them into one VCF
   using heterozygous calls from the overlaps to determine correct phase.
Usage: vcf-phased-join [OPTIONS] A.vcf B.vcf C.vcf
Options:
   -j, --min-join-quality <num>    Quality threshold for gluing the pre-phased blocks together [10]
   -l, --list <file>               List of VCFs to join.
   -o, --output <file>             Output file name. When "-" is supplied, STDOUT and STDERR will be used
   -q, --min-PQ <num>              Break pre-phased segments if PQ value is lower in input VCFs [0.6]
   -h, -?, --help                  This help message
```

## Captured Man Page

```text
No man page captured.
```

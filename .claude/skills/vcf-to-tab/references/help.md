# vcf-to-tab Help Reference

- Command: `vcf-to-tab`
- Sources: conda_bioconda
- Local executable: `/home/vimalinx/miniforge3/envs/bio/bin/vcf-to-tab`
- Summary: CLI installed by bioconda package vcftools.
- Package names: vcftools

## Captured Version

```text
$ vcf-to-tab --version
Unknown parameter "--version". Run -h for help.
 at /home/vimalinx/miniforge3/envs/bio/bin/vcf-to-tab line 18.
	main::error("Unknown parameter \"--version\". Run -h for help.\x{a}") called at /home/vimalinx/miniforge3/envs/bio/bin/vcf-to-tab line 40
	main::parse_params() called at /home/vimalinx/miniforge3/envs/bio/bin/vcf-to-tab line 8
```

## Captured Help

```text
$ vcf-to-tab --help
Usage: vcf-to-tab [OPTIONS] < in.vcf > out.tab
Options:
   -h, -?, --help                   This help message.
   -i, --iupac                      Use one-letter IUPAC codes
Notes:
   Please use `bcftools query` instead, this script will not be supported in future.
```

## Captured Man Page

```text
No man page captured.
```

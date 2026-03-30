# vcf-shuffle-cols Help Reference

- Command: `vcf-shuffle-cols`
- Sources: conda_bioconda
- Local executable: `/home/vimalinx/miniforge3/envs/bio/bin/vcf-shuffle-cols`
- Summary: CLI installed by bioconda package vcftools.
- Package names: vcftools

## Captured Version

```text
$ vcf-shuffle-cols --version
Unknown parameter "--version". Run -h for help.
 at /home/vimalinx/miniforge3/envs/bio/bin/vcf-shuffle-cols line 21.
	main::error("Unknown parameter \"--version\". Run -h for help.\x{a}") called at /home/vimalinx/miniforge3/envs/bio/bin/vcf-shuffle-cols line 42
	main::parse_params() called at /home/vimalinx/miniforge3/envs/bio/bin/vcf-shuffle-cols line 11
```

## Captured Help

```text
$ vcf-shuffle-cols --help
About: Reorder columns to match the order in the template VCF.
Usage: vcf-shuffle-cols [OPTIONS] -t template.vcf.gz file.vcf.gz > out.vcf
Options:
   -t, --template <file>            The file with the correct order of the columns.
   -h, -?, --help                   This help message.
```

## Captured Man Page

```text
No man page captured.
```

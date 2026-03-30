# vcf-fix-newlines Help Reference

- Command: `vcf-fix-newlines`
- Sources: conda_bioconda
- Local executable: `/home/vimalinx/miniforge3/envs/bio/bin/vcf-fix-newlines`
- Summary: CLI installed by bioconda package vcftools.
- Package names: vcftools

## Captured Version

```text
$ vcf-fix-newlines --version
Unknown parameter "--version". Run -h for help.
 at /home/vimalinx/miniforge3/envs/bio/bin/vcf-fix-newlines line 20.
	main::error("Unknown parameter \"--version\". Run -h for help.\x{a}") called at /home/vimalinx/miniforge3/envs/bio/bin/vcf-fix-newlines line 43
	main::parse_params() called at /home/vimalinx/miniforge3/envs/bio/bin/vcf-fix-newlines line 10
```

## Captured Help

```text
$ vcf-fix-newlines --help
About: Reads in a VCF file with any (commonly used) newline representation and outputs with the
	current system's newline representation.
Usage: vcf-fix-newlines [OPTIONS]
Options:
   -i, --info                      Report if the file is consistent with the current platform based.
   -h, -?, --help                  This help message.
Example:
	vcf-fix-newlines -i file.vcf
	vcf-fix-newlines file.vcf.gz > out.vcf
	cat file.vcf | vcf-fix-newlines > out.vcf
```

## Captured Man Page

```text
No man page captured.
```

# vcf-stats Help Reference

- Command: `vcf-stats`
- Sources: conda_bioconda
- Local executable: `/home/vimalinx/miniforge3/envs/bio/bin/vcf-stats`
- Summary: CLI installed by bioconda package vcftools.
- Package names: vcftools

## Captured Version

```text
$ vcf-stats --version
Unknown parameter or nonexistent file: "--version". Run -h for help.
 at /home/vimalinx/miniforge3/envs/bio/bin/vcf-stats line 21.
	main::error("Unknown parameter or nonexistent file: \"--version\". Run -h fo"...) called at /home/vimalinx/miniforge3/envs/bio/bin/vcf-stats line 65
	main::parse_params() called at /home/vimalinx/miniforge3/envs/bio/bin/vcf-stats line 11
```

## Captured Help

```text
$ vcf-stats --help
Usage: vcf-stats [OPTIONS] file.vcf.gz
Options:
   -d, --dump <file>                           Take an existing dump file and recreate the files (works with -p)
   -f, --filters <filter1,filter2>             List of filters such as column/field (any value), column/field=bin:max (cluster in bins),column/field=value (exact value)
   -p, --prefix <dir/string>                   Prefix of output files. If slashes are present, directories will be created.
   -s, --samples <list>                        Process only the listed samples, - for none. Excluding unwanted samples may increase performance considerably.
   -h, -?, --help                              This help message.

Examples:
   # Calculate stats separately for the filter field, quality and non-indels
   vcf-stats file.vcf.gz -f FILTER,QUAL=10:200,INFO/INDEL=False -p out/

   # Calculate stats for all samples
   vcf-stats file.vcf.gz -f FORMAT/DP=10:200 -p out/

   # Calculate stats only for the sample NA00001
   vcf-stats file.vcf.gz -f SAMPLE/NA00001/DP=1:200 -p out/

   vcf-stats file.vcf.gz > perl.dump
```

## Captured Man Page

```text
No man page captured.
```

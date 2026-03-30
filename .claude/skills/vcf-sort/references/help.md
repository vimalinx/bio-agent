# vcf-sort Help Reference

- Command: `vcf-sort`
- Sources: conda_bioconda
- Local executable: `/home/vimalinx/miniforge3/envs/bio/bin/vcf-sort`
- Summary: CLI installed by bioconda package vcftools.
- Package names: vcftools

## Captured Version

```text
$ vcf-sort --version
Unknown parameter "--version". Run -h for help.
 at /home/vimalinx/miniforge3/envs/bio/bin/vcf-sort line 20.
	main::error("Unknown parameter \"--version\". Run -h for help.\x{a}") called at /home/vimalinx/miniforge3/envs/bio/bin/vcf-sort line 46
	main::parse_params() called at /home/vimalinx/miniforge3/envs/bio/bin/vcf-sort line 10
```

## Captured Help

```text
$ vcf-sort --help
Usage: vcf-sort > out.vcf
       cat file.vcf | vcf-sort > out.vcf
Options:
   -c, --chromosomal-order       Use natural ordering (1,2,10,MT,X) rather then the default (1,10,2,MT,X). This requires
                                     new version of the unix "sort" command which supports the --version-sort option.
   -p, --parallel <int>          Change the number of sorts run concurrently to <int>
   -t, --temporary-directory     Use a directory other than /tmp as the temporary directory for sorting.
   -h, -?, --help                This help message.
```

## Captured Man Page

```text
No man page captured.
```

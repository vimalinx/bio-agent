# vrfs-variances Help Reference

- Command: `vrfs-variances`
- Sources: conda_bioconda
- Local executable: `/home/vimalinx/miniforge3/envs/bio/bin/vrfs-variances`
- Summary: CLI installed by bioconda package bcftools.
- Package names: bcftools

## Captured Version

```text
$ vrfs-variances --version
Unknown parameter "--version". Run -h for help.
 at /home/vimalinx/miniforge3/envs/bio/bin/vrfs-variances line 42.
	main::error("Unknown parameter \"--version\". Run -h for help.\x{a}") called at /home/vimalinx/miniforge3/envs/bio/bin/vrfs-variances line 66
	main::parse_params() called at /home/vimalinx/miniforge3/envs/bio/bin/vrfs-variances line 32
```

## Captured Help

```text
$ vrfs-variances --help
About: Parse bcftools/vrfs output and from a subset of sites calculate variances.
Usage: vrfs-variances [OPTIONS]
Options:
   -n, --ndat NUM          Number of sites to include, fraction (FLOAT) or absolute (INT) [0.2]
   -r, --rand-noise INT    Add random noise, INT is a seed for reproducibility, or 0 for no seed [0]
   -s, --list-sites        List sites passing the -n setting
   -v, --list-var2         Output in a format suitable for `bcftools +vrfs -r file`
   -h, -?, --help          This help message
```

## Captured Man Page

```text
No man page captured.
```

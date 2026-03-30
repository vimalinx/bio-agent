# gff2gff Help Reference

- Command: `gff2gff`
- Sources: conda_bioconda
- Local executable: `/home/vimalinx/miniforge3/envs/bio/bin/gff2gff`
- Summary: CLI installed by bioconda package bcftools.
- Package names: bcftools

## Captured Version

```text
$ gff2gff --version
Unknown parameter "--version". Run -h for help.
 at /home/vimalinx/miniforge3/envs/bio/bin/gff2gff line 40.
	main::error("Unknown parameter \"--version\". Run -h for help.\x{a}") called at /home/vimalinx/miniforge3/envs/bio/bin/gff2gff line 62
	main::parse_params() called at /home/vimalinx/miniforge3/envs/bio/bin/gff2gff line 30
```

## Captured Help

```text
$ gff2gff --help
About: Attempt to fix a GFF file to be correctly parsed by bcftools/csq, see
       the man page for the description of the expected format
           http://samtools.github.io/bcftools/bcftools-man.html#csq
Usage: gff2gff [OPTIONS]
Options:
   -v, --verbose        Increase verbosity
   -h, -?, --help       This help message
Example:
   zcat in.gff.gz | gff2gff | gzip -c > out.gff.gz
```

## Captured Man Page

```text
No man page captured.
```

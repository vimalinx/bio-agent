# run-roh-pl Help Reference

- Command: `run-roh.pl`
- Sources: conda_bioconda
- Local executable: `/home/vimalinx/miniforge3/envs/bio/bin/run-roh.pl`
- Summary: CLI installed by bioconda package bcftools.
- Package names: bcftools

## Captured Version

```text
$ run-roh.pl --version
Unknown parameter "--version". Run -h for help.

 at /home/vimalinx/miniforge3/envs/bio/bin/run-roh.pl line 43.
	main::error("Unknown parameter \"--version\". Run -h for help.\x{a}") called at /home/vimalinx/miniforge3/envs/bio/bin/run-roh.pl line 93
	main::parse_params() called at /home/vimalinx/miniforge3/envs/bio/bin/run-roh.pl line 32
```

## Captured Help

```text
$ run-roh.pl --help
About: This is a convenience wrapper for "bcftools roh" which takes multiple VCF/BCF files
       and locates regions private to a sample or shared across multiple samples. On input it
       expects a directory with .vcf, .vcf.gz or .bcf files, a file with allele frequencies
       and optionally a genetic map. See http://samtools.github.io/bcftools/howtos/roh-calling.html
       for details
Usage: run-roh.pl [OPTIONS]
Options:
   -a, --af-annots <file>      Allele frequency annotations (optional)
   -i, --indir <dir>           Input directory with VCF files
       --include <expr>        Select sites for which the expression is true
       --exclude <expr>        Exclude sites for which the epxression is true
   -l, --min-length <num>      Filter input regions shorter than this [1e6]
   -m, --genmap <dir>          Directory with genetic map in IMPUTE2 format (optional)
   -M, --rec-rate <float>      constant recombination rate per bp (optional)
   -n, --min-markers <num>     Filter input regions with fewer marker than this [100]
   -o, --outdir <dir>          Output directory
   -q, --min-qual <num>        Filter input regions with quality smaller than this [10]
       --roh-args <string>     Extra arguments to pass to bcftools roh
   -s, --silent                Quiet output, do not print commands
   -h, -?, --help              This help message
```

## Captured Man Page

```text
No man page captured.
```

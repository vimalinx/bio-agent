# vcf-subset Help Reference

- Command: `vcf-subset`
- Sources: conda_bioconda
- Local executable: `/home/vimalinx/miniforge3/envs/bio/bin/vcf-subset`
- Summary: CLI installed by bioconda package vcftools.
- Package names: vcftools

## Captured Version

```text
$ vcf-subset --version
Unknown parameter "--version". Run -h for help.
 at /home/vimalinx/miniforge3/envs/bio/bin/vcf-subset line 21.
	main::error("Unknown parameter \"--version\". Run -h for help.\x{a}") called at /home/vimalinx/miniforge3/envs/bio/bin/vcf-subset line 70
	main::parse_params() called at /home/vimalinx/miniforge3/envs/bio/bin/vcf-subset line 11
```

## Captured Help

```text
$ vcf-subset --help
Usage: vcf-subset [OPTIONS] in.vcf.gz > out.vcf
Options:
   -a, --trim-alt-alleles           Remove alternate alleles if not found in the subset
   -c, --columns <string>           File or comma-separated list of columns to keep in the vcf file. If file, one column per row
   -e, --exclude-ref                Exclude rows not containing variants.
   -f, --force                      Proceed anyway even if VCF does not contain some of the samples.
   -p, --private                    Print only rows where only the subset columns carry an alternate allele.
   -r, --replace-with-ref           Replace the excluded types with reference allele instead of dot.
   -t, --type <list>                Comma-separated list of variant types to include: ref,SNPs,indels,MNPs,other.
   -u, --keep-uncalled              Do not exclude rows without calls.
   -h, -?, --help                   This help message.
Examples:
   cat in.vcf | vcf-subset -r -t indels -e -c SAMPLE1 > out.vcf
```

## Captured Man Page

```text
No man page captured.
```

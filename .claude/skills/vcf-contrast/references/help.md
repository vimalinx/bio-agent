# vcf-contrast Help Reference

- Command: `vcf-contrast`
- Sources: conda_bioconda
- Local executable: `/home/vimalinx/miniforge3/envs/bio/bin/vcf-contrast`
- Summary: CLI installed by bioconda package vcftools.
- Package names: vcftools

## Captured Version

```text
$ vcf-contrast --version
Missing the list of variant samples (+<list>).
 at /home/vimalinx/miniforge3/envs/bio/bin/vcf-contrast line 21.
	main::error("Missing the list of variant samples (+<list>).\x{a}") called at /home/vimalinx/miniforge3/envs/bio/bin/vcf-contrast line 63
	main::parse_params() called at /home/vimalinx/miniforge3/envs/bio/bin/vcf-contrast line 11
```

## Captured Help

```text
$ vcf-contrast --help
About: Finds differences amongst samples adding NOVELGT, NOVELAL and NOVELTY annotations to INFO field.
       Note that haploid genotypes are internally treated as homozygous diploid genotypes, therefore
       "0/1" and "1" are considered different genotypes.
Usage: vcf-contrast +<list> -<list> [OPTIONS] file.vcf.gz
Options:
   +<list>                             List of samples where unique variant is expected
   -<list>                             List of background samples
   -d, --min-DP <int>                  Minimum depth across all -<list> samples
   -f, --apply-filters                 Skip sites with FILTER column different from PASS or "."
   -n, --novel-sites                   Print only records with novel genotypes
   -h, -?, --help                      This help message.
Example:
   # Test if any of the samples A,B is different from all C,D,E
   vcf-contrast +A,B -C,D,E -m file.vcf.gz

   # Same as above but printing only sites with novel variants and table output
   vcf-contrast -n +A,B -C,D,E -m file.vcf.gz | vcf-query -f '%CHROM %POS\t%INFO/NOVELTY\t%INFO/NOVELAL\t%INFO/NOVELGT[\t%SAMPLE %GTR %PL]\n'

   # Similar to above but require minimum mapping quality of 20
   vcf-annotate -f MinMQ=20 file.vcf.gz | vcf-contrast +A,B,C -D,E,F -f
```

## Captured Man Page

```text
No man page captured.
```

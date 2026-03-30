# vcf-fix-ploidy Help Reference

- Command: `vcf-fix-ploidy`
- Sources: conda_bioconda
- Local executable: `/home/vimalinx/miniforge3/envs/bio/bin/vcf-fix-ploidy`
- Summary: CLI installed by bioconda package vcftools.
- Package names: vcftools

## Captured Version

```text
$ vcf-fix-ploidy --version
Unknown parameter "--version". Run -h for help.
 at /home/vimalinx/miniforge3/envs/bio/bin/vcf-fix-ploidy line 21.
	main::error("Unknown parameter \"--version\". Run -h for help.\x{a}") called at /home/vimalinx/miniforge3/envs/bio/bin/vcf-fix-ploidy line 83
	main::parse_params() called at /home/vimalinx/miniforge3/envs/bio/bin/vcf-fix-ploidy line 11
```

## Captured Help

```text
$ vcf-fix-ploidy --help
Usage: cat broken.vcf | vcf-fix-ploidy [OPTIONS] > fixed.vcf
Options:
   -a, --assumed-sex <sex>         M or F, required if the list is not complete in -s
   -l, --fix-likelihoods           Add or remove het likelihoods (not the default behaviour)
   -p, --ploidy <file>             Ploidy definition. The default is shown below.
   -s, --samples <file>            List of sample sexes (sample_name [MF]).
   -h, -?, --help                  This help message.
Default ploidy definition:
   ploidy =>
   {
       X =>
       [
           # The pseudoautosomal regions 60,001-2,699,520 and 154,931,044-155,270,560 with the ploidy 2
           { from=>1, to=>60_000, M=>1 },
           { from=>2_699_521, to=>154_931_043, M=>1 },
       ],
       Y =>
       [
           # No chrY in females and one copy in males
           { from=>1, to=>59_373_566, M=>1, F=>0 },
       ],
       MT =>
       [
           # Haploid MT in males and females
           { from=>1, to => 16_569, M=>1, F=>1 },
       ],
   }
```

## Captured Man Page

```text
No man page captured.
```

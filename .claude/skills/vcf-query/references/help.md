# vcf-query Help Reference

- Command: `vcf-query`
- Sources: conda_bioconda
- Local executable: `/home/vimalinx/miniforge3/envs/bio/bin/vcf-query`
- Summary: CLI installed by bioconda package vcftools.
- Package names: vcftools

## Captured Version

```text
$ vcf-query --version
Unknown parameter or non-existent file "--version". Run -h for help.
 at /home/vimalinx/miniforge3/envs/bio/bin/vcf-query line 21.
	main::error("Unknown parameter or non-existent file \"--version\". Run -h fo"...) called at /home/vimalinx/miniforge3/envs/bio/bin/vcf-query line 65
	main::parse_params() called at /home/vimalinx/miniforge3/envs/bio/bin/vcf-query line 11
```

## Captured Help

```text
$ vcf-query --help
Usage: vcf-query [OPTIONS] file.vcf.gz
Options:
   -c, --columns <file|list>           List of comma-separated column names or one column name per line in a file.
   -f, --format <string>               The default is '%CHROM:%POS\t%REF[\t%SAMPLE=%GT]\n'
   -l, --list-columns                  List columns.
   -r, --region chr:from-to            Retrieve the region. (Runs tabix.)
       --use-old-method                Use old version of API, which is slow but more robust.
   -h, -?, --help                      This help message.
Expressions:
   %CHROM          The CHROM column (similarly also other columns)
   %GT             Translated genotype (e.g. C/A)
   %GTR            Raw genotype (e.g. 0/1)
   %INFO/TAG       Any tag in the INFO column
   %LINE           Prints the whole line
   %SAMPLE         Sample name
   []              The brackets loop over all samples
   %*<A><B>        All format fields printed as KEY<A>VALUE<B>
Examples:
   vcf-query file.vcf.gz 1:1000-2000 -c NA001,NA002,NA003
   vcf-query file.vcf.gz -r 1:1000-2000 -f '%CHROM:%POS\t%REF\t%ALT[\t%SAMPLE:%*=,]\n'
   vcf-query file.vcf.gz -f '[%GT\t]%LINE\n'
   vcf-query file.vcf.gz -f '[%GT\ ]%LINE\n'
   vcf-query file.vcf.gz -f '%CHROM\_%POS\t%INFO/DP\t%FILTER\n'
Notes:
   Please use `bcftools query` instead, this script will not be supported in future.
```

## Captured Man Page

```text
No man page captured.
```

# vcf-merge Help Reference

- Command: `vcf-merge`
- Sources: conda_bioconda
- Local executable: `/home/vimalinx/miniforge3/envs/bio/bin/vcf-merge`
- Summary: CLI installed by bioconda package vcftools.
- Package names: vcftools

## Captured Version

```text
$ vcf-merge --version
Unknown parameter or non-existent file "--version". Run -? for help.
 at /home/vimalinx/miniforge3/envs/bio/bin/vcf-merge line 21.
	main::error("Unknown parameter or non-existent file \"--version\". Run -? fo"...) called at /home/vimalinx/miniforge3/envs/bio/bin/vcf-merge line 79
	main::parse_params() called at /home/vimalinx/miniforge3/envs/bio/bin/vcf-merge line 11
```

## Captured Help

```text
$ vcf-merge --help
About: Merges VCF files by position, creating multi-sample VCFs from fewer-sample VCFs.
   The tool requires bgzipped and tabix indexed VCF files on input. (E.g. bgzip file.vcf; tabix -p vcf file.vcf.gz)
   If you need to concatenate VCFs (e.g. files split by chromosome), look at vcf-concat instead.
Usage: vcf-merge [OPTIONS] file1.vcf file2.vcf.gz ... > out.vcf
Options:
   -c, --collapse <snps|indels|both|any|none>      treat as identical sites with differing alleles [any]
   -d, --remove-duplicates                         If there should be two consecutive rows with the same chr:pos, print only the first one.
   -H, --vcf-header <file>                         Use the provided VCF header
   -h, -?, --help                                  This help message.
   -r, --regions <list|file>                       Do only the given regions (comma-separated list or one region per line in a file).
   -R, --ref-for-missing <string>                  Use the REF allele instead of the default missing genotype. Because it is not obvious
                                                       what ploidy should be used, a user-defined string is used instead (e.g. 0/0).
   -s, --silent                                    Try to be a bit more silent, no warnings about duplicate lines.
   -t, --trim-ALTs                                 If set, redundant ALTs will be removed
```

## Captured Man Page

```text
No man page captured.
```

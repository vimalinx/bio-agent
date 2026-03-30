# vcf-compare Help Reference

- Command: `vcf-compare`
- Sources: conda_bioconda
- Local executable: `/home/vimalinx/miniforge3/envs/bio/bin/vcf-compare`
- Summary: CLI installed by bioconda package vcftools.
- Package names: vcftools

## Captured Version

```text
$ vcf-compare --version
Unknown parameter or non-existent file "--version". Run -h for help.
 at /home/vimalinx/miniforge3/envs/bio/bin/vcf-compare line 29.
	main::error("Unknown parameter or non-existent file \"--version\". Run -h fo"...) called at /home/vimalinx/miniforge3/envs/bio/bin/vcf-compare line 104
	main::parse_params() called at /home/vimalinx/miniforge3/envs/bio/bin/vcf-compare line 12
```

## Captured Help

```text
$ vcf-compare --help
About: Compare bgzipped and tabix indexed VCF files. (E.g. bgzip file.vcf; tabix -p vcf file.vcf.gz)
Usage: vcf-compare [OPTIONS] file1.vcf file2.vcf ...
       vcf-compare -p plots chr1.cmp chr2.cmp ...
Options:
   -a, --apply-filters                 Ignore lines where FILTER column is anything else than PASS or '.'
   -c, --chromosomes <list|file>       Same as -r, left for backward compatibility. Please do not use as it will be dropped in the future.
   -d, --debug                         Debugging information. Giving the option multiple times increases verbosity
   -g, --cmp-genotypes                 Compare genotypes, not only positions
       --ignore-indels                 Exclude sites containing indels from genotype comparison
   -m, --name-mapping <list|file>      Use with -g when comparing files with differing column names. The argument to this options is a
                                           comma-separated list or one mapping per line in a file. The names are colon separated and must
                                           appear in the same order as the files on the command line.
       --INFO <string> [<int>]         Calculate genotype errors by INFO. Use zero based indecies if field has more than one value. Can be
                                           given multiple times.
   -p, --plot <prefix>                 Create plots. Multiple files (e.g. per-chromosome outputs from vcf-compare) can be given.
   -R, --refseq <file>                 Compare the actual sequence, not just positions. Use with -w to compare indels.
   -r, --regions <list|file>           Process the given regions (comma-separated list or one region per line in a file).
   -s, --samples <list|file>           Process only the listed samples. Excluding unwanted samples may increase performance considerably.
   -t, --title <string>                Title for graphs (see also -p)
   -w, --win <int>                     In repetitive sequences, the same indel can be called at different positions. Consider
                                           records this far apart as matching (be it a SNP or an indel).
   -h, -?, --help                      This help message.
```

## Captured Man Page

```text
No man page captured.
```

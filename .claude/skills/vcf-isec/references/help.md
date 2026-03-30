# vcf-isec Help Reference

- Command: `vcf-isec`
- Sources: conda_bioconda
- Local executable: `/home/vimalinx/miniforge3/envs/bio/bin/vcf-isec`
- Summary: CLI installed by bioconda package vcftools.
- Package names: vcftools

## Captured Version

```text
$ vcf-isec --version
Unknown parameter or non-existent file "--version". Run -h for help.
 at /home/vimalinx/miniforge3/envs/bio/bin/vcf-isec line 21.
	main::error("Unknown parameter or non-existent file \"--version\". Run -h fo"...) called at /home/vimalinx/miniforge3/envs/bio/bin/vcf-isec line 87
	main::parse_params() called at /home/vimalinx/miniforge3/envs/bio/bin/vcf-isec line 11
```

## Captured Help

```text
$ vcf-isec --help
About: Create intersections, unions, complements on bgzipped and tabix indexed VCF or tab-delimited files.
   Note that lines from all files can be intermixed together on the output, which can yield
   unexpected results.
Usage: vcf-isec [OPTIONS] file1.vcf file2.vcf ...
Options:
   -a, --apply-filters                 Ignore lines where FILTER column is anything else than PASS or '.'
   -c, --complement                    Output positions present in the first file but missing from the other files.
   -d, --debug                         Debugging information
   -f, --force                         Continue even if the script complains about differing columns, VCF versions, etc.
   -o, --one-file-only                 Print only entries from the left-most file. Without -o, all unique positions will be printed.
   -n, --nfiles [+-=]<int>             Output positions present in this many (=), this many or more (+), or this many or fewer (-) files.
   -p, --prefix <path>                 If present, multiple files will be created with all possible isec combinations. (Suitable for Venn Diagram analysis.)
   -r, --regions <list|file>           Do only the given regions (comma-separated list or one region per line in a file).
   -t, --tab <chr:pos:file>            Tab-delimited file with indexes of chromosome and position columns. (1-based indexes)
   -w, --win <int>                     In repetitive sequences, the same indel can be called at different positions. Consider
                                           records this far apart as matching (be it a SNP or an indel).
   -h, -?, --help                      This help message.
Examples:
   bgzip file.vcf; tabix -p vcf file.vcf.gz
   bgzip file.tab; tabix -s 1 -b 2 -e 2 file.tab.gz
```

## Captured Man Page

```text
No man page captured.
```

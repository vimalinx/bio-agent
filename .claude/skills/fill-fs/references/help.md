# fill-fs Help Reference

- Command: `fill-fs`
- Sources: conda_bioconda
- Local executable: `/home/vimalinx/miniforge3/envs/bio/bin/fill-fs`
- Summary: CLI installed by bioconda package vcftools.
- Package names: vcftools

## Captured Version

```text
$ fill-fs --version
Unknown parameter "--version". Run -h for help.
 at /home/vimalinx/miniforge3/envs/bio/bin/fill-fs line 22.
	main::error("Unknown parameter \"--version\". Run -h for help.\x{a}") called at /home/vimalinx/miniforge3/envs/bio/bin/fill-fs line 58
	main::parse_params() called at /home/vimalinx/miniforge3/envs/bio/bin/fill-fs line 12
```

## Captured Help

```text
$ fill-fs --help
About: Annotate VCF with flanking sequence (INFO/FS tag)
Usage: fill-fs [OPTIONS] file.vcf
Options:
   -b, --bed-mask <file>           Regions to mask (tabix indexed), multiple files can be given
   -c, --cluster <int>             Do self-masking of clustered variants within this range.
   -l, --length <int>              Flanking sequence length [100]
   -m, --mask-char <char|lc>       The character to use or "lc" for lowercase. This option must preceed
                                       -b, -v or -c in order to take effect. With multiple files works
                                        as a switch on the command line, see the example below [N]
   -r, --refseq <file>             The reference sequence.
   -v, --vcf-mask <file>           Mask known variants in the flanking sequence, multiple files can be given (tabix indexed)
   -h, -?, --help                  This help message.
Example:
   # Mask variants from the VCF file with N's and use lowercase for the bed file regions
   fill-fs file.vcf -v mask.vcf -m lc -b mask.bed
```

## Captured Man Page

```text
No man page captured.
```

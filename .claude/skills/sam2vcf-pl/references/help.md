# sam2vcf-pl Help Reference

- Command: `sam2vcf.pl`
- Sources: conda_bioconda
- Local executable: `/home/vimalinx/miniforge3/envs/bio/bin/sam2vcf.pl`
- Summary: CLI installed by bioconda package samtools.
- Package names: samtools

## Captured Version

```text
$ sam2vcf.pl --version
Unknown parameter "--version". Run -h for help.
 at /home/vimalinx/miniforge3/envs/bio/bin/sam2vcf.pl line 41.
	main::error("Unknown parameter \"--version\". Run -h for help.\x{a}") called at /home/vimalinx/miniforge3/envs/bio/bin/sam2vcf.pl line 71
	main::parse_params() called at /home/vimalinx/miniforge3/envs/bio/bin/sam2vcf.pl line 31
```

## Captured Help

```text
$ sam2vcf.pl --help
Usage: sam2vcf.pl [OPTIONS] < in.pileup > out.vcf
Options:
   -h, -?, --help                  This help message.
   -i, --indels-only               Ignore SNPs.
   -r, --refseq <file.fa>          The reference sequence, required when indels are present.
   -R, --keep-ref                  Print reference alleles as well.
   -s, --snps-only                 Ignore indels.
   -t, --column-title <string>     The column title.
```

## Captured Man Page

```text
No man page captured.
```

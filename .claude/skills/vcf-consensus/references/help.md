# vcf-consensus Help Reference

- Command: `vcf-consensus`
- Sources: conda_bioconda
- Local executable: `/home/vimalinx/miniforge3/envs/bio/bin/vcf-consensus`
- Summary: CLI installed by bioconda package vcftools.
- Package names: vcftools

## Captured Version

```text
$ vcf-consensus --version
Unknown parameter "--version". Run -h for help.
 at /home/vimalinx/miniforge3/envs/bio/bin/vcf-consensus line 18.
	main::error("Unknown parameter \"--version\". Run -h for help.\x{a}") called at /home/vimalinx/miniforge3/envs/bio/bin/vcf-consensus line 47
	main::parse_params() called at /home/vimalinx/miniforge3/envs/bio/bin/vcf-consensus line 8
```

## Captured Help

```text
$ vcf-consensus --help
Usage: cat ref.fa | vcf-consensus [OPTIONS] in.vcf.gz > out.fa
Options:
   -h, -?, --help                   This help message.
   -H, --haplotype <int>            Apply only variants for the given haplotype (1,2)
   -i, --iupac-codes                Apply variants in the form of IUPAC ambiguity codes
   -s, --sample <name>              If not given, all variants are applied
Examples:
   # Get the consensus for one region. The fasta header lines are then expected
   # in the form ">chr:from-to".
   samtools faidx ref.fa 8:11870-11890 | vcf-consensus in.vcf.gz > out.fa
```

## Captured Man Page

```text
No man page captured.
```

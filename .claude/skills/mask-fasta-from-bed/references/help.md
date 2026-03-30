# mask-fasta-from-bed Help Reference

- Command: `maskFastaFromBed`
- Sources: conda_bioconda
- Local executable: `/home/vimalinx/miniforge3/envs/bio/bin/maskFastaFromBed`
- Summary: CLI installed by bioconda package bedtools.
- Package names: bedtools

## Captured Version

```text
$ maskFastaFromBed --version
*****ERROR: Unrecognized parameter: --version *****


Tool:    bedtools maskfasta (aka maskFastaFromBed)
Version: v2.31.1
Summary: Mask a fasta file based on feature coordinates.

Usage:   bedtools maskfasta [OPTIONS] -fi <fasta> -fo <fasta> -bed <bed/gff/vcf>

Options:
	-fi		Input FASTA file
	-bed		BED/GFF/VCF file of ranges to mask in -fi
	-fo		Output FASTA file
	-soft		Enforce "soft" masking.
			Mask with lower-case bases, instead of masking with Ns.
	-mc		Replace masking character.
			Use another character, instead of masking with Ns.
	-fullHeader	Use full fasta header.
			By default, only the word before the first space or tab
			is used.
```

## Captured Help

```text
$ maskFastaFromBed --help
*****ERROR: Unrecognized parameter: --help *****


Tool:    bedtools maskfasta (aka maskFastaFromBed)
Version: v2.31.1
Summary: Mask a fasta file based on feature coordinates.

Usage:   bedtools maskfasta [OPTIONS] -fi <fasta> -fo <fasta> -bed <bed/gff/vcf>

Options:
	-fi		Input FASTA file
	-bed		BED/GFF/VCF file of ranges to mask in -fi
	-fo		Output FASTA file
	-soft		Enforce "soft" masking.
			Mask with lower-case bases, instead of masking with Ns.
	-mc		Replace masking character.
			Use another character, instead of masking with Ns.
	-fullHeader	Use full fasta header.
			By default, only the word before the first space or tab
			is used.
```

## Captured Man Page

```text
No man page captured.
```

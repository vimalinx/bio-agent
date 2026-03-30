# fasta-from-bed Help Reference

- Command: `fastaFromBed`
- Sources: conda_bioconda
- Local executable: `/home/vimalinx/miniforge3/envs/bio/bin/fastaFromBed`
- Summary: CLI installed by bioconda package bedtools.
- Package names: bedtools

## Captured Version

```text
$ fastaFromBed --version
*****ERROR: Unrecognized parameter: --version *****


Tool:    bedtools getfasta (aka fastaFromBed)
Version: v2.31.1
Summary: Extract DNA sequences from a fasta file based on feature coordinates.

Usage:   bedtools getfasta [OPTIONS] -fi <fasta> -bed <bed/gff/vcf>

Options: 
	-fi		Input FASTA file
	-fo		Output file (opt., default is STDOUT
	-bed		BED/GFF/VCF file of ranges to extract from -fi
	-name		Use the name field and coordinates for the FASTA header
	-name+		(deprecated) Use the name field and coordinates for the FASTA header
	-nameOnly	Use the name field for the FASTA header
	-split		Given BED12 fmt., extract and concatenate the sequences
			from the BED "blocks" (e.g., exons)
	-tab		Write output in TAB delimited format.
	-bedOut		Report extract sequences in a tab-delimited BED format instead of in FASTA format.
			- Default is FASTA format.
	-s		Force strandedness. If the feature occupies the antisense,
			strand, the sequence will be reverse complemented.
			- By default, strand information is ignored.
	-fullHeader	Use full fasta header.
			- By default, only the word before the first space or tab 
			is used.
	-rna	The FASTA is RNA not DNA. Reverse complementation handled accordingly.
```

## Captured Help

```text
$ fastaFromBed --help
*****ERROR: Unrecognized parameter: --help *****


Tool:    bedtools getfasta (aka fastaFromBed)
Version: v2.31.1
Summary: Extract DNA sequences from a fasta file based on feature coordinates.

Usage:   bedtools getfasta [OPTIONS] -fi <fasta> -bed <bed/gff/vcf>

Options: 
	-fi		Input FASTA file
	-fo		Output file (opt., default is STDOUT
	-bed		BED/GFF/VCF file of ranges to extract from -fi
	-name		Use the name field and coordinates for the FASTA header
	-name+		(deprecated) Use the name field and coordinates for the FASTA header
	-nameOnly	Use the name field for the FASTA header
	-split		Given BED12 fmt., extract and concatenate the sequences
			from the BED "blocks" (e.g., exons)
	-tab		Write output in TAB delimited format.
	-bedOut		Report extract sequences in a tab-delimited BED format instead of in FASTA format.
			- Default is FASTA format.
	-s		Force strandedness. If the feature occupies the antisense,
			strand, the sequence will be reverse complemented.
			- By default, strand information is ignored.
	-fullHeader	Use full fasta header.
			- By default, only the word before the first space or tab 
			is used.
	-rna	The FASTA is RNA not DNA. Reverse complementation handled accordingly.
```

## Captured Man Page

```text
No man page captured.
```

# bam-to-bed Help Reference

- Command: `bamToBed`
- Sources: conda_bioconda
- Local executable: `/home/vimalinx/miniforge3/envs/bio/bin/bamToBed`
- Summary: CLI installed by bioconda package bedtools.
- Package names: bedtools

## Captured Version

```text
$ bamToBed --version
*****ERROR: Unrecognized parameter: --version *****


Tool:    bedtools bamtobed (aka bamToBed)
Version: v2.31.1
Summary: Converts BAM alignments to BED6 or BEDPE format.

Usage:   bedtools bamtobed [OPTIONS] -i <bam> 

Options: 
	-bedpe	Write BEDPE format.
		- Requires BAM to be grouped or sorted by query.

	-mate1	When writing BEDPE (-bedpe) format, 
		always report mate one as the first BEDPE "block".

	-bed12	Write "blocked" BED format (aka "BED12"). Forces -split.

		http://genome-test.cse.ucsc.edu/FAQ/FAQformat#format1

	-split	Report "split" BAM alignments as separate BED entries.
		Splits only on N CIGAR operations.

	-splitD	Split alignments based on N and D CIGAR operators.
		Forces -split.

	-ed	Use BAM edit distance (NM tag) for BED score.
		- Default for BED is to use mapping quality.
		- Default for BEDPE is to use the minimum of
		  the two mapping qualities for the pair.
		- When -ed is used with -bedpe, the total edit
		  distance from the two mates is reported.

	-tag	Use other NUMERIC BAM alignment tag for BED score.
		- Default for BED is to use mapping quality.
		  Disallowed with BEDPE output.

	-color	An R,G,B string for the color used with BED12 format.
		Default is (255,0,0).

	-cigar	Add the CIGAR string to the BED entry as a 7th column.
```

## Captured Help

```text
$ bamToBed --help
*****ERROR: Unrecognized parameter: --help *****


Tool:    bedtools bamtobed (aka bamToBed)
Version: v2.31.1
Summary: Converts BAM alignments to BED6 or BEDPE format.

Usage:   bedtools bamtobed [OPTIONS] -i <bam> 

Options: 
	-bedpe	Write BEDPE format.
		- Requires BAM to be grouped or sorted by query.

	-mate1	When writing BEDPE (-bedpe) format, 
		always report mate one as the first BEDPE "block".

	-bed12	Write "blocked" BED format (aka "BED12"). Forces -split.

		http://genome-test.cse.ucsc.edu/FAQ/FAQformat#format1

	-split	Report "split" BAM alignments as separate BED entries.
		Splits only on N CIGAR operations.

	-splitD	Split alignments based on N and D CIGAR operators.
		Forces -split.

	-ed	Use BAM edit distance (NM tag) for BED score.
		- Default for BED is to use mapping quality.
		- Default for BEDPE is to use the minimum of
		  the two mapping qualities for the pair.
		- When -ed is used with -bedpe, the total edit
		  distance from the two mates is reported.

	-tag	Use other NUMERIC BAM alignment tag for BED score.
		- Default for BED is to use mapping quality.
		  Disallowed with BEDPE output.

	-color	An R,G,B string for the color used with BED12 format.
		Default is (255,0,0).

	-cigar	Add the CIGAR string to the BED entry as a 7th column.
```

## Captured Man Page

```text
No man page captured.
```

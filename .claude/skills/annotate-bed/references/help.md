# annotate-bed Help Reference

- Command: `annotateBed`
- Sources: conda_bioconda
- Local executable: `/home/vimalinx/miniforge3/envs/bio/bin/annotateBed`
- Summary: CLI installed by bioconda package bedtools.
- Package names: bedtools

## Captured Version

```text
$ annotateBed --version
*****ERROR: Unrecognized parameter: --version *****


*****
*****ERROR: Need -i and -files files. 
*****

Tool:    bedtools annotate (aka annotateBed)
Version: v2.31.1
Summary: Annotates the depth & breadth of coverage of features from mult. files
	 on the intervals in -i.

Usage:   bedtools annotate [OPTIONS] -i <bed/gff/vcf> -files FILE1 FILE2..FILEn

Options: 
	-names	A list of names (one / file) to describe each file in -i.
		These names will be printed as a header line.

	-counts	Report the count of features in each file that overlap -i.
		- Default is to report the fraction of -i covered by each file.

	-both	Report the counts followed by the % coverage.
		- Default is to report the fraction of -i covered by each file.

	-s	Require same strandedness.  That is, only counts overlaps
		on the _same_ strand.
		- By default, overlaps are counted without respect to strand.

	-S	Require different strandedness.  That is, only count overlaps
		on the _opposite_ strand.
		- By default, overlaps are counted without respect to strand.
```

## Captured Help

```text
$ annotateBed --help
*****ERROR: Unrecognized parameter: --help *****


*****
*****ERROR: Need -i and -files files. 
*****

Tool:    bedtools annotate (aka annotateBed)
Version: v2.31.1
Summary: Annotates the depth & breadth of coverage of features from mult. files
	 on the intervals in -i.

Usage:   bedtools annotate [OPTIONS] -i <bed/gff/vcf> -files FILE1 FILE2..FILEn

Options: 
	-names	A list of names (one / file) to describe each file in -i.
		These names will be printed as a header line.

	-counts	Report the count of features in each file that overlap -i.
		- Default is to report the fraction of -i covered by each file.

	-both	Report the counts followed by the % coverage.
		- Default is to report the fraction of -i covered by each file.

	-s	Require same strandedness.  That is, only counts overlaps
		on the _same_ strand.
		- By default, overlaps are counted without respect to strand.

	-S	Require different strandedness.  That is, only count overlaps
		on the _opposite_ strand.
		- By default, overlaps are counted without respect to strand.
```

## Captured Man Page

```text
No man page captured.
```

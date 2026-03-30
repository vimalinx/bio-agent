# tag-bam Help Reference

- Command: `tagBam`
- Sources: conda_bioconda
- Local executable: `/home/vimalinx/miniforge3/envs/bio/bin/tagBam`
- Summary: CLI installed by bioconda package bedtools.
- Package names: bedtools

## Captured Version

```text
$ tagBam --version
*****ERROR: Unrecognized parameter: --version *****


*****
*****ERROR: Need -i, -files
*****

*****
*****ERROR: Need -labels or -names or -scores
*****

Tool:    bedtools tag (aka tagBam)
Version: v2.31.1
Summary: Annotates a BAM file based on overlaps with multiple BED/GFF/VCF files
	 on the intervals in -i.

Usage:   bedtools tag [OPTIONS] -i <BAM> -files FILE1 .. FILEn  -labels LAB1 .. LABn

Options: 
	-s	Require overlaps on the same strand.  That is, only tag alignments that have the same
		strand as a feature in the annotation file(s).

	-S	Require overlaps on the opposite strand.  That is, only tag alignments that have the opposite
		strand as a feature in the annotation file(s).

	-f	Minimum overlap required as a fraction of the alignment.
		- Default is 1E-9 (i.e., 1bp).
		- FLOAT (e.g. 0.50)

	-tag	Dictate what the tag should be. Default is YB.
		- STRING (two characters, e.g., YK)

	-names	Use the name field from the annotation files to populate tags.
		By default, the -labels values are used.

	-scores	Use the score field from the annotation files to populate tags.
		By default, the -labels values are used.

	-intervals	Use the full interval (including name, score, and strand) to populate tags.
			Requires the -labels option to identify from which file the interval came.
```

## Captured Help

```text
$ tagBam --help
*****ERROR: Unrecognized parameter: --help *****


*****
*****ERROR: Need -i, -files
*****

*****
*****ERROR: Need -labels or -names or -scores
*****

Tool:    bedtools tag (aka tagBam)
Version: v2.31.1
Summary: Annotates a BAM file based on overlaps with multiple BED/GFF/VCF files
	 on the intervals in -i.

Usage:   bedtools tag [OPTIONS] -i <BAM> -files FILE1 .. FILEn  -labels LAB1 .. LABn

Options: 
	-s	Require overlaps on the same strand.  That is, only tag alignments that have the same
		strand as a feature in the annotation file(s).

	-S	Require overlaps on the opposite strand.  That is, only tag alignments that have the opposite
		strand as a feature in the annotation file(s).

	-f	Minimum overlap required as a fraction of the alignment.
		- Default is 1E-9 (i.e., 1bp).
		- FLOAT (e.g. 0.50)

	-tag	Dictate what the tag should be. Default is YB.
		- STRING (two characters, e.g., YK)

	-names	Use the name field from the annotation files to populate tags.
		By default, the -labels values are used.

	-scores	Use the score field from the annotation files to populate tags.
		By default, the -labels values are used.

	-intervals	Use the full interval (including name, score, and strand) to populate tags.
			Requires the -labels option to identify from which file the interval came.
```

## Captured Man Page

```text
No man page captured.
```

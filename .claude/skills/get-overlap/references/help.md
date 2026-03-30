# get-overlap Help Reference

- Command: `getOverlap`
- Sources: conda_bioconda
- Local executable: `/home/vimalinx/miniforge3/envs/bio/bin/getOverlap`
- Summary: CLI installed by bioconda package bedtools.
- Package names: bedtools

## Captured Version

```text
$ getOverlap --version
*****ERROR: Unrecognized parameter: --version *****


Tool:    bedtools overlap (aka getOverlap)
Version: v2.31.1
Summary: Computes the amount of overlap (positive values)
	 or distance (negative values) between genome features
	 and reports the result at the end of the same line.

Options: 
	-i	Input file. Use "stdin" for pipes.

	-cols	Specify the columns (1-based) for the starts and ends of the
		features for which you'd like to compute the overlap/distance.
		The columns must be listed in the following order: 

		start1,end1,start2,end2

Example: 
	$ bedtools window -a A.bed -b B.bed -w 10
	chr1 10  20  A   chr1    15  25  B
	chr1 10  20  C   chr1    25  35  D

	$ bedtools window -a A.bed -b B.bed -w 10 | bedtools overlap -i stdin -cols 2,3,6,7
	chr1 10  20  A   chr1    15  25  B   5
	chr1 10  20  C   chr1    25  35  D   -5
```

## Captured Help

```text
$ getOverlap --help
*****ERROR: Unrecognized parameter: --help *****


Tool:    bedtools overlap (aka getOverlap)
Version: v2.31.1
Summary: Computes the amount of overlap (positive values)
	 or distance (negative values) between genome features
	 and reports the result at the end of the same line.

Options: 
	-i	Input file. Use "stdin" for pipes.

	-cols	Specify the columns (1-based) for the starts and ends of the
		features for which you'd like to compute the overlap/distance.
		The columns must be listed in the following order: 

		start1,end1,start2,end2

Example: 
	$ bedtools window -a A.bed -b B.bed -w 10
	chr1 10  20  A   chr1    15  25  B
	chr1 10  20  C   chr1    25  35  D

	$ bedtools window -a A.bed -b B.bed -w 10 | bedtools overlap -i stdin -cols 2,3,6,7
	chr1 10  20  A   chr1    15  25  B   5
	chr1 10  20  C   chr1    25  35  D   -5
```

## Captured Man Page

```text
No man page captured.
```

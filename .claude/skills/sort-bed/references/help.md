# sort-bed Help Reference

- Command: `sortBed`
- Sources: conda_bioconda
- Local executable: `/home/vimalinx/miniforge3/envs/bio/bin/sortBed`
- Summary: CLI installed by bioconda package bedtools.
- Package names: bedtools

## Captured Version

```text
$ sortBed --version
*****ERROR: Unrecognized parameter: --version *****


Tool:    bedtools sort (aka sortBed)
Version: v2.31.1
Summary: Sorts a feature file in various and useful ways.

Usage:   bedtools sort [OPTIONS] -i <bed/gff/vcf>

Options: 
	-sizeA			Sort by feature size in ascending order.
	-sizeD			Sort by feature size in descending order.
	-chrThenSizeA		Sort by chrom (asc), then feature size (asc).
	-chrThenSizeD		Sort by chrom (asc), then feature size (desc).
	-chrThenScoreA		Sort by chrom (asc), then score (asc).
	-chrThenScoreD		Sort by chrom (asc), then score (desc).
	-g (names.txt)	Sort according to the chromosomes declared in "genome.txt"
	-faidx (names.txt)	Sort according to the chromosomes declared in "names.txt"
	-header	Print the header from the A file prior to results.
```

## Captured Help

```text
$ sortBed --help
*****ERROR: Unrecognized parameter: --help *****


Tool:    bedtools sort (aka sortBed)
Version: v2.31.1
Summary: Sorts a feature file in various and useful ways.

Usage:   bedtools sort [OPTIONS] -i <bed/gff/vcf>

Options: 
	-sizeA			Sort by feature size in ascending order.
	-sizeD			Sort by feature size in descending order.
	-chrThenSizeA		Sort by chrom (asc), then feature size (asc).
	-chrThenSizeD		Sort by chrom (asc), then feature size (desc).
	-chrThenScoreA		Sort by chrom (asc), then score (asc).
	-chrThenScoreD		Sort by chrom (asc), then score (desc).
	-g (names.txt)	Sort according to the chromosomes declared in "genome.txt"
	-faidx (names.txt)	Sort according to the chromosomes declared in "names.txt"
	-header	Print the header from the A file prior to results.
```

## Captured Man Page

```text
No man page captured.
```

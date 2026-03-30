# cluster-bed Help Reference

- Command: `clusterBed`
- Sources: conda_bioconda
- Local executable: `/home/vimalinx/miniforge3/envs/bio/bin/clusterBed`
- Summary: CLI installed by bioconda package bedtools.
- Package names: bedtools

## Captured Version

```text
$ clusterBed --version
*****ERROR: Unrecognized parameter: --version *****


Tool:    bedtools cluster
Version: v2.31.1
Summary: Clusters overlapping/nearby BED/GFF/VCF intervals.

Usage:   bedtools cluster [OPTIONS] -i <bed/gff/vcf>

Options: 
	-s	Force strandedness.  That is, only merge features
		that are the same strand.
		- By default, merging is done without respect to strand.

	-d	Maximum distance between features allowed for features
		to be merged.
		- Def. 0. That is, overlapping & book-ended features are merged.
		- (INTEGER)
```

## Captured Help

```text
$ clusterBed --help
*****ERROR: Unrecognized parameter: --help *****


Tool:    bedtools cluster
Version: v2.31.1
Summary: Clusters overlapping/nearby BED/GFF/VCF intervals.

Usage:   bedtools cluster [OPTIONS] -i <bed/gff/vcf>

Options: 
	-s	Force strandedness.  That is, only merge features
		that are the same strand.
		- By default, merging is done without respect to strand.

	-d	Maximum distance between features allowed for features
		to be merged.
		- Def. 0. That is, overlapping & book-ended features are merged.
		- (INTEGER)
```

## Captured Man Page

```text
No man page captured.
```

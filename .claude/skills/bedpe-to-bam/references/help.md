# bedpe-to-bam Help Reference

- Command: `bedpeToBam`
- Sources: conda_bioconda
- Local executable: `/home/vimalinx/miniforge3/envs/bio/bin/bedpeToBam`
- Summary: CLI installed by bioconda package bedtools.
- Package names: bedtools

## Captured Version

```text
$ bedpeToBam --version
*****ERROR: Unrecognized parameter: --version *****


*****
*****ERROR: Need -g (genome) file. 
*****

Tool:    bedtools bedpetobam (aka bedpeToBam)
Version: v2.31.1
Summary: Converts feature records to BAM format.

Usage:   bedpetobam [OPTIONS] -i <bed/gff/vcf> -g <genome>

Options: 
	-mapq	Set the mappinq quality for the BAM records.
		(INT) Default: 255

	-ubam	Write uncompressed BAM output. Default writes compressed BAM.

Notes: 
	(1)  BED files must be at least BED4 to create BAM (needs name field).
```

## Captured Help

```text
$ bedpeToBam --help
*****ERROR: Unrecognized parameter: --help *****


*****
*****ERROR: Need -g (genome) file. 
*****

Tool:    bedtools bedpetobam (aka bedpeToBam)
Version: v2.31.1
Summary: Converts feature records to BAM format.

Usage:   bedpetobam [OPTIONS] -i <bed/gff/vcf> -g <genome>

Options: 
	-mapq	Set the mappinq quality for the BAM records.
		(INT) Default: 255

	-ubam	Write uncompressed BAM output. Default writes compressed BAM.

Notes: 
	(1)  BED files must be at least BED4 to create BAM (needs name field).
```

## Captured Man Page

```text
No man page captured.
```

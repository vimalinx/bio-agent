# bam-to-fastq Help Reference

- Command: `bamToFastq`
- Sources: conda_bioconda
- Local executable: `/home/vimalinx/miniforge3/envs/bio/bin/bamToFastq`
- Summary: CLI installed by bioconda package bedtools.
- Package names: bedtools

## Captured Version

```text
$ bamToFastq --version
*****ERROR: Unrecognized parameter: --version *****


*****
*****ERROR: Need bam file (-i). 
*****

*****
*****ERROR: Need -fq. 
*****

Tool:    bedtools bamtofastq (aka bamToFastq)
Version: v2.31.1
Summary: Convert BAM alignments to FASTQ files. 

Usage:   bamToFastq [OPTIONS] -i <BAM> -fq <FQ> 

Options:
	-fq2	FASTQ for second end.  Used if BAM contains paired-end data.
		BAM should be sorted by query name is creating paired FASTQ.

	-tags	Create FASTQ based on the mate info
		in the BAM R2 and Q2 tags.

Tips: 
	If you want to create a single, interleaved FASTQ file 
	for paired-end data, you can just write both to /dev/stdout:

	bedtools bamtofastq -i x.bam -fq /dev/stdout -fq2 /dev/stdout > x.ilv.fq

	Also, the samtools fastq command has more fucntionality and is a useful alternative.
```

## Captured Help

```text
$ bamToFastq --help
*****ERROR: Unrecognized parameter: --help *****


*****
*****ERROR: Need bam file (-i). 
*****

*****
*****ERROR: Need -fq. 
*****

Tool:    bedtools bamtofastq (aka bamToFastq)
Version: v2.31.1
Summary: Convert BAM alignments to FASTQ files. 

Usage:   bamToFastq [OPTIONS] -i <BAM> -fq <FQ> 

Options:
	-fq2	FASTQ for second end.  Used if BAM contains paired-end data.
		BAM should be sorted by query name is creating paired FASTQ.

	-tags	Create FASTQ based on the mate info
		in the BAM R2 and Q2 tags.

Tips: 
	If you want to create a single, interleaved FASTQ file 
	for paired-end data, you can just write both to /dev/stdout:

	bedtools bamtofastq -i x.bam -fq /dev/stdout -fq2 /dev/stdout > x.ilv.fq

	Also, the samtools fastq command has more fucntionality and is a useful alternative.
```

## Captured Man Page

```text
No man page captured.
```

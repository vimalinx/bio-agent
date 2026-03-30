# complement-bed Help Reference

- Command: `complementBed`
- Sources: conda_bioconda
- Local executable: `/home/vimalinx/miniforge3/envs/bio/bin/complementBed`
- Summary: CLI installed by bioconda package bedtools.
- Package names: bedtools

## Captured Version

```text
$ complementBed --version
Tool:    bedtools complement (aka complementBed)
Version: v2.31.1
Summary: Returns the base pair complement of a feature file.

Usage:   bedtools complement [OPTIONS] -i <bed/gff/vcf> -g <genome>

Options: 
	-L	Limit output to solely the chromosomes with records in the input file.

Notes: 
	(1)  The genome file should tab delimited and structured as follows:
	     <chromName><TAB><chromSize>

	For example, Human (hg19):
	chr1	249250621
	chr2	243199373
	...
	chr18_gl000207_random	4262

Tip 1. Use samtools faidx to create a genome file from a FASTA: 
	One can the samtools faidx command to index a FASTA file.
	The resulting .fai index is suitable as a genome file, 
	as bedtools will only look at the first two, relevant columns
	of the .fai file.

	For example:
	samtools faidx GRCh38.fa
	bedtools complement -i my.bed -g GRCh38.fa.fai

Tip 2. Use UCSC Table Browser to create a genome file: 
	One can use the UCSC Genome Browser's MySQL database to extract
	chromosome sizes. For example, H. sapiens:

	mysql --user=genome --host=genome-mysql.cse.ucsc.edu -A -e \
	"select chrom, size from hg19.chromInfo"  > hg19.genome




***** ERROR: no -g genome file provided. *****
```

## Captured Help

```text
$ complementBed --help
Tool:    bedtools complement (aka complementBed)
Version: v2.31.1
Summary: Returns the base pair complement of a feature file.

Usage:   bedtools complement [OPTIONS] -i <bed/gff/vcf> -g <genome>

Options: 
	-L	Limit output to solely the chromosomes with records in the input file.

Notes: 
	(1)  The genome file should tab delimited and structured as follows:
	     <chromName><TAB><chromSize>

	For example, Human (hg19):
	chr1	249250621
	chr2	243199373
	...
	chr18_gl000207_random	4262

Tip 1. Use samtools faidx to create a genome file from a FASTA: 
	One can the samtools faidx command to index a FASTA file.
	The resulting .fai index is suitable as a genome file, 
	as bedtools will only look at the first two, relevant columns
	of the .fai file.

	For example:
	samtools faidx GRCh38.fa
	bedtools complement -i my.bed -g GRCh38.fa.fai

Tip 2. Use UCSC Table Browser to create a genome file: 
	One can use the UCSC Genome Browser's MySQL database to extract
	chromosome sizes. For example, H. sapiens:

	mysql --user=genome --host=genome-mysql.cse.ucsc.edu -A -e \
	"select chrom, size from hg19.chromInfo"  > hg19.genome
```

## Captured Man Page

```text
No man page captured.
```

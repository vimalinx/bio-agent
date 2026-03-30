# nuc-bed Help Reference

- Command: `nucBed`
- Sources: conda_bioconda
- Local executable: `/home/vimalinx/miniforge3/envs/bio/bin/nucBed`
- Summary: CLI installed by bioconda package bedtools.
- Package names: bedtools

## Captured Version

```text
$ nucBed --version
*****ERROR: Unrecognized parameter: --version *****


Tool:    bedtools nuc (aka nucBed)
Version: v2.31.1
Summary: Profiles the nucleotide content of intervals in a fasta file.

Usage:   bedtools nuc [OPTIONS] -fi <fasta> -bed <bed/gff/vcf>

Options: 
	-fi	Input FASTA file

	-bed	BED/GFF/VCF file of ranges to extract from -fi

	-s	Profile the sequence according to strand.

	-seq	Print the extracted sequence

	-pattern	Report the number of times a user-defined sequence
			is observed (case-sensitive).

	-C	Ignore case when matching -pattern. By defaulty, case matters.

	-fullHeader	Use full fasta header.
		- By default, only the word before the first space or tab is used.

Output format: 
	The following information will be reported after each BED entry:
	    1) %AT content
	    2) %GC content
	    3) Number of As observed
	    4) Number of Cs observed
	    5) Number of Gs observed
	    6) Number of Ts observed
	    7) Number of Ns observed
	    8) Number of other bases observed
	    9) The length of the explored sequence/interval.
	    10) The seq. extracted from the FASTA file. (opt., if -seq is used)
	    11) The number of times a user's pattern was observed.
	        (opt., if -pattern is used.)
```

## Captured Help

```text
$ nucBed --help
*****ERROR: Unrecognized parameter: --help *****


Tool:    bedtools nuc (aka nucBed)
Version: v2.31.1
Summary: Profiles the nucleotide content of intervals in a fasta file.

Usage:   bedtools nuc [OPTIONS] -fi <fasta> -bed <bed/gff/vcf>

Options: 
	-fi	Input FASTA file

	-bed	BED/GFF/VCF file of ranges to extract from -fi

	-s	Profile the sequence according to strand.

	-seq	Print the extracted sequence

	-pattern	Report the number of times a user-defined sequence
			is observed (case-sensitive).

	-C	Ignore case when matching -pattern. By defaulty, case matters.

	-fullHeader	Use full fasta header.
		- By default, only the word before the first space or tab is used.

Output format: 
	The following information will be reported after each BED entry:
	    1) %AT content
	    2) %GC content
	    3) Number of As observed
	    4) Number of Cs observed
	    5) Number of Gs observed
	    6) Number of Ts observed
	    7) Number of Ns observed
	    8) Number of other bases observed
	    9) The length of the explored sequence/interval.
	    10) The seq. extracted from the FASTA file. (opt., if -seq is used)
	    11) The number of times a user's pattern was observed.
	        (opt., if -pattern is used.)
```

## Captured Man Page

```text
No man page captured.
```

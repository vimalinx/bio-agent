# expand-cols Help Reference

- Command: `expandCols`
- Sources: conda_bioconda
- Local executable: `/home/vimalinx/miniforge3/envs/bio/bin/expandCols`
- Summary: CLI installed by bioconda package bedtools.
- Package names: bedtools

## Captured Version

```text
$ expandCols --version
*****ERROR: Unrecognized parameter: --version *****


*****
*****ERROR: Need -opCols.
*****

Tool:    bedtools expand 
Version: v2.31.1
Summary: Replicate lines in a file based on columns of comma-separated values.

Usage:	 bedtools expand -c [COLS] 
Options: 
	-i	Input file. Assumes "stdin" if omitted.

	-c 	Specify the column (1-based) that should be summarized.
		- Required.
Examples: 
  $ cat test.txt
  chr1	10	20	1,2,3	10,20,30
  chr1	40	50	4,5,6	40,50,60

  $ bedtools expand test.txt -c 5
  chr1	10	20	1,2,3	10
  chr1	10	20	1,2,3	20
  chr1	10	20	1,2,3	30
  chr1	40	50	4,5,6	40
  chr1	40	50	4,5,6	50
  chr1	40	50	4,5,6	60

  $ bedtools expand test.txt -c 4,5
  chr1	10	20	1	10
  chr1	10	20	2	20
  chr1	10	20	3	30
  chr1	40	50	4	40
  chr1	40	50	5	50
  chr1	40	50	6	60
```

## Captured Help

```text
$ expandCols --help
*****ERROR: Unrecognized parameter: --help *****


*****
*****ERROR: Need -opCols.
*****

Tool:    bedtools expand 
Version: v2.31.1
Summary: Replicate lines in a file based on columns of comma-separated values.

Usage:	 bedtools expand -c [COLS] 
Options: 
	-i	Input file. Assumes "stdin" if omitted.

	-c 	Specify the column (1-based) that should be summarized.
		- Required.
Examples: 
  $ cat test.txt
  chr1	10	20	1,2,3	10,20,30
  chr1	40	50	4,5,6	40,50,60

  $ bedtools expand test.txt -c 5
  chr1	10	20	1,2,3	10
  chr1	10	20	1,2,3	20
  chr1	10	20	1,2,3	30
  chr1	40	50	4,5,6	40
  chr1	40	50	4,5,6	50
  chr1	40	50	4,5,6	60

  $ bedtools expand test.txt -c 4,5
  chr1	10	20	1	10
  chr1	10	20	2	20
  chr1	10	20	3	30
  chr1	40	50	4	40
  chr1	40	50	5	50
  chr1	40	50	6	60
```

## Captured Man Page

```text
No man page captured.
```

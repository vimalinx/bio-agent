# links-bed Help Reference

- Command: `linksBed`
- Sources: conda_bioconda
- Local executable: `/home/vimalinx/miniforge3/envs/bio/bin/linksBed`
- Summary: CLI installed by bioconda package bedtools.
- Package names: bedtools

## Captured Version

```text
$ linksBed --version
*****ERROR: Unrecognized parameter: --version *****


Tool:    bedtools links (aka linksBed)
Version: v2.31.1
Summary: Creates HTML links to an UCSC Genome Browser from a feature file.

Usage:   bedtools links [OPTIONS] -i <bed/gff/vcf> > out.html

Options: 
	-base	The browser basename.  Default: http://genome.ucsc.edu 
	-org	The organism. Default: human
	-db	The build.  Default: hg18

Example: 
	By default, the links created will point to human (hg18) UCSC browser.
	If you have a local mirror, you can override this behavior by supplying
	the -base, -org, and -db options.

	For example, if the URL of your local mirror for mouse MM9 is called: 
	http://mymirror.myuniversity.edu, then you would use the following:
	-base http://mymirror.myuniversity.edu
	-org mouse
	-db mm9
```

## Captured Help

```text
$ linksBed --help
*****ERROR: Unrecognized parameter: --help *****


Tool:    bedtools links (aka linksBed)
Version: v2.31.1
Summary: Creates HTML links to an UCSC Genome Browser from a feature file.

Usage:   bedtools links [OPTIONS] -i <bed/gff/vcf> > out.html

Options: 
	-base	The browser basename.  Default: http://genome.ucsc.edu 
	-org	The organism. Default: human
	-db	The build.  Default: hg18

Example: 
	By default, the links created will point to human (hg18) UCSC browser.
	If you have a local mirror, you can override this behavior by supplying
	the -base, -org, and -db options.

	For example, if the URL of your local mirror for mouse MM9 is called: 
	http://mymirror.myuniversity.edu, then you would use the following:
	-base http://mymirror.myuniversity.edu
	-org mouse
	-db mm9
```

## Captured Man Page

```text
No man page captured.
```

# uniq-table Help Reference

- Command: `uniq-table`
- Sources: conda_bioconda
- Local executable: `/home/vimalinx/miniforge3/envs/bio/bin/uniq-table`
- Summary: CLI installed by bioconda package entrez-direct.
- Package names: entrez-direct

## Captured Version

```text
$ uniq-table --version
GNU Awk 5.4.0, API 4.1, PMA Avon 8-g1, (GNU MPFR 4.2.2, GNU MP 6.3.0)
Copyright (C) 1989, 1991-2026 Free Software Foundation.

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see http://www.gnu.org/licenses/.
```

## Captured Help

```text
$ uniq-table --help
Usage: awk [POSIX or GNU style options] -f progfile [--] file ...
Usage: awk [POSIX or GNU style options] [--] 'program' file ...
POSIX options:		GNU long options: (standard)
	-f progfile		--file=progfile
	-F fs			--field-separator=fs
	-v var=val		--assign=var=val
Short options:		GNU long options: (extensions)
	-b			--characters-as-bytes
	-c			--traditional
	-C			--copyright
	-d[file]		--dump-variables[=file]
	-D[file]		--debug[=file]
	-e 'program-text'	--source='program-text'
	-E file			--exec=file
	-g			--gen-pot
	-h			--help
	-i includefile		--include=includefile
	-I			--trace
	-k			--csv
	-l library		--load=library
	-L[fatal|invalid|no-ext]	--lint[=fatal|invalid|no-ext]
	-M			--bignum
	-N			--use-lc-numeric
	-n			--non-decimal-data
	-o[file]		--pretty-print[=file]
	-O			--optimize
	-p[file]		--profile[=file]
	-P			--posix
	-r			--re-interval
	-s			--no-optimize
	-S			--sandbox
	-t			--lint-old
	-V			--version

To report bugs, use the `gawkbug' program.
For full instructions, see the node `Bugs' in `gawk.info'
which is section `Reporting Problems and Bugs' in the
printed version.  This same information may be found at
https://www.gnu.org/software/gawk/manual/html_node/Bugs.html.
PLEASE do NOT try to report bugs by posting in comp.lang.awk,
or by using a web forum such as Stack Overflow.

Source code for gawk may be obtained from
https://ftp.gnu.org/gnu/gawk/gawk-5.4.0.tar.gz

gawk is a pattern scanning and processing language.
By default it reads standard input and writes standard output.

Examples:
	awk '{ sum += $1 }; END { print sum }' file
	awk -F: '{ print $1 }' /etc/passwd
```

## Captured Man Page

```text
No man page captured.
```

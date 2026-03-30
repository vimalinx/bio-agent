# exclude-uid-lists Help Reference

- Command: `exclude-uid-lists`
- Sources: conda_bioconda
- Local executable: `/home/vimalinx/miniforge3/envs/bio/bin/exclude-uid-lists`
- Summary: CLI installed by bioconda package entrez-direct.
- Package names: entrez-direct

## Captured Version

```text
$ exclude-uid-lists --version
Copyright (C) 2026 Free Software Foundation, Inc.
License GPLv3+: GNU GPL version 3 or later <https://gnu.org/licenses/gpl.html>.
There is NO WARRANTY, to the extent permitted by law.
This is free software: you are free to change and redistribute it.
Written by Mike Haertel and Paul Eggert.
sort (GNU coreutils) 9.10

sort: cannot read: '': No such file or directory
comm: file 1 is not in sorted order
comm: input is not in sorted order
```

## Captured Help

```text
$ exclude-uid-lists --help
]8;;https://www.gnu.org/software/coreutils/manual/coreutils.html#sort-C\[1m-C, --check=quiet, --check=silent[0m]8;;\
  ]8;;https://www.gnu.org/software/coreutils/manual/coreutils.html#sort-M\[1m-M, --month-sort[0m]8;;\
  ]8;;https://www.gnu.org/software/coreutils/manual/coreutils.html#sort-R\[1m-R, --random-sort[0m]8;;\
  ]8;;https://www.gnu.org/software/coreutils/manual/coreutils.html#sort-S\[1m-S, --buffer-size=SIZE[0m]8;;\
  ]8;;https://www.gnu.org/software/coreutils/manual/coreutils.html#sort-T\[1m-T, --temporary-directory=DIR[0m]8;;\
  ]8;;https://www.gnu.org/software/coreutils/manual/coreutils.html#sort-V\[1m-V, --version-sort[0m]8;;\
  ]8;;https://www.gnu.org/software/coreutils/manual/coreutils.html#sort-b\[1m-b, --ignore-leading-blanks[0m]8;;\
  ]8;;https://www.gnu.org/software/coreutils/manual/coreutils.html#sort-c\[1m-c, --check, --check=diagnose-first[0m]8;;\
  ]8;;https://www.gnu.org/software/coreutils/manual/coreutils.html#sort-d\[1m-d, --dictionary-order[0m]8;;\
  ]8;;https://www.gnu.org/software/coreutils/manual/coreutils.html#sort-f\[1m-f, --ignore-case[0m]8;;\
  ]8;;https://www.gnu.org/software/coreutils/manual/coreutils.html#sort-g\[1m-g, --general-numeric-sort[0m]8;;\
  ]8;;https://www.gnu.org/software/coreutils/manual/coreutils.html#sort-h\[1m-h, --human-numeric-sort[0m]8;;\
  ]8;;https://www.gnu.org/software/coreutils/manual/coreutils.html#sort-i\[1m-i, --ignore-nonprinting[0m]8;;\
  ]8;;https://www.gnu.org/software/coreutils/manual/coreutils.html#sort-k\[1m-k, --key=KEYDEF[0m]8;;\
  ]8;;https://www.gnu.org/software/coreutils/manual/coreutils.html#sort-m\[1m-m, --merge[0m]8;;\
  ]8;;https://www.gnu.org/software/coreutils/manual/coreutils.html#sort-n\[1m-n, --numeric-sort[0m]8;;\
  ]8;;https://www.gnu.org/software/coreutils/manual/coreutils.html#sort-o\[1m-o, --output=FILE[0m]8;;\
  ]8;;https://www.gnu.org/software/coreutils/manual/coreutils.html#sort-r\[1m-r, --reverse[0m]8;;\
  ]8;;https://www.gnu.org/software/coreutils/manual/coreutils.html#sort-s\[1m-s, --stable[0m]8;;\
  ]8;;https://www.gnu.org/software/coreutils/manual/coreutils.html#sort-t\[1m-t, --field-separator=SEP[0m]8;;\
  ]8;;https://www.gnu.org/software/coreutils/manual/coreutils.html#sort-u\[1m-u, --unique[0m]8;;\
  ]8;;https://www.gnu.org/software/coreutils/manual/coreutils.html#sort-z\[1m-z, --zero-terminated[0m]8;;\
      ]8;;https://www.gnu.org/software/coreutils/manual/coreutils.html#sort--batch-size\[1m--batch-size=NMERGE[0m]8;;\
      ]8;;https://www.gnu.org/software/coreutils/manual/coreutils.html#sort--compress-program\[1m--compress-program=PROG[0m]8;;\
      ]8;;https://www.gnu.org/software/coreutils/manual/coreutils.html#sort--debug\[1m--debug[0m]8;;\
      ]8;;https://www.gnu.org/software/coreutils/manual/coreutils.html#sort--files0-from\[1m--files0-from=F[0m]8;;\
      ]8;;https://www.gnu.org/software/coreutils/manual/coreutils.html#sort--parallel\[1m--parallel=N[0m]8;;\
      ]8;;https://www.gnu.org/software/coreutils/manual/coreutils.html#sort--random-source\[1m--random-source=FILE[0m]8;;\
      ]8;;https://www.gnu.org/software/coreutils/manual/coreutils.html#sort--sort\[1m--sort=WORD[0m]8;;\
      ]8;;https://www.gnu.org/software/coreutils/sort#sort--help\[1m--help[0m]8;;\
      ]8;;https://www.gnu.org/software/coreutils/sort#sort--version\[1m--version[0m]8;;\
           general-numeric -g, human-numeric -h, month -M,
           numeric -n, random -R, version -V
         If F is -, read names from standard input
         and warn about questionable usage to standard error
         annotate the part of the line used to sort,
         change the number of sorts run concurrently to N
         check for sorted input; do not sort
         compare (unknown) < 'JAN' < ... < 'DEC'
         compare according to general numerical value
         compare according to string numerical value;
         compare human readable numbers (e.g., 2K 1G)
         compress temporaries with PROG; decompress them with PROG -d
         consider only blanks and alphanumeric characters
         consider only printable characters
         display this help and exit
         fold lower case to upper case characters
         get random bytes from FILE
         ignore leading blanks when finding sort keys in each line
         like -c, but do not report first bad line
         line delimiter is NUL, not newline
         merge already sorted files; do not sort
         merge at most NMERGE inputs at once; for more use temp files
         multiple options specify multiple directories
         natural sort of (version) numbers within text
         output only the first of lines with equal keys;
         output version information and exit
         read input from the files specified by NUL-terminated names in file F;
         reverse the result of comparisons
         see full documentation for supported strings
         shuffle, but group identical keys.  See also shuf(1)
         sort according to WORD:
         sort via a key; KEYDEF gives location and type
         stabilize sort by disabling last-resort comparison
         use DIR for temporaries, not $TMPDIR or /tmp;
         use SEP instead of non-blank to blank transition
         use SIZE for main memory buffer
         with -c, check for strict ordering
         write result to FILE instead of standard output
  or:  sort [OPTION]... --files0-from=F
% 1% of memory, b 1, K 1024 (default), and so on for M, G, T, P, E, Z, Y, R, Q.
*** WARNING ***
Full documentation <https://www.gnu.org/software/coreutils/sort>
GNU coreutils home page: <https://www.gnu.org/software/coreutils/>
General help using GNU software: <https://www.gnu.org/gethelp/>
KEYDEF is F[.C][OPTS][,F[.C][OPTS]] for start and stop position, where F is a
Mandatory arguments to long options are mandatory for short options too.
Ordering options:
Other options:
Report any translation bugs to <https://translationproject.org/team/>
Report bugs to: bug-coreutils@gnu.org
SIZE may be followed by the following multiplicative suffixes:
Set LC_ALL=C to get the traditional sort order that uses
The locale specified by the environment affects sort order.
Usage: sort [OPTION]... [FILE]...
With no FILE, or when FILE is -, read standard input.
Write sorted concatenation of all FILE(s) to standard output.
effect, characters in a field are counted from the beginning of the preceding
field number and C a character position in the field; both are origin 1, and
native byte values.
or available locally via: info '(coreutils) sort invocation'
the entire line as the key.  Use --debug to diagnose incorrect key usage.
the stop position defaults to the line's end.  If neither -t nor -b is in
which override global ordering options for that key.  If no key is given, use
whitespace.  OPTS is one or more single-letter ordering options [bdfgiMhnRrV],

sort: cannot read: '': No such file or directory
comm: file 1 is not in sorted order
comm: input is not in sorted order
```

## Captured Man Page

```text
No man page captured.
```

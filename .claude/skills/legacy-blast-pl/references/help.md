# legacy-blast-pl Help Reference

- Command: `legacy_blast.pl`
- Sources: conda_bioconda
- Local executable: `/home/vimalinx/miniforge3/envs/bio/bin/legacy_blast.pl`
- Summary: CLI installed by bioconda package blast.
- Package names: blast

## Captured Version

```text
$ legacy_blast.pl --version
/home/vimalinx/miniforge3/envs/bio/bin/legacy_blast.pl version 608983
```

## Captured Help

```text
$ legacy_blast.pl --help
NAME
    legacy_blast.pl - Convert BLAST command line invocations from NCBI C
    toolkit's implementation to NCBI C++ toolkit's implementation.

SYNOPSIS
    legacy_blast.pl <C toolkit command line program and arguments>
    [--print_only] [--path /path/to/binaries] legacy_blast.pl [--version]
    legacy_blast.pl [--help]

OPTIONS
    --path
      Use the provided path as the location of the BLAST binaries to
      execute/print (default: /usr/bin).

    --print_only
      Print the equivalent command line option instead of running the
      command (default: false).

    --version
      Prints this script's version. Must be invoked as the first and only
      argument to this script.

DESCRIPTION
    This script converts and runs the equivalent NCBI C toolkit command line
    BLAST program and arguments provided to it (whenever possible) to NCBI
    C++ tookit BLAST programs. Note that to specify options to this script
    they MUST use 2 dashes to prefix the options AND be listed at the end of
    the command line invocation to convert.

EXIT CODES
    This script returns 0 on success and a non-zero value on errors.

BUGS
    Please report them to <blast-help@ncbi.nlm.nih.gov>

COPYRIGHT
    See PUBLIC DOMAIN NOTICE included at the top of this script.
```

## Captured Man Page

```text
No man page captured.
```

# rnadistance Help Reference

- Command: `RNAdistance`
- Sources: conda_bioconda
- Local executable: `/home/vimalinx/miniforge3/envs/bio/bin/RNAdistance`
- Summary: CLI installed by bioconda package viennarna.
- Package names: viennarna

## Captured Version

```text
$ RNAdistance --version
RNAdistance 2.7.2
```

## Captured Help

```text
$ RNAdistance --help
Usage: RNAdistance [OPTION]...
Calculate distances between RNA secondary structures

This program reads RNA secondary structures from stdin and calculates one or
more measures for their dissimilarity, based on tree or string editing
(alignment). In addition it calculates a "base pair distance" given by the
number of base pairs present in one structure, but not the other. For
structures of different length base pair distance is not recommended.


  -h, --help                    Print help and exit
      --detailed-help           Print help, including all details and hidden
                                  options, and exit
      --full-help               Print help, including hidden options, and exit
  -V, --version                 Print version and exit
  -v, --verbose                 Be verbose.
                                    (default=off)
  -D, --distance=fhwcFHWCP      Specify the distance representation to be used
                                  in calculations.
                                    (default=`f')
  -X, --compare=p|m|f|c         Specify the comparison directive.
                                    (default=`p')
  -S, --shapiro                 Use the Bruce Shapiro's cost matrix for
                                  comparing coarse structures.

                                    (default=off)
  -B, --backtrack[=<filename>]  Print an "alignment" with gaps of the
                                  structures, to show matching substructures.
                                  The aligned structures are written to
                                  <filename>, if specified.
                                    (default=`none')

If in doubt our program is right, nature is at fault.
Comments should be sent to rna@tbi.univie.ac.at.
```

## Captured Man Page

```text
No man page captured.
```

# rnaplot Help Reference

- Command: `RNAplot`
- Sources: conda_bioconda
- Local executable: `/home/vimalinx/miniforge3/envs/bio/bin/RNAplot`
- Summary: CLI installed by bioconda package viennarna.
- Package names: viennarna

## Captured Version

```text
$ RNAplot --version
RNAplot 2.7.2
```

## Captured Help

```text
$ RNAplot --help
Usage: RNAplot [OPTIONS] [<input0>] [<input1>]...
Draw RNA Secondary Structures

The program reads (aligned) RNA sequences and structures in the format as
produced by RNAfold or Stockholm 1.0 and produces drawings of the secondary
structure graph.
Coordinates for the structure graphs are produced using either E. Bruccoleri's
naview routines, or a simple radial layout method.
For aligned sequences and consensus structures (--msa option) the graph may be
annotated by covariance information. Additionally, a color-annotated EPS
alignment figure can be produced, similar to that obtained by RNAalifold and
RNALalifold.
If the sequence was preceded by a FASTA header, or if the multiple sequence
alignment contains an ID field, these IDs will be taken as names for the output
file(s): "name_ss.ps" and "name_aln.ps". Otherwise "rna.ps" and
"aln.ps" will be used. This behavior may be over-ruled by explicitly setting
a filename prefix using the --auto-id option.
Existing files of the same name will be overwritten.


  -h, --help                    Print help and exit
      --detailed-help           Print help, including all details and hidden
                                  options, and exit
      --full-help               Print help, including hidden options, and exit
  -V, --version                 Print version and exit
  -v, --verbose                 Be verbose.
                                    (default=off)

I/O Options:
  Command line options for input and output (pre-)processing


  -i, --infile=<filename>       Read a file instead of reading from stdin.
  -a, --msa                     Input is multiple sequence alignment in
                                  Stockholm 1.0 format.  (default=off)
      --mis                     Output "most informative sequence" instead of
                                  simple consensus  (default=off)
  -j, --jobs[=number]           Split batch input into jobs and start
                                  processing in parallel using multiple
                                  threads.  (default=`0')
  -f, --output-format=format    Specify output file format.  (possible
                                  values="eps", "svg", "gml", "xrna",
                                  "ssv" default=`eps')
      --pre=string              Add annotation macros to postscript file, and
                                  add the postscript code in "string" just
                                  before the code to draw the structure. This
                                  is an easy way to add annotation.
      --post=string             Same as --pre but in contrast to adding the
                                  annotation macros. E.g to mark position 15
                                  with circle use --post="15 cmark".
      --auto-id                 Automatically generate an ID for each sequence.
                                    (default=off)
      --id-prefix=STRING        Prefix for automatically generated IDs (as used
                                  in output file names).
                                    (default=`sequence')

Plotting:
  Command line options for changing the default behavior of structure layout
  and pairing probability plots


      --covar                   Annotate covariance of base pairs in consensus
                                  structure.

                                    (default=off)
      --aln                     Produce a colored and structure annotated
                                  alignment in PostScript format in the file
                                  "aln.ps" in the current directory.

                                    (default=off)
  -t, --layout-type=INT         Choose the plotting layout algorithm.
                                  (possible values="0", "1", "2", "3",
                                  "4" default=`1')

If in doubt our program is right, nature is at fault.
Comments should be sent to rna@tbi.univie.ac.at.
```

## Captured Man Page

```text
No man page captured.
```

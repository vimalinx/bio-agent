# rnapaln Help Reference

- Command: `RNApaln`
- Sources: conda_bioconda
- Local executable: `/home/vimalinx/miniforge3/envs/bio/bin/RNApaln`
- Summary: CLI installed by bioconda package viennarna.
- Package names: viennarna

## Captured Version

```text
$ RNApaln --version
RNApaln 2.7.2
```

## Captured Help

```text
$ RNApaln --help
Usage: RNApaln [OPTION]...
RNA alignment based on sequence base pairing propensities

Uses string-alignment techniques to perform fast pairwise structural alignments
of RNAs. Similar to RNApdist secondary structure is incorporated in an
approximate manner by computing base pair probabilities, which are then reduced
to a vector holding the probability that a base is paired upstream, downstream,
or remains unpaired. Such pair propsensity vectors can then be compared using
standard alignment algorithms. In contrast to RNApdist, RNApaln performs
similarity (instead of distance) alignments, considers both sequence and
structure information, and uses affine (rather than linear) gap costs. RNApaln
can perform semi-local alignments by using free end gaps, a true local
alignment mode is planned.

The same approach has since been used in the StraL program from Gerhard
Steeger's group. Since StraL has optimized parameters and a multiple alignment
mode, it be be currently the better option.


  -h, --help                    Print help and exit
      --detailed-help           Print help, including all details and hidden
                                  options, and exit
      --full-help               Print help, including hidden options, and exit
  -V, --version                 Print version and exit
  -v, --verbose                 Be verbose.
                                    (default=off)

I/O Options:
  Command line options for input and output (pre-)processing


  -B, --printAlignment[=filename]
                                Print an "alignment" with gaps of the
                                  profiles
                                  The aligned structures are written to
                                  filename, if specified
                                  Otherwise output is written to stdout, unless
                                  the -Xm option is set in which case
                                  "backtrack.file" is used.
                                    (default=`stdout')
      --noconv                  Do not automatically substitute nucleotide
                                  "T" with "U".

                                    (default=off)

Algorithms:
  Select additional algorithms which should be included in the calculations.

  -X, --mode=pmfc               Set the alignment mode to be used.

      --gapo=open               Set the gap open penalty


      --gape=ext                Set the gap extension penalty


      --seqw=w                  Set the weight of sequence (compared to
                                  structure) in the scoring function.


      --endgaps                 Use free end-gaps

                                    (default=off)

Energy Parameters:
  Energy parameter sets can be adapted or loaded from user-provided input files


  -T, --temp=DOUBLE             Rescale energy parameters to a temperature of
                                  temp C. Default is 37C.

                                    (default=`37.0')
  -P, --paramFile=paramfile     Read energy parameters from paramfile, instead
                                  of using the default parameter set.

      --salt=DOUBLE             Set salt concentration in molar (M). Default is
                                  1.021M.



Model Details:
  Tweak the energy model and pairing rules additionally using the following
  parameters


  -d, --dangles=INT             How to treat "dangling end" energies for
                                  bases adjacent to helices in free ends and
                                  multi-loops.
                                    (default=`2')
      --noLP                    Produce structures without lonely pairs
                                  (helices of length 1).
                                    (default=off)

If in doubt our program is right, nature is at fault.
Comments should be sent to rna@tbi.univie.ac.at.
```

## Captured Man Page

```text
No man page captured.
```

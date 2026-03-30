# rnaheat Help Reference

- Command: `RNAheat`
- Sources: conda_bioconda
- Local executable: `/home/vimalinx/miniforge3/envs/bio/bin/RNAheat`
- Summary: CLI installed by bioconda package viennarna.
- Package names: viennarna

## Captured Version

```text
$ RNAheat --version
RNAheat 2.7.2
```

## Captured Help

```text
$ RNAheat --help
Usage: RNAheat [OPTIONS] [<input0>] [<input1>]...
calculate specific heat of RNAs

Reads RNA sequences from stdin or input files and calculates their specific
heat in the temperature range t1 to t2, from the partition function by numeric
differentiation. The result is written to stdout as a list of pairs of
temperature in C and specific heat in kcal/(mol*K).
The program will continue to read new sequences until a line consisting of the
single character '@' or an end of file condition is encountered.


  -h, --help                   Print help and exit
      --detailed-help          Print help, including all details and hidden
                                 options, and exit
      --full-help              Print help, including hidden options, and exit
  -V, --version                Print version and exit
  -v, --verbose                Be verbose.
                                   (default=off)

I/O Options:
  Command line options for input and output (pre-)processing


  -i, --infile=filename        Read a file instead of reading from stdin

  -j, --jobs[=number]          Split batch input into jobs and start processing
                                 in parallel using multiple threads. A value of
                                 0 indicates to use as many parallel threads as
                                 computation cores are available.
                                   (default=`0')
      --noconv                 Do not automatically substitute nucleotide "T"
                                 with "U".

                                   (default=off)
      --auto-id                Automatically generate an ID for each sequence.
                                   (default=off)
      --id-prefix=STRING       Prefix for automatically generated IDs (as used
                                 in output file names)

                                   (default=`sequence')

Algorithms:
  Select additional algorithms which should be included in the calculations.


      --Tmin=t1                Lowest temperature.

                                   (default=`0')
      --Tmax=t2                Highest temperature.

                                   (default=`100')
      --stepsize=FLOAT         Calculate partition function every stepsize
                                 degrees C.

                                   (default=`1.')
  -m, --ipoints=ipoints        The program fits a parabola to 2*ipoints+1 data
                                 points to calculate 2nd derivatives.
                                 Increasing this parameter produces a smoother
                                 curve.

                                   (default=`2')
  -c, --circ                   Assume a circular (instead of linear) RNA
                                 molecule.

                                   (default=off)
  -g, --gquad                  Incoorporate G-Quadruplex formation into the
                                 structure prediction algorithm.

                                   (default=off)

Structure Constraints:
  Command line options to interact with the structure constraints feature of
  this program


      --maxBPspan=INT          Set the maximum base pair span.

                                   (default=`-1')

Energy Parameters:
  Energy parameter sets can be adapted or loaded from user-provided input files


  -P, --paramFile=paramfile    Read energy parameters from paramfile, instead
                                 of using the default parameter set.

      --salt=DOUBLE            Set salt concentration in molar (M). Default is
                                 1.021M.



Model Details:
  Tweak the energy model and pairing rules additionally using the following
  parameters


  -d, --dangles=INT            How to treat "dangling end" energies for bases
                                 adjacent to helices in free ends and
                                 multi-loops
                                   (default=`2')
      --noLP                   Produce structures without lonely pairs (helices
                                 of length 1).
                                   (default=off)

If in doubt our program is right, nature is at fault.
Comments should be sent to rna@tbi.univie.ac.at.
```

## Captured Man Page

```text
No man page captured.
```

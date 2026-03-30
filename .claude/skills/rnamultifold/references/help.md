# rnamultifold Help Reference

- Command: `RNAmultifold`
- Sources: conda_bioconda
- Local executable: `/home/vimalinx/miniforge3/envs/bio/bin/RNAmultifold`
- Summary: CLI installed by bioconda package viennarna.
- Package names: viennarna

## Captured Version

```text
$ RNAmultifold --version
RNAmultifold 2.7.2
```

## Captured Help

```text
$ RNAmultifold --help
Usage: RNAmultifold [OPTION]... [FILE]...
Compute secondary structures of multiple interacting RNAs

The program works much like RNAfold, but allows one to specify multiple RNA
sequences which are then allowed to form conncected components. RNA sequences
are read from stdin in the usual format, i.e. each line of input corresponds to
one sequence, except for lines starting with ">" which contain the name of
the next sequence(s).
Multiple strands must be concatenated using the '&' character as separator.
RNAmultifold can compute MFE, partition function, corresponding ensemble free
energy and base pairing probabilities. These properties are either computed for
a particular arrangement (concatenation) of sequences, for the full ensemble of
the complex of input RNAs, or all complexes formed by the input sequences up to
a specified number of interacting sequences.
Output consists of a PostScript "dot plot" file containing the pair
probabilities, see the RNAfold man page for details.
The program will continue to read new sequences until a line consisting of the
single character '@' or an end of file condition is encountered.



  -h, --help                    Print help and exit
      --detailed-help           Print help, including all details and hidden
                                  options, and exit
      --full-help               Print help, including hidden options, and exit
  -V, --version                 Print version and exit
  -v, --verbose                 Be verbose.
                                    (default=off)

I/O Options:
  Command line options for input and output (pre-)processing


  -j, --jobs[=number]           Split batch input into jobs and start
                                  processing in parallel using multiple
                                  threads. A value of 0 indicates to use as
                                  many parallel threads as computation cores
                                  are available.
                                    (default=`0')
      --noconv                  Do not automatically substitute nucleotide
                                  "T" with "U".

                                    (default=off)
      --auto-id                 Automatically generate an ID for each sequence.
                                    (default=off)
      --id-prefix=STRING        Prefix for automatically generated IDs (as used
                                  in output file names).
                                    (default=`sequence')

Algorithms:
  Select additional algorithms which should be included in the calculations.
  The Minimum free energy (MFE) and a structure representative are calculated
  in any case.


  -p, --partfunc[=INT]          Calculate the partition function and base
                                  pairing probability matrix in addition to the
                                  MFE structure. Default is calculation of mfe
                                  structure only.
                                    (default=`1')
  -a, --all_pf[=INT]            Compute the partition function and free
                                  energies not only for the complex formed by
                                  the input sequences (the "ABC... mutimer"),
                                  but also of all complexes formed by the input
                                  sequences up to the number of input
                                  sequences, e.g. AAA, AAB, ABB, BBB, etc.
                                    (default=`1')
  -c, --concentrations          In addition to everything listed under the -a
                                  option, read in initial monomer
                                  concentrations and compute the expected
                                  equilibrium concentrations of all possible
                                  species (A, B, AA, BB, AB, etc).
                                    (default=off)
  -f, --concfile=filename       Specify a file with initial concentrations for
                                  the input sequences.
      --absolute-concentrations Report absolute instead of relative
                                  concentrations

                                    (default=off)
  -g, --gquad                   Incoorporate G-Quadruplex formation into the
                                  structure prediction algorithm.
                                    (default=off)

Structure Constraints:
  Command line options to interact with the structure constraints feature of
  this program


      --maxBPspan=INT           Set the maximum base pair span.

                                    (default=`-1')

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

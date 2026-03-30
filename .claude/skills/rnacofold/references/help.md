# rnacofold Help Reference

- Command: `RNAcofold`
- Sources: conda_bioconda
- Local executable: `/home/vimalinx/miniforge3/envs/bio/bin/RNAcofold`
- Summary: CLI installed by bioconda package viennarna.
- Package names: viennarna

## Captured Version

```text
$ RNAcofold --version
RNAcofold 2.7.2
```

## Captured Help

```text
$ RNAcofold --help
Usage: RNAcofold [OPTION]... [FILE]...
calculate secondary structures of two RNAs with dimerization

The program works much like RNAfold, but allows one to specify two RNA
sequences which are then allowed to form a dimer structure. RNA sequences are
read from stdin in the usual format, i.e. each line of input corresponds to one
sequence, except for lines starting with '>' which contain the name of the next
sequence.
To compute the hybrid structure of two molecules, the two sequences must be
concatenated using the '&' character as separator.
RNAcofold can compute minimum free energy (mfe) structures, as well as
partition function (pf) and base pairing probability matrix (using the -p
switch)
Since dimer formation is concentration dependent, RNAcofold can be used to
compute equilibrium concentrations for all five monomer and (homo/hetero)-dimer
species, given input concentrations for the monomers.
Output consists of the mfe structure in bracket notation as well as PostScript
structure plots and "dot plot" files containing the pair probabilities, see
the RNAfold man page for details. In the dot plots a cross marks the chain
break between the two concatenated sequences.
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
                                  mfe structure. Default is calculation of mfe
                                  structure only.
                                    (default=`1')
  -a, --all_pf[=INT]            Compute the partition function and free
                                  energies not only of the hetero-dimer
                                  consisting of the two input sequences (the
                                  'AB dimer'), but also of the homo-dimers AA
                                  and BB as well as A and B monomers.
                                    (default=`1')
  -c, --concentrations          In addition to everything listed under the -a
                                  option, read in initial monomer
                                  concentrations and compute the expected
                                  equilibrium concentrations of the 5 possible
                                  species (AB, AA, BB, A, B).
                                    (default=off)
  -f, --concfile=filename       Specify a file with initial concentrations for
                                  the two sequences.

      --centroid                Compute the centroid structure.
                                    (default=off)
      --MEA[=gamma]             Compute MEA (maximum expected accuracy)
                                  structure.
                                    (default=`1.')
  -g, --gquad                   Incoorporate G-Quadruplex formation into the
                                  structure prediction algorithm.

                                    (default=off)

Structure Constraints:
  Command line options to interact with the structure constraints feature of
  this program


      --maxBPspan=INT           Set the maximum base pair span.

                                    (default=`-1')
  -C, --constraint[=filename]   Calculate structures subject to constraints.
                                    (default=`')
      --enforceConstraint       Enforce base pairs given by round brackets '('
                                  ')' in structure constraint.

                                    (default=off)
      --shape=filename          Use SHAPE reactivity data to guide structure
                                  predictions.


      --shapeConversion=method  Select method for SHAPE reactivity conversion.

                                    (default=`O')

Energy Parameters:
  Energy parameter sets can be adapted or loaded from user-provided input files


  -T, --temp=DOUBLE             Rescale energy parameters to a temperature of
                                  temp C. Default is 37C.

                                    (default=`37.0')
  -P, --paramFile=paramfile     Read energy parameters from paramfile, instead
                                  of using the default parameter set.

      --salt=DOUBLE             Set salt concentration in molar (M). Default is
                                  1.021M.


  -m, --modifications[=STRING]  Allow for modified bases within the RNA
                                  sequence string.
                                    (default=`7I6P9D')
      --mod-file=STRING         Use additional modified base data from JSON
                                  file.



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

Plotting:
  Command line options for changing the default behavior of structure layout
  and pairing probability plots


      --noPS                    Do not produce postscript drawing of the mfe
                                  structure.

                                    (default=off)

If in doubt our program is right, nature is at fault.
Comments should be sent to rna@tbi.univie.ac.at.
```

## Captured Man Page

```text
No man page captured.
```

# rnafold Help Reference

- Command: `RNAfold`
- Sources: conda_bioconda, path, tool_reference
- Local executable: `/home/vimalinx/miniforge3/envs/bio/bin/RNAfold`
- Summary: Predict RNA secondary structure and minimum free energy folds.
- Package names: viennarna

## Captured Version

```text
$ RNAfold --version
RNAfold 2.7.2
```

## Captured Help

```text
$ RNAfold --help
Usage: RNAfold [OPTIONS] [<input0.fa>] [<input1.fa>]...
Calculate minimum free energy secondary structures and partition function of
RNAs

The program reads RNA sequences, calculates their minimum free energy (mfe)
structure and prints the mfe structure in bracket notation and its free energy.
If not specified differently using commandline arguments, input is accepted
from stdin or read from an input file, and output printed to stdout. If the -p
option was given it also computes the partition function (pf) and base pairing
probability matrix, and prints the free energy of the thermodynamic ensemble,
the frequency of the mfe structure in the ensemble, and the ensemble diversity
to stdout.

It also produces PostScript files with plots of the resulting secondary
structure graph and a "dot plot" of the base pairing matrix.
The dot plot shows a matrix of squares with area proportional to the pairing
probability in the upper right half, and one square for each pair in the
minimum free energy structure in the lower left half. For each pair i-j with
probability p>10E-6 there is a line of the form

i  j  sqrt(p)  ubox

in the PostScript file, so that the pair probabilities can be easily extracted.

Sequences may be provided in a simple text format where each sequence occupies
a single line. Output files are named "rna.ps" and "dot.ps". Existing files
of the same name will be overwritten.

It is also possible to provide sequence data in FASTA format. In this case, the
first word of the FASTA header will be used as prefix for output file names.
PostScript files "prefix_ss.ps" and "prefix_dp.ps" are produced for the
structure and dot plot, respectively. Note, however, that once FASTA input was
provided all following sequences must be in FASTA format too.

To avoid problems with certain operating systems and/or file systems the prefix
will ALWAYS be sanitized! This step substitutes any special character in the
prefix by a filename delimiter. See the --filename-delim option to change the
delimiting character according to your requirements.

The program will continue to read new sequences until a line consisting of the
single character '@' or an end of file (EOF) condition is encountered.



  -h, --help                    Print help and exit
      --detailed-help           Print help, including all details and hidden
                                  options, and exit
      --full-help               Print help, including hidden options, and exit
  -V, --version                 Print version and exit
  -v, --verbose                 Be verbose.
                                    (default=off)

I/O Options:
  Command line options for input and output (pre-)processing


  -i, --infile=filename         Read a file instead of reading from stdin.

  -o, --outfile[=filename]      Print output to file instead of stdout.

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
                                  pairing probability matrix.
                                    (default=`1')
      --MEA[=gamma]             Compute MEA (maximum expected accuracy)
                                  structure.
                                    (default=`1.')
  -c, --circ                    Assume a circular (instead of linear) RNA
                                  molecule.

                                    (default=off)
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

Experimental Structure Probing Data:
  The following arguments and siwtches control various implementations that
  allow for guiding the structure prediction with the help of additional
  (experimental) RNA structure probing data, such as SHAPE, DMS, etc.


      --sp-data=filename        Read structure probing data from an input file
                                  and guide the predictions accordingly. Must
                                  precede the strategy, i.e. a data file must
                                  be specified before the corresponding
                                  --sp-strategy option!


      --sp-strategy=strategy    Select the strategy how the probing data is
                                  used to guide the structure predictions.

                                    (default=`D')
      --shape=filename          Use SHAPE reactivity data to guide structure
                                  predictions.



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
      --noDP                    Do not produce dot-plot postscript file
                                  containing base pair or stack
                                  probabilitities.
                                    (default=off)

If in doubt our program is right, nature is at fault.
Comments should be sent to rna@tbi.univie.ac.at.
```

## Captured Man Page

```text
No man page captured.
```

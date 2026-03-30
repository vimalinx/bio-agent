# rnalfold Help Reference

- Command: `RNALfold`
- Sources: conda_bioconda
- Local executable: `/home/vimalinx/miniforge3/envs/bio/bin/RNALfold`
- Summary: CLI installed by bioconda package viennarna.
- Package names: viennarna

## Captured Version

```text
$ RNALfold --version
RNALfold 2.7.2
```

## Captured Help

```text
$ RNALfold --help
Usage: RNALfold [OPTION]...
calculate locally stable secondary structures of RNAs

Compute locally stable RNA secondary structure with a maximal base pair span.
For a sequence of length n and a base pair span of L the algorithm uses only
O(n+L*L) memory and O(n*L*L) CPU time. Thus it is practical to "scan" very
large genomes for short RNA structures.
Output consists of a list of secondary structure components of size <= L, one
entry per line. Each output line contains the predicted local structure its
energy in kcal/mol and the starting position of the local structure.


  -h, --help                    Print help and exit
      --detailed-help           Print help, including all details and hidden
                                  options, and exit
      --full-help               Print help, including hidden options, and exit
  -V, --version                 Print version and exit
  -v, --verbose                 Be verbose.
                                    (default=off)

I/O Options:
  Command line options for input and output (pre-)processing


  -i, --infile=filename         Read a file instead of reading from stdin

  -o, --outfile[=filename]      Print output to file instead of stdout.

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


  -L, --span=INT                Set the maximum distance between any two
                                  pairing nucleotides.
                                    (default=`150')
  -z, --zscore[=DOUBLE]         Limit the output to predictions with a Z-score
                                  below a threshold.
                                    (default=`-2')
      --zscore-pre-filter       Apply the z-score filtering in the forward
                                  recursions.
                                    (default=off)
      --zscore-report-subsumed  Report subsumed structures if their z-score is
                                  less than that of the enclosing structure.
                                    (default=off)
  -b, --backtrack-global        Backtrack a global MFE structure.
                                    (default=off)
  -g, --gquad                   Incoorporate G-Quadruplex formation into the
                                  structure prediction algorithm.

                                    (default=off)

Structure Constraints:
  Command line options to interact with the structure constraints feature of
  this program


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

If in doubt our program is right, nature is at fault.
Comments should be sent to rna@tbi.univie.ac.at.
```

## Captured Man Page

```text
No man page captured.
```

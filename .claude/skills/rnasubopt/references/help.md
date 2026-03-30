# rnasubopt Help Reference

- Command: `RNAsubopt`
- Sources: conda_bioconda
- Local executable: `/home/vimalinx/miniforge3/envs/bio/bin/RNAsubopt`
- Summary: CLI installed by bioconda package viennarna.
- Package names: viennarna

## Captured Version

```text
$ RNAsubopt --version
RNAsubopt 2.7.2
```

## Captured Help

```text
$ RNAsubopt --help
Usage: RNAsubopt [OPTION]...
calculate suboptimal secondary structures of RNAs

Reads RNA sequences from stdin and (in the default -e mode) calculates all
suboptimal secondary structures within a user defined energy range above the
minimum free energy (mfe). It prints the suboptimal structures in dot-bracket
notation followed by the energy in kcal/mol to stdout. Be careful, the number
of structures returned grows exponentially with both sequence length and energy
range.

Alternatively, when used with the -p option, RNAsubopt produces Boltzmann
weighted samples of secondary structures.


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

      --noconv                  Do not automatically substitute nucleotide
                                  "T" with "U".

                                    (default=off)
      --auto-id                 Automatically generate an ID for each sequence.
                                    (default=off)
      --id-prefix=STRING        Prefix for automatically generated IDs (as used
                                  in output file names).
                                    (default=`sequence')

Algorithms:
  Select the algorithms which should be applied to the given RNA sequence(s).


  -e, --deltaEnergy=range       Compute suboptimal structures with energy in a
                                  certain range of the optimum (kcal/mol).

  -s, --sorted                  Sort the suboptimal structures by energy and
                                  lexicographical order.
                                    (default=off)
  -p, --stochBT=number          Randomly draw structures according to their
                                  probability in the Boltzmann ensemble.

  -N, --nonRedundant            Enable non-redundant sampling strategy.

                                    (default=off)
  -c, --circ                    Assume a circular (instead of linear) RNA
                                  molecule.

                                    (default=off)
  -D, --dos                     Compute density of states instead of secondary
                                  structures.
                                    (default=off)
  -z, --zuker                   Compute Zuker suboptimals instead of all
                                  suboptimal structures within an energy band
                                  around the MFE.

                                    (default=off)
  -g, --gquad                   Incoorporate G-Quadruplex formation.
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
      --logML                   Recompute energies of structures using a
                                  logarithmic energy function for multi-loops
                                  before output.  (default=off)

If in doubt our program is right, nature is at fault.
Comments should be sent to rna@tbi.univie.ac.at.
```

## Captured Man Page

```text
No man page captured.
```

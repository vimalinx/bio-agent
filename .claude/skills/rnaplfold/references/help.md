# rnaplfold Help Reference

- Command: `RNAplfold`
- Sources: conda_bioconda
- Local executable: `/home/vimalinx/miniforge3/envs/bio/bin/RNAplfold`
- Summary: CLI installed by bioconda package viennarna.
- Package names: viennarna

## Captured Version

```text
$ RNAplfold --version
RNAplfold 2.7.2
```

## Captured Help

```text
$ RNAplfold --help
Usage: RNAplfold [OPTION]...
calculate locally stable secondary structure - pair probabilities

Computes local pair probabilities for base pairs with a maximal span of L. The
probabilities are averaged over all windows of size L that contain the base
pair. For a sequence of length n and a window size of L the algorithm uses only
O(n+L*L) memory and O(n*L*L) CPU time. Thus it is practical to "scan" very
large genomes for short stable RNA structures.


  -h, --help                    Print help and exit
      --detailed-help           Print help, including all details and hidden
                                  options, and exit
      --full-help               Print help, including hidden options, and exit
  -V, --version                 Print version and exit
  -v, --verbose                 Be verbose.
                                    (default=off)

I/O Options:
  Command line options for input and output (pre-)processing


  -c, --cutoff=FLOAT            Report only base pairs with an average
                                  probability larger than 'cutoff' in the dot
                                  plot.

                                    (default=`0.01')
  -o, --print_onthefly          Save memory by printing out everything during
                                  computation.
                                    (default=off)
  -O, --opening_energies        Switch output from probabilities to their
                                  logarithms.
                                    (default=off)
      --noconv                  Do not automatically substitute nucleotide
                                  "T" with "U".

                                    (default=off)
      --auto-id                 Automatically generate an ID for each sequence.
                                    (default=off)
      --id-prefix=STRING        Prefix for automatically generated IDs (as used
                                  in output file names).
                                    (default=`sequence')

Algorithms:
  Select and change parameters of (additional) algorithms which should be
  included in the calculations.


  -W, --winsize=size            Average the pair probabilities over windows of
                                  given size.

                                    (default=`70')
  -L, --span=size               Set the maximum allowed separation of a base
                                  pair to span.

  -u, --ulength=length          Compute the mean probability that regions of
                                  length 1 to a given length are unpaired.
                                    (default=`31')

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


  -d, --dangles=INT             Specify "dangling end" model for bases
                                  adjacent to helices in free ends and
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

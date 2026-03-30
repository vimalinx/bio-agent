# rnapdist Help Reference

- Command: `RNApdist`
- Sources: conda_bioconda
- Local executable: `/home/vimalinx/miniforge3/envs/bio/bin/RNApdist`
- Summary: CLI installed by bioconda package viennarna.
- Package names: viennarna

## Captured Version

```text
$ RNApdist --version
RNApdist 2.7.2
```

## Captured Help

```text
$ RNApdist --help
Usage: RNApdist [OPTION]...
Calculate distances between thermodynamic RNA secondary structures ensembles

This program reads RNA sequences from stdin and calculates structure distances
between the thermodynamic ensembles of their secondary structures.


  -h, --help                    Print help and exit
      --detailed-help           Print help, including all details and hidden
                                  options, and exit
      --full-help               Print help, including hidden options, and exit
  -V, --version                 Print version and exit
  -v, --verbose                 Be verbose.
                                    (default=off)

I/O Options:
  Command line options for input and output (pre-)processing


      --noconv                  Do not automatically substitute nucleotide
                                  "T" with "U".

                                    (default=off)

Algorithms:
  Select additional algorithms which should be included in the calculations.


  -X, --compare=p|m|f|c         Specify the comparison directive.
                                    (default=`p')
  -B, --backtrack[=<filename>]  Print an "alignment" with gaps of the
                                  profiles. The aligned structures are written
                                  to <filename>, if specified.
                                    (default=`none')

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


  -d, --dangles=INT             set energy model for treatment of dangling
                                  bases.

                                    (possible values="0", "2" default=`2')
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

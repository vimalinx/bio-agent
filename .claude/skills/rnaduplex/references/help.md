# rnaduplex Help Reference

- Command: `RNAduplex`
- Sources: conda_bioconda
- Local executable: `/home/vimalinx/miniforge3/envs/bio/bin/RNAduplex`
- Summary: CLI installed by bioconda package viennarna.
- Package names: viennarna

## Captured Version

```text
$ RNAduplex --version
RNAduplex 2.7.2
```

## Captured Help

```text
$ RNAduplex --help
Usage: RNAduplex [OPTION]...
Compute the structure upon hybridization of two RNA strands

reads two RNA sequences from stdin or <filename> and computes optimal and
suboptimal secondary structures for their hybridization. The calculation is
simplified by allowing only inter-molecular base pairs, for the general case
use RNAcofold.
The computed optimal and suboptimal structure are written to stdout, one
structure per line. Each line consist of: The structure in dot bracket format
with a '&' separating the two strands. The range of the structure in the two
sequences in the format  "from,to : from,to"; the energy of duplex structure
in kcal/mol.
The format is especially useful for computing the hybrid structure between a
small probe sequence and a long target sequence.


  -h, --help                   Print help and exit
      --detailed-help          Print help, including all details and hidden
                                 options, and exit
      --full-help              Print help, including hidden options, and exit
  -V, --version                Print version and exit
  -v, --verbose                Be verbose.
                                   (default=off)

I/O Options:
  Command line options for input and output (pre-)processing


  -s, --sorted                 Sort the printed output by free energy.

                                   (default=off)
      --noconv                 Do not automatically substitute nucleotide "T"
                                 with "U".

                                   (default=off)

Algorithms:
  Select additional algorithms which should be included in the calculations.


  -e, --deltaEnergy=range      Compute suboptimal structures with energy in a
                                 certain range of the optimum (kcal/mol).
                                 Default is calculation of mfe structure only.



Energy Parameters:
  Energy parameter sets can be adapted or loaded from user-provided input files


  -T, --temp=DOUBLE            Rescale energy parameters to a temperature of
                                 temp C. Default is 37C.

                                   (default=`37.0')
  -P, --paramFile=paramfile    Read energy parameters from paramfile, instead
                                 of using the default parameter set.

      --salt=DOUBLE            Set salt concentration in molar (M). Default is
                                 1.021M.



Model Details:
  Tweak the energy model and pairing rules additionally using the following
  parameters


  -d, --dangles=INT            How to treat "dangling end" energies for bases
                                 adjacent to helices in free ends and
                                 multi-loops.
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

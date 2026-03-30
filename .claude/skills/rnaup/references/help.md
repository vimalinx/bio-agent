# rnaup Help Reference

- Command: `RNAup`
- Sources: conda_bioconda
- Local executable: `/home/vimalinx/miniforge3/envs/bio/bin/RNAup`
- Summary: CLI installed by bioconda package viennarna.
- Package names: viennarna

## Captured Version

```text
$ RNAup --version
RNAup 2.7.2
```

## Captured Help

```text
$ RNAup --help
Usage: RNAup [OPTION]...
Calculate the thermodynamics of RNA-RNA interactions

RNAup calculates the thermodynamics of RNA-RNA interactions, by decomposing the
binding into two stages. (1) First the probability that a potential binding
sites remains unpaired (equivalent to the free energy needed to open the site)
is computed. (2) Then this accessibility is combined with the interaction
energy to obtain the total binding energy. All calculations are done by
computing partition functions over all possible conformations.


  -h, --help                   Print help and exit
      --detailed-help          Print help, including all details and hidden
                                 options, and exit
      --full-help              Print help, including hidden options, and exit
  -V, --version                Print version and exit
  -v, --verbose                Be verbose.
                                   (default=off)

I/O Options:
  Command line options for input and output (pre-)processing


  -o, --no_output_file         Do not produce an output file.

                                   (default=off)
      --no_header              Do not produce a header with the command line
                                 parameters used in the outputfile.

                                   (default=off)
      --noconv                 Do not automatically substitute nucleotide "T"
                                 with "U".

                                   (default=off)

Algorithms:
  Select additional algorithms which should be included in the calculations.


  -u, --ulength=length         Specify the length of the unstructured region in
                                 the output.
                                   (default=`4')
  -c, --contributions=SHIME    Specify the contributions listed in the output.
                                   (default=`S')

Calculations of RNA-RNA interactions:
  -w, --window=INT             Set the maximal length of the region of
                                 interaction.

                                   (default=`25')
  -b, --include_both           Include the probability of unpaired regions in
                                 both (b) RNAs.
                                   (default=off)
  -5, --extend5=INT            Extend the region of interaction in the target
                                 to some residues on the 5' side.

  -3, --extend3=INT            Extend the region of interaction in the target
                                 to some residues on the 3' side.

      --interaction_pairwise   Activate pairwise interaction mode.
                                   (default=off)
      --interaction_first      Activate interaction mode using first sequence
                                 only.
                                   (default=off)

Structure Constraints:
  Command line options to interact with the structure constraints feature of
  this program


  -C, --constraint             Apply structural constraint(s) during
                                 prediction.
                                   (default=off)

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


  -d, --dangles=INT            Specify "dangling end" model for bases
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

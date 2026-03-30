# rnaaliduplex Help Reference

- Command: `RNAaliduplex`
- Sources: conda_bioconda
- Local executable: `/home/vimalinx/miniforge3/envs/bio/bin/RNAaliduplex`
- Summary: CLI installed by bioconda package viennarna.
- Package names: viennarna

## Captured Version

```text
$ RNAaliduplex --version
RNAaliduplex 2.7.2
```

## Captured Help

```text
$ RNAaliduplex --help
Usage: RNAaliduplex [options] <file1.aln> <file2.aln>
Predict conserved RNA-RNA interactions between two alignments

The program reads two alignments of RNA sequences in CLUSTAL format and
predicts optimal and suboptimal binding sites, hybridization energies and the
corresponding structures. The calculation takes only inter-molecular base pairs
into account, for the general case use RNAcofold. The use of alignments allows
one to focus on binding sites that are evolutionary conserved. Note, that the
two input alignments need to have equal number of sequences and the same order,
i.e. the 1st sequence in file1 will be hybridized to the 1st in file2 etc.

The computed binding sites, energies, and structures are written to stdout, one
structure per line. Each line consist of: The structure in dot bracket format
with a "&" separating the two strands. The range of the structure in the two
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

Algorithms:
  Select additional algorithms which should be included in the calculations.


  -e, --deltaEnergy=range      Compute suboptimal structures with energy in a
                                 certain range of the optimum (kcal/mol).
                                 Default is calculation of mfe structure only.


  -s, --sorted                 Sort output by free energy.

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

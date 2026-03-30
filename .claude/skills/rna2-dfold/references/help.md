# rna2-dfold Help Reference

- Command: `RNA2Dfold`
- Sources: conda_bioconda
- Local executable: `/home/vimalinx/miniforge3/envs/bio/bin/RNA2Dfold`
- Summary: CLI installed by bioconda package viennarna.
- Package names: viennarna

## Captured Version

```text
$ RNA2Dfold --version
RNA2Dfold 2.7.2
```

## Captured Help

```text
$ RNA2Dfold --help
Usage: RNA2Dfold [OPTION]...
Compute MFE structure, partition function and representative sample structures
of k,l neighborhoods

The program partitions the secondary structure space into (basepair)distance
classes according to two fixed reference structures. It expects a sequence and
two secondary structures in dot-bracket notation as its inputs. For each
distance class, the MFE representative, Boltzmann probabilities and Gibbs free
energy is computed. Additionally, a stochastic backtracking routine allows one
to produce samples of representative suboptimal secondary structures from each
partition



  -h, --help                   Print help and exit
      --detailed-help          Print help, including all details and hidden
                                 options, and exit
      --full-help              Print help, including hidden options, and exit
  -V, --version                Print version and exit
  -v, --verbose                Be verbose.
                                   (default=off)

I/O Options:
  Command line options for input and output (pre-)processing


  -j, --numThreads=INT         Set the number of threads used for calculations
                                 (only available when compiled with OpenMP
                                 support)


      --noconv                 Do not automatically substitute nucleotide "T"
                                 with "U".

                                   (default=off)

Algorithms:
  Select additional algorithms which should be included in the calculations.
  The Minimum free energy (MFE) and a structure representative are calculated
  in any case.


  -p, --partfunc               calculate partition function and thus, Boltzmann
                                 probabilities and Gibbs free energy

                                   (default=off)
      --stochBT=INT            backtrack a certain number of Boltzmann samples
                                 from the appropriate k,l neighborhood(s)


      --neighborhood=<k>:<l>   backtrack structures from certain
                                 k,l-neighborhood only, can be specified
                                 multiple times (<k>:<l>,<m>:<n>,...)


  -K, --maxDist1=INT           maximum distance to first reference structure
  -L, --maxDist2=INT           maximum distance to second reference structure
      --noBT                   do not backtrack structures, calculate energy
                                 contributions only

                                   (default=off)
  -c, --circ                   Assume a circular (instead of linear) RNA
                                 molecule.

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
                                 multi-loops
                                   (possible values="0", "2" default=`2')

If in doubt our program is right, nature is at fault.
Comments should be sent to rna@tbi.univie.ac.at.
```

## Captured Man Page

```text
No man page captured.
```

# rnapkplex Help Reference

- Command: `RNAPKplex`
- Sources: conda_bioconda
- Local executable: `/home/vimalinx/miniforge3/envs/bio/bin/RNAPKplex`
- Summary: CLI installed by bioconda package viennarna.
- Package names: viennarna

## Captured Version

```text
$ RNAPKplex --version
RNAPKplex 2.7.2
```

## Captured Help

```text
$ RNAPKplex --help
Usage: RNAPKplex [OPTION]...
predicts RNA secondary structures including pseudoknots

Computes RNA secondary structures by first making two sequence intervals
accessible and unpaired using the algorithm of RNAplfold and then calculating
the energy of the interaction of those two intervals. The algorithm uses
O(n^2*w^4) CPU time and O(n*w^2) memory space.
The algorithm furthermore always considers dangle=2 model.


  -h, --help                   Print help and exit
      --detailed-help          Print help, including all details and hidden
                                 options, and exit
      --full-help              Print help, including hidden options, and exit
  -V, --version                Print version and exit
  -v, --verbose                Be verbose.
                                   (default=off)

I/O Options:
  Command line options for input and output (pre-)processing


      --noconv                 Do not automatically substitute nucleotide "T"
                                 with "U".

                                   (default=off)

Algorithms:
  Select additional algorithms which should be included in the calculations.


  -c, --cutoff=FLOAT           Only consider unpaired probabities > cutoff for
                                 putative PK sites.

                                   (default=`1e-6')
  -e, --energyCutoff=DOUBLE    Energy cutoff or pseudoknot initiation cost.
                                 Minimum energy gain of a pseudoknot
                                 interaction for it to be returned. Pseudoknots
                                 with smaller energy gains are rejected.

                                   (default=`-8.10')
  -s, --subopts=DOUBLE         print suboptimal structures whose energy
                                 difference of the pseudoknot to the optimum
                                 pseudoknot is smaller than the given value.
                                   (default=`0.0')

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

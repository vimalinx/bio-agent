# rnados Help Reference

- Command: `RNAdos`
- Sources: conda_bioconda
- Local executable: `/home/vimalinx/miniforge3/envs/bio/bin/RNAdos`
- Summary: CLI installed by bioconda package viennarna.
- Package names: viennarna

## Captured Version

```text
$ RNAdos --version
RNAdos 2.7.2
```

## Captured Help

```text
$ RNAdos --help
Usage: RNAdos [OPTIONS]
Calculate the density of states for each energy band of an RNA

The program reads an RNA sequence and computes the density of states for each
energy band.



  -h, --help                   Print help and exit
      --detailed-help          Print help, including all details and hidden
                                 options, and exit
      --full-help              Print help, including hidden options, and exit
  -V, --version                Print version and exit
  -v, --verbose                Be verbose.
                                   (default=off)

I/O Options:
  Command line options for input and output (pre-)processing


  -s, --sequence=STRING        The RNA sequence (ACGU).

  -j, --numThreads=INT         Set the number of threads used for calculations
                                 (only available when compiled with OpenMP
                                 support)



Algorithms:
  Select additional algorithms which should be included in the calculations.
  The Minimum free energy (MFE) and a structure representative are calculated
  in any case.


  -e, --max-energy=INT         Structures are only counted until this threshold
                                 is reached. Default is 0 kcal/mol.
                                   (default=`0')

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

If in doubt our program is right, nature is at fault.
Comments should be sent to rna@tbi.univie.ac.at.
```

## Captured Man Page

```text
No man page captured.
```

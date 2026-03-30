# rnaparconv Help Reference

- Command: `RNAparconv`
- Sources: conda_bioconda
- Local executable: `/home/vimalinx/miniforge3/envs/bio/bin/RNAparconv`
- Summary: CLI installed by bioconda package viennarna.
- Package names: viennarna

## Captured Version

```text
$ RNAparconv --version
RNAparconv 2.7.2
```

## Captured Help

```text
$ RNAparconv --help
Usage: RNAparconv [options] [<input file>] [<output file>]

Convert energy parameter files from ViennaRNA 1.8.4 to 2.0 format

Converts energy parameter files from "old" ViennaRNAPackage 1.8.4 format to
the new format used since ViennaRNAPackage 2.0.
The Program reads a valid energy parameter file or valid energy parameters from
stdin and prints the converted energy parameters to stdout or a specified
output file. Per default, the converted output file contains the whole set of
energy parameters used throughout ViennaRNAPackage 1.8.4. The user can specify
sets of energy parameters that should not be included in the output.


  -h, --help                 Print help and exit
      --detailed-help        Print help, including all details and hidden
                               options, and exit
      --full-help            Print help, including hidden options, and exit
  -V, --version              Print version and exit
  -v, --verbose              Be verbose.
                                 (default=off)

I/O Options:
  Command line options for input and output (pre-)processing


  -i, --input=filename       Specify an input file name. If argument is missing
                               the energy parameter input can be supplied via
                               'stdin'.


  -o, --output=filename      Specify an output file name. If argument is
                               missing the converted energy parameters are
                               printed to 'stdout'.


      --vanilla              Print just as much as needed to represent the
                               given energy parameters data set.
                               This option overrides all other output settings!

                                 (default=off)
      --dump                 Just dump Vienna 1.8.4 energy parameters in format
                               used since 2.0.
                               This option skips any energy parameter input!

                                 (default=off)
      --silent               Print just energy parameters and appropriate
                               comment lines but suppress all other output

                                 (default=off)

If in doubt our program is right, nature is at fault.
Comments should be sent to rna@tbi.univie.ac.at.
```

## Captured Man Page

```text
No man page captured.
```

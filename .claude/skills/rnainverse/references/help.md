# rnainverse Help Reference

- Command: `RNAinverse`
- Sources: conda_bioconda
- Local executable: `/home/vimalinx/miniforge3/envs/bio/bin/RNAinverse`
- Summary: CLI installed by bioconda package viennarna.
- Package names: viennarna

## Captured Version

```text
$ RNAinverse --version
RNAinverse 2.7.2
```

## Captured Help

```text
$ RNAinverse --help
Usage: RNAinverse [OPTION]...
Find RNA sequences with given secondary structure

The program searches for sequences folding into a predefined structure, thereby
inverting the folding algorithm. Target structures (in bracket notation) and
starting sequences for the search are read alternately from stdin.
Characters in the start sequence other than "AUGC" (or the alphabet specified
with -a) will be treated as wild cards and replaced by a random character. Any
lower case characters in the start sequence will be kept fixed during the
search. If necessary, the sequence will be elongated to the length of the
structure. Thus a string of "N"s as well as a blank line specify a random
start sequence.
For each search the best sequence found and its Hamming distance to the start
sequence are printed to stdout. If the the search was unsuccessful, a structure
distance to the target is appended.
The -Fp and -R options can modify the output format, see commandline options
below.
The program will continue to read new structures and sequences until a line
consisting of the single character "@" or an end of file condition is
encountered.


  -h, --help                   Print help and exit
      --detailed-help          Print help, including all details and hidden
                                 options, and exit
      --full-help              Print help, including hidden options, and exit
  -V, --version                Print version and exit
  -v, --verbose                In conjunction with a negative value supplied to
                                 -R, print the last subsequence and
                                 substructure for each unsuccessful search.
                                   (default=off)

Algorithms:
  Select additional algorithms which should be included in the calculations.


  -F, --function=mp            Use minimum energy (-Fm), partition function
                                 folding (-Fp) or both (-Fmp).
                                   (default=`m')
  -f, --final=FLOAT            In combination with -Fp stop search when
                                 sequence is found with E(s)-F is smaller than
                                 final, where F=-kT*ln(Q).


  -R, --repeat[=INT]           Search repeatedly for the same structure.
                                 If an argument is supplied to this option it
                                 must follow the option flag immediately. E.g.:
                                 -R5
                                   (default=`1')
  -a, --alphabet=ALPHABET      Find sequences using only nucleotides from a
                                 given alphabet.



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
                                   (default=`2')

If in doubt our program is right, nature is at fault.
Comments should be sent to rna@tbi.univie.ac.at.
```

## Captured Man Page

```text
No man page captured.
```

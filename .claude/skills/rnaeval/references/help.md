# rnaeval Help Reference

- Command: `RNAeval`
- Sources: conda_bioconda
- Local executable: `/home/vimalinx/miniforge3/envs/bio/bin/RNAeval`
- Summary: CLI installed by bioconda package viennarna.
- Package names: viennarna

## Captured Version

```text
$ RNAeval --version
RNAeval 2.7.2
```

## Captured Help

```text
$ RNAeval --help
Usage: RNAeval [OPTIONS] [<input0>] [<input1>]...
Determine the free energy of a (consensus) secondary structure for (an
alignment of) RNA sequence(s)

Evaluates the free energy of a particular (consensus) secondary structure for
an (an alignment of) RNA molecule(s). The energy unit is kcal/mol and contains
a covariance pseudo-energy term for multiple sequence alignments (--msa option)
and corresponding consensus structures.
The program will continue to read new sequences and structures until a line
consisting of the single character '@' or an end of file condition is
encountered.
If the input sequence or structure contains the separator character '&' the
program calculates the energy of the co-folding of two RNA strands, where the
'&' marks the boundary between the two strands.


  -h, --help                    Print help and exit
      --detailed-help           Print help, including all details and hidden
                                  options, and exit
      --full-help               Print help, including hidden options, and exit
  -V, --version                 Print version and exit
  -v, --verbose                 Be verbose and print out energy contribution of
                                  each loop in the structure.
                                    (default=off)

I/O Options:
  Command line options for input and output (pre-)processing


  -i, --infile=filename         Read a file instead of reading from stdin.

  -a, --msa                     Input is multiple sequence alignment in
                                  Stockholm 1.0 format.
                                    (default=off)
      --mis                     Output "most informative sequence" instead of
                                  simple consensus: For each column of the
                                  alignment output the set of nucleotides with
                                  frequency greater than average in IUPAC
                                  notation.

                                    (default=off)
  -j, --jobs[=number]           Split batch input into jobs and start
                                  processing in parallel using multiple
                                  threads. A value of 0 indicates to use as
                                  many parallel threads as computation cores
                                  are available.
                                    (default=`0')
      --noconv                  Do not automatically substitute nucleotide
                                  "T" with "U".

                                    (default=off)
      --auto-id                 Automatically generate an ID for each sequence.
                                    (default=off)
      --id-prefix=STRING        Prefix for automatically generated IDs (as used
                                  in output file names).
                                    (default=`sequence')

Algorithms:
  Select additional algorithmic details which should be included in the
  calculations.


  -c, --circ                    Assume a circular (instead of linear) RNA
                                  molecule.

                                    (default=off)
  -g, --gquad                   Incoorporate G-Quadruplex formation into the
                                  structure prediction algorithm.

                                    (default=off)

Structure Constraints:
  Command line options to interact with the structure constraints feature of
  this program


      --shape=filename          Use SHAPE reactivity data to guide structure
                                  predictions.


      --shapeConversion=method  Select method for SHAPE reactivity conversion.

                                    (default=`O')

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


  -d, --dangles=INT             How to treat "dangling end" energies for
                                  bases adjacent to helices in free ends and
                                  multi-loops.
                                    (default=`2')
      --logML                   Recalculate energies of structures using a
                                  logarithmic energy function for multi-loops
                                  before output.
                                    (default=off)
      --cfactor=DOUBLE          Set the weight of the covariance term in the
                                  energy function

                                    (default=`1.0')
      --nfactor=DOUBLE          Set the penalty for non-compatible sequences in
                                  the covariance term of the energy function

                                    (default=`1.0')
  -R, --ribosum_file=ribosumfile
                                use specified Ribosum Matrix instead of normal
                                  energy model.

  -r, --ribosum_scoring         use ribosum scoring matrix.
                                    (default=off)
      --old                     use old energy evaluation, treating gaps as
                                  characters.

                                    (default=off)

If in doubt our program is right, nature is at fault.
Comments should be sent to rna@tbi.univie.ac.at.
```

## Captured Man Page

```text
No man page captured.
```

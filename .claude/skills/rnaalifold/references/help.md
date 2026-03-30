# rnaalifold Help Reference

- Command: `RNAalifold`
- Sources: conda_bioconda
- Local executable: `/home/vimalinx/miniforge3/envs/bio/bin/RNAalifold`
- Summary: CLI installed by bioconda package viennarna.
- Package names: viennarna

## Captured Version

```text
$ RNAalifold --version
RNAalifold 2.7.2
```

## Captured Help

```text
$ RNAalifold --help
Usage: RNAalifold [options] [<input0.aln>] [<input1.aln>]...
calculate secondary structures for a set of aligned RNAs

Read aligned RNA sequences from stdin or file.aln and calculate their minimum
free energy (mfe) structure, partition function (pf) and base pairing
probability matrix. Currently, input alignments have to be in CLUSTAL,
Stockholm, FASTA, or MAF format. The input format must be set manually in
interactive mode (default is Clustal), but will be determined automagically
from the input file, if not expplicitly set. It returns the mfe structure in
bracket notation, its energy, the free energy of the thermodynamic ensemble and
the frequency of the mfe structure in the ensemble to stdout.  It also produces
Postscript files with plots of the resulting secondary structure graph
("alirna.ps") and a "dot plot" of the base pairing matrix ("alidot.ps").
The file "alifold.out" will contain a list of likely pairs sorted by
credibility, suitable for viewing  with "AliDot.pl". Be warned that output
file will overwrite any existing files of the same name.



  -h, --help                    Print help and exit
      --detailed-help           Print help, including all details and hidden
                                  options, and exit
      --full-help               Print help, including hidden options, and exit
  -V, --version                 Print version and exit
  -v, --verbose                 Be verbose.
                                    (default=off)
  -q, --quiet                   Be quiet.
                                    (default=off)

I/O Options:
  Command line options for input and output (pre-)processing


  -f, --input-format=C|S|F|M    File format of the input multiple sequence
                                  alignment (MSA).

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
  -n, --continuous-ids          Use continuous alignment ID numbering when no
                                  alignment ID can be retrieved from input
                                  data.
                                    (default=off)
      --auto-id                 Automatically generate an ID for each
                                  alignment.
                                    (default=off)
      --id-prefix=STRING        Prefix for automatically generated IDs (as used
                                  in output file names).
                                    (default=`alignment')

Algorithms:
  Select additional algorithms which should be included in the calculations.


  -p, --partfunc[=INT]          Calculate the partition function and base
                                  pairing probability matrix in addition to the
                                  mfe structure. Default is calculation of mfe
                                  structure only.
                                    (default=`1')
      --MEA[=gamma]             Compute MEA (maximum expected accuracy)
                                  structure.
                                    (default=`1.')
      --sci                     Compute the structure conservation index (SCI)
                                  for the MFE consensus structure of the
                                  alignment.

                                    (default=off)
  -c, --circ                    Assume a circular (instead of linear) RNA
                                  molecule.

                                    (default=off)
  -g, --gquad                   Incoorporate G-Quadruplex formation into the
                                  structure prediction algorithm.

                                    (default=off)
  -s, --stochBT=INT             Stochastic backtrack. Compute a certain number
                                  of random structures with a probability
                                  dependend on the partition function. See -p
                                  option in RNAsubopt.


      --stochBT_en=INT          same as -s option but also print out the
                                  energies and probabilities of the backtraced
                                  structures.


  -N, --nonRedundant            Enable non-redundant sampling strategy.

                                    (default=off)

Structure Constraints:
  Command line options to interact with the structure constraints feature of
  this program


      --maxBPspan=INT           Set the maximum base pair span.

                                    (default=`-1')
  -C, --constraint[=filename]   Calculate structures subject to constraints.
                                  The constraining structure will be read from
                                  'stdin', the alignment has to be given as a
                                  file name on the command line.
                                    (default=`')
      --enforceConstraint       Enforce base pairs given by round brackets '('
                                  ')' in structure constraint.

                                    (default=off)
      --SS_cons                 Use consensus structures from Stockholm file
                                  ('#=GF SS_cons') as constraint.
                                    (default=off)
      --shape=file1,file2       Use SHAPE reactivity data to guide structure
                                  predictions.


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
      --noLP                    Produce structures without lonely pairs
                                  (helices of length 1).
                                    (default=off)
      --cfactor=DOUBLE          Set the weight of the covariance term in the
                                  energy function

                                    (default=`1.0')
      --nfactor=DOUBLE          Set the penalty for non-compatible sequences in
                                  the covariance term of the energy function

                                    (default=`1.0')
  -E, --endgaps                 Score pairs with endgaps same as gap-gap pairs.

                                    (default=off)
  -R, --ribosum_file=ribosumfile
                                use specified Ribosum Matrix instead of normal
                                  energy model.

  -r, --ribosum_scoring         use ribosum scoring matrix.
                                    (default=off)
      --old                     use old energy evaluation, treating gaps as
                                  characters.

                                    (default=off)

Plotting:
  Command line options for changing the default behavior of structure layout
  and pairing probability plots


      --color                   Produce a colored version of the consensus
                                  structure plot "alirna.ps" (default b&w
                                  only)

                                    (default=off)
      --aln                     Produce a colored and structure annotated
                                  alignment in PostScript format in the file
                                  "aln.ps" in the current directory.

                                    (default=off)
      --aln-stk[=prefix]        Create a multi-Stockholm formatted output file.
                                    (default=`RNAalifold_results')
      --noPS                    Do not produce postscript drawing of the mfe
                                  structure.

                                    (default=off)
      --noDP                    Do not produce dot-plot postscript file
                                  containing base pair or stack
                                  probabilitities.
                                    (default=off)
Caveats:

Sequences are not weighted. If possible, do not mix very similar and dissimilar
sequences. Duplicate sequences, for example, can distort the prediction.


If in doubt our program is right, nature is at fault.
Comments should be sent to rna@tbi.univie.ac.at.
```

## Captured Man Page

```text
No man page captured.
```

# rnalalifold Help Reference

- Command: `RNALalifold`
- Sources: conda_bioconda
- Local executable: `/home/vimalinx/miniforge3/envs/bio/bin/RNALalifold`
- Summary: CLI installed by bioconda package viennarna.
- Package names: viennarna

## Captured Version

```text
$ RNALalifold --version
RNALalifold 2.7.2
```

## Captured Help

```text
$ RNALalifold --help
Usage: RNALalifold [options] <file1.aln>
calculate locally stable secondary structures for a set of aligned RNAs

reads aligned RNA sequences from stdin or file.aln and calculates locally
stable RNA secondary structure with a maximal base pair span. For a sequence of
length n and a base pair span of L the algorithm uses only O(n+L*L) memory and
O(n*L*L) CPU time. Thus it is practical to "scan" very large genomes for
short RNA
 structures.


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

      --csv                     Create comma separated output (csv)

                                    (default=off)
      --aln[=prefix]            Produce output alignments and secondary
                                  structure plots for each hit found.

      --aln-stk[=prefix]        Add hits to a multi-Stockholm formatted output
                                  file.
                                    (default=`RNALalifold_results')
      --mis                     Output "most informative sequence" instead of
                                  simple consensus: For each column of the
                                  alignment output the set of nucleotides with
                                  frequency greater than average in IUPAC
                                  notation.

                                    (default=off)
      --split-contributions     Split the free energy contributions into
                                  separate parts
                                    (default=off)
      --noconv                  Do not automatically substitute nucleotide
                                  "T" with "U".

                                    (default=off)
      --auto-id                 Automatically generate an ID for each
                                  alignment.
                                    (default=off)
      --id-prefix=STRING        Prefix for automatically generated IDs (as used
                                  in output file names).
                                    (default=`alignment')

Algorithms:
  Select additional algorithms which should be included in the calculations.
  The Minimum free energy (MFE) and a structure representative are calculated
  in any case.


  -L, --maxBPspan=INT           Set the maximum allowed separation of a base
                                  pair to span. I.e. no pairs (i,j) with
                                  j-i>span will be allowed.

                                    (default=`70')
      --threshold=DOUBLE        Energy threshold in kcal/mol per nucleotide
                                  above which secondary structure hits are
                                  omitted in the output.

                                    (default=`-0.1')
  -g, --gquad                   Incoorporate G-Quadruplex formation into the
                                  structure prediction algorithm.

                                    (default=off)

Structure Constraints:
  Command line options to interact with the structure constraints feature of
  this program


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
  -R, --ribosum_file=ribosumfile
                                use specified Ribosum Matrix instead of normal
                                  energy model.

  -r, --ribosum_scoring         use ribosum scoring matrix.
                                    (default=off)

Plotting:
  Command line options for changing the default behavior of structure layout
  and pairing probability plots


      --aln-EPS[=prefix]        Produce colored and structure annotated
                                  subalignment for each hit.

      --aln-EPS-ss[=prefix]     Produce colored consensus secondary structure
                                  plots in PostScript format.


If in doubt our program is right, nature is at fault.
Comments should be sent to rna@tbi.univie.ac.at.
```

## Captured Man Page

```text
No man page captured.
```

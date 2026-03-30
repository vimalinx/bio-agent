# rnalocmin Help Reference

- Command: `RNAlocmin`
- Sources: conda_bioconda
- Local executable: `/home/vimalinx/miniforge3/envs/bio/bin/RNAlocmin`
- Summary: CLI installed by bioconda package viennarna.
- Package names: viennarna

## Captured Version

```text
$ RNAlocmin --version
RNAlocmin 2.1
```

## Captured Help

```text
$ RNAlocmin --help
Usage: RNAlocmin [OPTION]... [FILE]...
Calculate local minima from structures via gradient walks. Example usage: 
    RNAsubopt -p 10000 < "sequence.txt" > "suboptp.txt"
    RNAlocmin -s "sequence.txt" [OPTIONS] < "suboptp.txt"

  -h, --help                 Print help and exit
      --detailed-help        Print help, including all details and hidden
                               options, and exit
      --full-help            Print help, including hidden options, and exit
  -V, --version              Print version and exit

General options:
  -s, --seq=STRING           Sequence file in FASTA format. If the sequence is
                               the first line of the input file, this is not
                               needed  (default=`seq.txt')
  -p, --previous=STRING      Previously found LM (output from RNAlocmin or
                               barriers), if specified does not need --seq
                               option
  -m, --move=STRING          Move set:
                               I ==> insertion & deletion of base pairs
                               S ==> I&D& switch of base pairs  (possible
                               values="I", "S" default=`I')
  -n, --min-num=INT          Maximal number of local minima returned
                               (0 == unlimited)  (default=`100000')
      --find-num=INT         Maximal number of local minima found
                               (default = unlimited - crawl through whole input
                               file)
  -v, --verbose-lvl=INT      Level of verbosity (0 = nothing, 4 = full)
                               WARNING: higher verbose levels increase the
                               computation time  (default=`0')
      --depth=INT            Depth of findpath search (higher value increases
                               running time linearly)  (default=`10')
      --minh=DOUBLE          Print only minima with energy barrier greater than
                               this  (default=`0.0')
  -w, --walk=STRING          Walking method used
                               D ==> gradient descent
                               F ==> use first found lower energy structure
                               R ==> use random lower energy structure (does
                               not work with --noLP and -m S options)
                               (possible values="D", "F", "R"
                               default=`D')
      --noLP                 Work only with canonical RNA structures (w/o
                               isolated base pairs, cannot be combined with
                               ranodm walk (-w R option) and shift move set (-m
                               S))  (default=off)
  -P, --paramFile=STRING     Read energy parameters from paramfile, instead of
                               using the default parameter set
  -d, --dangles=INT          How to treat "dangling end" energies for bases
                               adjacent to helices in free ends and multi-loops
                                 (default=`2')
  -k, --pseudoknots          Allow for pseudoknots according to "gfold" model
                               - H, K, L, and M types (genus one) of
                               pseudoknots are allowed (increases computation
                               time greatly), cannot be combined with shift
                               move set (-m S)  (default=off)
      --just-read            Do not expect input from stdin, just do
                               postprocessing.  (default=off)
  -N, --neighborhood         Use the Neighborhood routines to perform gradient
                               descend. Cannot be combined with shift move set
                               (-m S) and pseudoknots (-k). Test option.
                               (default=off)
      --degeneracy-off       Do not deal with degeneracy, select the
                               lexicographically first from the same energy
                               neighbors.  (default=off)
      --just-output          Do not store the minima and optimize, just compute
                               directly minima and output them. Output file can
                               contain duplicates.  (default=off)

Barrier tree:
  -b, --bartree              Generate an approximate barrier tree.
                               (default=off)
      --barr-name=STRING     Name of barrier tree output file, switches on -b
                               flag.  (default=`treeRNAloc.ps')

Kinetics (rates for treekin program):
      --barrier-file=STRING  File for saddle heights between LM (simulates the
                               output format of barriers program)
  -r, --rates                Create rates for treekin  (default=off)
  -f, --rates-file=STRING    File where to write rates, switches on -r flag
                               (default=`rates.out')
  -T, --temp=DOUBLE          Temperature in Celsius (only for rates)
                               (default=`37.0')

Flooding parameters (flooding occurs only with -r, -b, or --minh option):
      --floodPortion=DOUBLE  Fraction of minima to flood (floods first minima
                               with low number of inwalking sample structures)
                               (0.0 -> no flood; 1.0 -> try to flood all)
                               Usable only with -r or -b options.
                               (default=`0.95')
      --floodMax=INT         Flood cap - how many structures to flood in one
                               basin  (default=`1000')

Miscelaneous:
      --eRange=FLOAT         Report only LM, which energy is in range <MFE (or
                               lowest found LM), MFE+eRange> in kcal/mol.
```

## Captured Man Page

```text
No man page captured.
```

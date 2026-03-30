# rnaplex Help Reference

- Command: `RNAplex`
- Sources: conda_bioconda
- Local executable: `/home/vimalinx/miniforge3/envs/bio/bin/RNAplex`
- Summary: CLI installed by bioconda package viennarna.
- Package names: viennarna

## Captured Version

```text
$ RNAplex --version
RNAplex 2.7.2
```

## Captured Help

```text
$ RNAplex --help
Usage: RNAplex [options]

Find targets of a query RNA

reads two RNA sequences from stdin or <filename> and computes optimal and
suboptimal secondary structures for their hybridization. The calculation is
simplified by allowing only inter-molecular base pairs. Accessibility effects
can be estimated by RNAplex if a RNAplfold accessibility profile is provided.
The computed optimal and suboptimal structure are written to stdout, one
structure per line. Each line consist of: The structure in dot bracket format
with a "&" separating the two strands. The range of the structure in the two
sequences in the format  "from,to : from,to"; the energy of duplex structure
in kcal/mol.
The format is especially useful for computing the hybrid structure between a
small probe sequence and a long target sequence.


  -h, --help                    Print help and exit
      --detailed-help           Print help, including all details and hidden
                                  options, and exit
      --full-help               Print help, including hidden options, and exit
      --version                 Print version and exit
  -v, --verbose                 Be verbose.
                                    (default=off)

I/O Options:
  Command line options for input and output (pre-)processing


  -q, --query=STRING            File containing the query sequence.

  -t, --target=STRING           File containing the target sequence.

  -a, --accessibility-dir=STRING
                                Location of the accessibility profiles.

  -b, --binary                  Allow the reading and parsing of memory dumped
                                  opening energy file
                                    (default=off)

Algorithms:
  Options which alter the computing behaviour of RNAplex.


  -l, --interaction-length=INT  Maximal length of an interaction
                                    (default=`40')
  -c, --extension-cost=INT      Cost to add to each nucleotide in a duplex
                                    (default=`0')
  -p, --probe-mode              Compute Tm for probes  (default=off)
  -Q, --probe-concentration=DOUBLE
                                Set the probe concentration for the Tm
                                  computation

                                    (default=`0.1')
  -f, --fast-folding=INT        Speedup of the target search
                                    (default=`0')
  -V, --scale-accessibility=DOUBLE
                                Rescale all opening energy by a factor V
                                    (default=`1.0')
  -A, --alignment-mode          Tells RNAplex to compute interactions based on
                                  alignments
                                    (default=off)
  -k, --convert-to-bin          If set, RNAplex will convert all opening energy
                                  file in a directory set by the -a option into
                                  binary opening energy files
                                    (default=off)
  -z, --duplex-distance=INT     Distance between target 3' ends of two
                                  consecutive duplexes
                                    (default=`0')
  -e, --energy-threshold=DOUBLE Minimal energy for a duplex to be returned
                                    (default=`-100000')
  -L, --WindowLength=INT        Tells how large the region around the target
                                  site should be for redrawing the alignment
                                  interaction
                                    (default=`1')

Structure Constraints:
  Command line options to interact with the structure constraints feature of
  this program


  -C, --constraint              Calculate structures subject to constraints.
                                    (default=off)

Energy Parameters:
  Energy parameter sets can be adapted or loaded from user-provided input files


  -T, --temp=DOUBLE             Rescale energy parameters to a temperature of
                                  temp C. Default is 37C.

                                    (default=`37.0')
  -P, --paramFile=paramfile     Read energy parameters from paramfile, instead
                                  of using the default parameter set.

      --salt=DOUBLE             Set salt concentration in molar (M). Default is
                                  1.021M.



Plotting:
  Command line options for changing the default behavior of structure layout
  and pairing probability plots


  -I, --produce-ps=STRING       Draw an alignment annotated interaction from
                                  RNAplex.


If in doubt our program is right, nature is at fault.
Comments should be sent to rna@tbi.univie.ac.at.
```

## Captured Man Page

```text
No man page captured.
```

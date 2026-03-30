# rnaforester Help Reference

- Command: `RNAforester`
- Sources: conda_bioconda
- Local executable: `/home/vimalinx/miniforge3/envs/bio/bin/RNAforester`
- Summary: CLI installed by bioconda package viennarna.
- Package names: viennarna

## Captured Version

```text
$ RNAforester --version
RNAforester, version 2.0.1
Copyright Stefanie Schirmer, Matthias Hoechsmann  2001-2011,
sschirme@techfak.uni-bielefeld.de
```

## Captured Help

```text
$ RNAforester --help
Usage: RNAforester [options]
--help                    shows this help info
--version                 shows version information
-f=file                   read input from file
--score                   compute only scores, no alignment
--noscale                 suppress output of scale
--tables                  shows dynamic programming tables
--backtrace               shows backtrace call table cells
-t                        calculate alignment top down instead of bottom up
-d                        calculate distance instead of similarity
-r                        calculate relative score
-l                        local similarity
-so=int                   local suboptimal alignments within int%
-s                        small-in-large similarity
--anchor                  use shape anchoring for speedup
-a                        affine gap scoring
-m                        multiple alignment mode
--RIBOSUM                 RIBOSUM85-60 scoring matrix (base-pair substitutions)
-cbmin=double             minimum base frequency for consensus structure
-cmin=double              minimum basepair frequency for consensus structure
-mt=double                clustering threshold
-mc=double                clustering cutoff
-p                        predict structures from sequences
-pmin=double              minimum basepair frequency for prediction
-sp=file                  save profile
-ps=file                  profile search
-pm=int                   basepair(bond) match score
-pd=int                   basepair bond indel score
-pdo=int                  basepair bond indel open score
-bm=int                   base match score
-br=int                   base mismatch score
-bd=int                   base indel score
-bdo=int                  base indel open score
-2d                       generate alignment 2D plots in postscript format
--2d_hidebasenum          hide base numbers in 2D plot
--2d_basenuminterval=n    show every n-th base number
--2d_grey                 use only grey colors in 2D plots
--2d_scale=double         scale factor for the 2d plots
--2d_fig                  generate additional fig file of 2d plot
--fasta                   generate fasta output of alignments
```

## Captured Man Page

```text
No man page captured.
```

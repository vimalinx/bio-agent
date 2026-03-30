# rnaconsensus Help Reference

- Command: `RNAconsensus`
- Sources: conda_bioconda
- Local executable: `/home/vimalinx/miniforge3/envs/bio/bin/RNAconsensus`
- Summary: CLI installed by bioconda package viennarna.
- Package names: viennarna

## Captured Version

```text
$ RNAconsensus --version
usage: RNAconsensus [-h] [-a filename] [-o OUTPUT] [--turn TURN]
                    {hardcons,softcons} ...
RNAconsensus: error: unrecognized arguments: --version
```

## Captured Help

```text
$ RNAconsensus --help
usage: RNAconsensus [-h] [-a filename] [-o OUTPUT] [--turn TURN]
                    {hardcons,softcons} ...

A program to predict RNA secondary structures for single sequences based on
the information gained from a multiple sequence alignment of homologous
sequences.

options:
  -h, --help            show this help message and exit
  -a filename, --alignment filename
                        A multiple sequence alignment file name
  -o OUTPUT, --output OUTPUT
                        A file or directory where to store the output
  --turn TURN           Minimum hairpin length

Prediction Stratgies:
  This programm allows for different strategies for the way the consensus
  structure information is incorporated for the single sequence predictions

  {hardcons,softcons}   Available strategies
    hardcons            The legacy refold.pl mode
    softcons            RNAsoftcons mode

If in doubt our program is right, nature is at fault. Comments should be sent
to rna@tbi.univie.ac.at.
```

## Captured Man Page

```text
No man page captured.
```

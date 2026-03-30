# kinwalker Help Reference

- Command: `kinwalker`
- Sources: conda_bioconda
- Local executable: `/home/vimalinx/miniforge3/envs/bio/bin/kinwalker`
- Summary: CLI installed by bioconda package viennarna.
- Package names: viennarna

## Captured Version

```text
$ kinwalker --version
kinwalker: unrecognized option '--version'

Usage: kinwalker [OPTIONS] < SeqFile  > Outfile
Options without argument:
 -h, --help          Print usage information for kinwalker.
--init_structure     Start with a structure other than the open chain.
--interrupt          Allow interrupted folding trajectories when the barrier is exceeded.
--printfront.        Creates PS plots of front progression with index i, named front_trajectory($i).ps.
 -t, --test          Use test sequence.
 -v, --verbose       Verbose mode. Print debugging messages about program progress.

Options with argument:
--barrier_heuristic  'M' Morgan-Higgs,'S' limits small stacks,'B' Barriers,'A' all, then take minimum. Default: >M<
--dangle             Dangle value of 0,1,2 as in the ViennaRNA package. Default: >0<
--grouping           How barrier_heuristic 'M' treats conflict groups("standard" or "regroup"). Default: >standard<
--lookahead          #BP that MorganHiggs forms its subpaths from. Default: >1<
--maxkeep            Breadth of breadth first seerch in barrier_heuristic='B'. Default: >1<
--nolonely           Value of noLonelyPairs as in ViennaRNA. Default: >2<
--transcribed        #bases initially transcribed, <0 means all is transcribed. Default: >1<)
--transcription_rate #bases transcribed per second. Default: >200.000000<)
--windowsize         Max size of substructures considered for folding events during transcription, 0= all are considered. Default: >0<)
```

## Captured Help

```text
$ kinwalker --help
Usage: kinwalker [OPTIONS] < SeqFile  > Outfile
Options without argument:
 -h, --help          Print usage information for kinwalker.
--init_structure     Start with a structure other than the open chain.
--interrupt          Allow interrupted folding trajectories when the barrier is exceeded.
--printfront.        Creates PS plots of front progression with index i, named front_trajectory($i).ps.
 -t, --test          Use test sequence.
 -v, --verbose       Verbose mode. Print debugging messages about program progress.

Options with argument:
--barrier_heuristic  'M' Morgan-Higgs,'S' limits small stacks,'B' Barriers,'A' all, then take minimum. Default: >M<
--dangle             Dangle value of 0,1,2 as in the ViennaRNA package. Default: >0<
--grouping           How barrier_heuristic 'M' treats conflict groups("standard" or "regroup"). Default: >standard<
--lookahead          #BP that MorganHiggs forms its subpaths from. Default: >1<
--maxkeep            Breadth of breadth first seerch in barrier_heuristic='B'. Default: >1<
--nolonely           Value of noLonelyPairs as in ViennaRNA. Default: >2<
--transcribed        #bases initially transcribed, <0 means all is transcribed. Default: >1<)
--transcription_rate #bases transcribed per second. Default: >200.000000<)
--windowsize         Max size of substructures considered for folding events during transcription, 0= all are considered. Default: >0<)
```

## Captured Man Page

```text
No man page captured.
```

# plot-roh-py Help Reference

- Command: `plot-roh.py`
- Sources: conda_bioconda
- Local executable: `/home/vimalinx/miniforge3/envs/bio/bin/plot-roh.py`
- Summary: CLI installed by bioconda package bcftools.
- Package names: bcftools

## Captured Version

```text
$ plot-roh.py --version
No data files found in "--version"
```

## Captured Help

```text
$ plot-roh.py --help
Usage: plot-roh.py [OPTIONS] <dir>
Options:
   -H, --highlight +group1,-group2       Highlight calls shared within group1 but not present in group2
   -i, --interactive                     Run interactively
   -l, --min-length <num>                Filter input regions shorter than this [0]
   -n, --min-markers <num>               Filter input regions with fewer marker than this [0]
   -o, --outfile <file>                  Output file name [plot.png]
   -q, --min-qual <num>                  Filter input regions with quality smaller than this [0]
   -r, --region [^]<chr|chr:beg-end>     Plot this chromosome/region only
   -s, --samples <file>                  List of samples to show, rename or group: "name[\tnew_name[\tgroup]]"
   -h, --help                            This usage text
Matplotlib options:
   +adj, --adjust <str>          Set plot adjust [bottom=0.18,left=0.07,right=0.98]
   +dpi, --dpi <num>             Set bitmap DPI [150]
   +sxt, --show-xticks           Show x-ticks (genomic coordinate)
   +twh, --track-wh <num,num>    Set track width and height [20,1]
   +xlb, --xlabel <str>          Set x-label
   +xli, --xlimit <num>          Extend x-range by this fraction [0.05]
```

## Captured Man Page

```text
No man page captured.
```

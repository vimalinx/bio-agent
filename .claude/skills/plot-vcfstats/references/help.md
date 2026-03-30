# plot-vcfstats Help Reference

- Command: `plot-vcfstats`
- Sources: conda_bioconda
- Local executable: `/home/vimalinx/miniforge3/envs/bio/bin/plot-vcfstats`
- Summary: CLI installed by bioconda package bcftools.
- Package names: bcftools

## Captured Version

```text
$ plot-vcfstats --version
Unknown parameter or non-existent file "--version". Run -h for help.
 at /home/vimalinx/miniforge3/envs/bio/bin/plot-vcfstats line 116.
	main::error("Unknown parameter or non-existent file \"--version\". Run -h fo"...) called at /home/vimalinx/miniforge3/envs/bio/bin/plot-vcfstats line 284
	main::parse_params() called at /home/vimalinx/miniforge3/envs/bio/bin/plot-vcfstats line 46
```

## Captured Help

```text
$ plot-vcfstats --help
About: Plots the output of "bcftools stats"
Usage: plot-vcfstats [OPTIONS] -p outdir file.chk ...
Options:
   -m, --merge                         Merge vcfstats files to STDOUT, skip plotting.
   -p, --prefix <dir>                  Output directory.
   -P, --no-PDF                        Skip the PDF creation step.
   -r, --rasterize                     Rasterize PDF images for fast rendering, the default and opposite of -v.
   -s, --sample-names                  Use sample names for xticks rather than numeric IDs.
   -t, --title <string>                Identify files by these titles in plots. Can be given multiple times.
   -T, --main-title <string>           Main title for the PDF.
   -v, --vectors                       Generate vector graphics for PDF images, the opposite of -r
   -h, -?, --help                      This help message.

Example:
   # Generate the stats
   bcftools stats -s - > file.vchk

   # Plot the stats
   plot-vcfstats -p outdir file.vchk

   # The final looks can be customized by editing the generated
   # 'outdir/plot.py' script and re-running manually
   cd outdir && python3 plot.py && pdflatex summary.tex
```

## Captured Man Page

```text
No man page captured.
```

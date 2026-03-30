# plot-ampliconstats Help Reference

- Command: `plot-ampliconstats`
- Sources: conda_bioconda
- Local executable: `/home/vimalinx/miniforge3/envs/bio/bin/plot-ampliconstats`
- Summary: CLI installed by bioconda package samtools.
- Package names: samtools

## Captured Version

```text
$ plot-ampliconstats --version
plot-ampliconstats version 1.0

Usage: plot-ampliconstats prefix [FILE]

Options:
    -help         Show this usage
    -size  W,H    Set image width to W and height to H for heatmaps
    -size2 W,H    Set image width to W and height to H for graphs (horizontal)
    -size3 W,H    Set image width to W and height to H for graphs (vertical)
    -page N       Maximum number of samples per page in heatmaps
    -amp-add X    Small sample fudge: NErr/(NAll+X) in amplicon count plots
    -orient h/v   Orientation for plots, defaults to h (horizontal)
    -depth-max N  Force -reads.png plots to have a fixed yrange
    -thumbnails   Produce scaled down thumbnail images
    -thumb-size N Display thumbnails as N pixels wide.

If FILE is not specified, reads from stdin.

Unknown option: version
```

## Captured Help

```text
$ plot-ampliconstats --help
plot-ampliconstats version 1.0

Usage: plot-ampliconstats prefix [FILE]

Options:
    -help         Show this usage
    -size  W,H    Set image width to W and height to H for heatmaps
    -size2 W,H    Set image width to W and height to H for graphs (horizontal)
    -size3 W,H    Set image width to W and height to H for graphs (vertical)
    -page N       Maximum number of samples per page in heatmaps
    -amp-add X    Small sample fudge: NErr/(NAll+X) in amplicon count plots
    -orient h/v   Orientation for plots, defaults to h (horizontal)
    -depth-max N  Force -reads.png plots to have a fixed yrange
    -thumbnails   Produce scaled down thumbnail images
    -thumb-size N Display thumbnails as N pixels wide.

If FILE is not specified, reads from stdin.
```

## Captured Man Page

```text
No man page captured.
```

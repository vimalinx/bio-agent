# roh-viz Help Reference

- Command: `roh-viz`
- Sources: conda_bioconda
- Local executable: `/home/vimalinx/miniforge3/envs/bio/bin/roh-viz`
- Summary: CLI installed by bioconda package bcftools.
- Package names: bcftools

## Captured Version

```text
$ roh-viz --version
Unknown parameter "--version". Run -h for help.

About: HTML/JavaScript visualization of homozygosity rate and bcftools/roh output
Usage: roh-viz [OPTIONS]
Options:
   -c  --compress 0|1      Compress the embedded data [1]
   -e  --embed-d3 0|1      Embed JS libraries for offline rendering [0]
   -i, --RoH-file FILE     Output of bcftools/roh
   -l, --min-length NUM    Mimimum length of ROH [1e6]
   -o, --output FILE       HTML output file
   -r, --regions LIST      List of chromosomes/regions
   -s, --samples LIST      List of samples to show
   -v, --VCF-file FILE     VCF file to determine homozygosity rate
   -h, -?, --help          This help message
Example:
   bcftools roh --AF-dflt 0.5 -G 30 -Or -o roh.txt file.bcf
   roh-viz -r roh.txt -v file.bcf -o output.html
```

## Captured Help

```text
$ roh-viz --help
About: HTML/JavaScript visualization of homozygosity rate and bcftools/roh output
Usage: roh-viz [OPTIONS]
Options:
   -c  --compress 0|1      Compress the embedded data [1]
   -e  --embed-d3 0|1      Embed JS libraries for offline rendering [0]
   -i, --RoH-file FILE     Output of bcftools/roh
   -l, --min-length NUM    Mimimum length of ROH [1e6]
   -o, --output FILE       HTML output file
   -r, --regions LIST      List of chromosomes/regions
   -s, --samples LIST      List of samples to show
   -v, --VCF-file FILE     VCF file to determine homozygosity rate
   -h, -?, --help          This help message
Example:
   bcftools roh --AF-dflt 0.5 -G 30 -Or -o roh.txt file.bcf
   roh-viz -r roh.txt -v file.bcf -o output.html
```

## Captured Man Page

```text
No man page captured.
```

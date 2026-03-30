# bowtie2-inspect-s Help Reference

- Command: `bowtie2-inspect-s`
- Sources: conda_bioconda
- Local executable: `/home/vimalinx/miniforge3/envs/bio/bin/bowtie2-inspect-s`
- Summary: CLI installed by bioconda package bowtie2.
- Package names: bowtie2

## Captured Version

```text
$ bowtie2-inspect-s --version
bowtie2-inspect-s version 2.5.5
64-bit
Built on runnervmn36qa
Tue Feb 17 04:37:58 UTC 2026
Compiler: gcc version 14.3.0 (conda-forge gcc 14.3.0-17) 
Options: -O3 -funroll-loops -g3 -fvisibility-inlines-hidden -fmessage-length=0 -march=nocona -mtune=haswell -ftree-vectorize -fPIC -fstack-protector-strong -fno-plt -O2 -ffunction-sections -pipe -isystem /home/vimalinx/miniforge3/envs/bio/include -fdebug-prefix-map=/opt/conda/conda-bld/bowtie2_1771302537514/work=/usr/local/src/conda/bowtie2-2.5.5 -fdebug-prefix-map=/home/vimalinx/miniforge3/envs/bio=/usr/local/src/conda-prefix -O3
Sizeof {int, long, long long, void*, size_t, off_t}: {4, 8, 8, 8, 8, 8}
```

## Captured Help

```text
$ bowtie2-inspect-s --help
Bowtie 2 version 2.5.5 by Ben Langmead (langmea@cs.jhu.edu, www.cs.jhu.edu/~langmea)
Usage: bowtie2-inspect [options]* <bt2_base>
  <bt2_base>         bt2 filename minus trailing .1.bt2/.2.bt2

  By default, prints FASTA records of the indexed nucleotide sequences to
  standard out.  With -n, just prints names.  With -s, just prints a summary of
  the index parameters and sequences.

Options:
  -a/--across <int>  Number of characters across in FASTA output (default: 60)
  -n/--names         Print reference sequence names only
  -s/--summary       Print summary incl. ref names, lengths, index properties
  -o/--output        Save output to filename (default stdout)
  -v/--verbose       Verbose output (for debugging)
  -h/--help          print this and message quit


*** Warning ***
'boowtie2-inspect' was run directly.  It is recommended to use the wrapper script instead.
```

## Captured Man Page

```text
No man page captured.
```

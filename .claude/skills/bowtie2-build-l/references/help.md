# bowtie2-build-l Help Reference

- Command: `bowtie2-build-l`
- Sources: conda_bioconda
- Local executable: `/home/vimalinx/miniforge3/envs/bio/bin/bowtie2-build-l`
- Summary: CLI installed by bioconda package bowtie2.
- Package names: bowtie2

## Captured Version

```text
$ bowtie2-build-l --version
bowtie2-build-l version 2.5.5
64-bit
Built on runnervmn36qa
Tue Feb 17 04:31:44 UTC 2026
Compiler: gcc version 14.3.0 (conda-forge gcc 14.3.0-17) 
Options: -O3 -funroll-loops -g3 -fvisibility-inlines-hidden -fmessage-length=0 -march=nocona -mtune=haswell -ftree-vectorize -fPIC -fstack-protector-strong -fno-plt -O2 -ffunction-sections -pipe -isystem /home/vimalinx/miniforge3/envs/bio/include -fdebug-prefix-map=/opt/conda/conda-bld/bowtie2_1771302537514/work=/usr/local/src/conda/bowtie2-2.5.5 -fdebug-prefix-map=/home/vimalinx/miniforge3/envs/bio=/usr/local/src/conda-prefix -O3 -fvisibility-inlines-hidden -fmessage-length=0 -march=nocona -mtune=haswell -ftree-vectorize -fPIC -fstack-protector-strong -fno-plt -O2 -ffunction-sections -pipe -isystem /home/vimalinx/miniforge3/envs/bio/include -fdebug-prefix-map=/opt/conda/conda-bld/bowtie2_1771302537514/work=/usr/local/src/conda/bowtie2-2.5.5 -fdebug-prefix-map=/home/vimalinx/miniforge3/envs/bio=/usr/local/src/conda-prefix -O3
Sizeof {int, long, long long, void*, size_t, off_t}: {4, 8, 8, 8, 8, 8}
```

## Captured Help

```text
$ bowtie2-build-l --help
Bowtie 2 version 2.5.5 by Ben Langmead (langmea@cs.jhu.edu, www.cs.jhu.edu/~langmea)
Usage: bowtie2-build-l [options]* <reference_in> <bt2_index_base>
    reference_in            comma-separated list of files with ref sequences
    bt2_index_base          write bt2l data to files with this dir/basename
*** Bowtie 2 indexes will work with Bowtie v1.2.3 and later. ***
Options:
    -f                      reference files are Fasta (default)
    -c                      reference sequences given on cmd line (as
                            <reference_in>)
    -a/--noauto             disable automatic -p/--bmax/--dcv memory-fitting
    -p/--packed             use packed strings internally; slower, less memory
    --bmax <int>            max bucket sz for blockwise suffix-array builder
    --bmaxdivn <int>        max bucket sz as divisor of ref len (default: 4)
    --dcv <int>             diff-cover period for blockwise (default: 1024)
    --nodc                  disable diff-cover (algorithm becomes quadratic)
    -r/--noref              don't build .3/.4 index files
    -3/--justref            just build .3/.4 index files
    -o/--offrate <int>      SA is sampled every 2^<int> BWT chars (default: 5)
    -t/--ftabchars <int>    # of chars consumed in initial lookup (default: 10)
    --threads <int>         # of threads
    --seed <int>            seed for random number generator
    -q/--quiet              verbose output (for debugging)
    --h/--help              print this message and quit
    --version               print version information and quit


*** Warning ***
'bowtie2-build-l' was run directly.  It is recommended that you run the wrapper script 'bowtie2-build' instead.
```

## Captured Man Page

```text
No man page captured.
```

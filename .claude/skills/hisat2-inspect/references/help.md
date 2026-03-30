# hisat2-inspect Help Reference

- Command: `hisat2-inspect`
- Sources: conda_bioconda
- Local executable: `/home/vimalinx/miniforge3/envs/bio/bin/hisat2-inspect`
- Summary: CLI installed by bioconda package hisat2.
- Package names: hisat2

## Captured Version

```text
$ hisat2-inspect --version
hisat2-inspect version 2.2.2
64-bit
Built on runnervmxu0kd
Tue Jan 27 19:28:48 UTC 2026
Compiler: collect2: error: ld returned 1 exit status
Options: -O3 -m64 -msse2 -funroll-loops -g3 -std=c++11
Sizeof {int, long, long long, void*, size_t, off_t}: {4, 8, 8, 8, 8, 8}
```

## Captured Help

```text
$ hisat2-inspect --help
HISAT2 version 2.2.2 by Daehwan Kim (infphilo@gmail.com, http://www.ccb.jhu.edu/people/infphilo)
Usage: hisat2-inspect [options]* <ht2_base>
  <ht2_base>         ht2 filename minus trailing .1.ht2/.2.ht2

  By default, prints FASTA records of the indexed nucleotide sequences to
  standard out.  With -n, just prints names.  With -s, just prints a summary of
  the index parameters and sequences.  With -e, preserves colors if applicable.

Options:
  --large-index      force inspection of the 'large' index, even if a
                     'small' one is present.
  -a/--across <int>  Number of characters across in FASTA output (default: 60)
  -s/--summary       Print summary incl. ref names, lengths, index properties
  -n/--names         Print reference sequence names only
  --snp              Print SNPs
  --ss               Print splice sites
  --ss-all           Print splice sites including those not in the global index
  --exon             Print exons
  -e/--ht2-ref       Reconstruct reference from .ht2 (slow, preserves colors)
  -v/--verbose       Verbose output (for debugging)
  -h/--help          print detailed description of tool and its options
  --usage            print this usage message
```

## Captured Man Page

```text
No man page captured.
```

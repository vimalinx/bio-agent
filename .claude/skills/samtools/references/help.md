# samtools Help Reference

- Command: `samtools`
- Sources: conda_bioconda, path, tool_reference
- Local executable: `/home/vimalinx/miniforge3/envs/bio/bin/samtools`
- Summary: Utilities for SAM, BAM, and CRAM alignment files.
- Package names: samtools

## Captured Version

```text
$ samtools --version
samtools 1.22.1
Using htslib 1.22.1
Copyright (C) 2025 Genome Research Ltd.

Samtools compilation details:
    Features:       build=configure curses=yes 
    CC:             /opt/conda/conda-bld/samtools_1752528053426/_build_env/bin/x86_64-conda-linux-gnu-cc
    CPPFLAGS:       -DNDEBUG -D_FORTIFY_SOURCE=2 -O2 -isystem /home/vimalinx/miniforge3/envs/bio/include
    CFLAGS:         -Wall -march=nocona -mtune=haswell -ftree-vectorize -fPIC -fstack-protector-strong -fno-plt -O2 -ffunction-sections -pipe -isystem /home/vimalinx/miniforge3/envs/bio/include -fdebug-prefix-map=/opt/conda/conda-bld/samtools_1752528053426/work=/usr/local/src/conda/samtools-1.22.1 -fdebug-prefix-map=/home/vimalinx/miniforge3/envs/bio=/usr/local/src/conda-prefix
    LDFLAGS:        -Wl,-O2 -Wl,--sort-common -Wl,--as-needed -Wl,-z,relro -Wl,-z,now -Wl,--disable-new-dtags -Wl,--gc-sections -Wl,--allow-shlib-undefined -Wl,-rpath,/home/vimalinx/miniforge3/envs/bio/lib -Wl,-rpath-link,/home/vimalinx/miniforge3/envs/bio/lib -L/home/vimalinx/miniforge3/envs/bio/lib
    HTSDIR:         
    LIBS:           
    CURSES_LIB:     -ltinfow -lncursesw

HTSlib compilation details:
    Features:       build=configure libcurl=yes S3=yes GCS=yes libdeflate=yes lzma=yes bzip2=yes plugins=yes plugin-path=/home/vimalinx/miniforge3/envs/bio/libexec/htslib htscodecs=1.6.4
    CC:             /opt/conda/conda-bld/htslib_1752522550715/_build_env/bin/x86_64-conda-linux-gnu-cc
    CPPFLAGS:       -DNDEBUG -D_FORTIFY_SOURCE=2 -O2 -isystem /home/vimalinx/miniforge3/envs/bio/include
    CFLAGS:         -Wall -march=nocona -mtune=haswell -ftree-vectorize -fPIC -fstack-protector-strong -fno-plt -O2 -ffunction-sections -pipe -isystem /home/vimalinx/miniforge3/envs/bio/include -fdebug-prefix-map=/opt/conda/conda-bld/htslib_1752522550715/work=/usr/local/src/conda/htslib-1.22.1 -fdebug-prefix-map=/home/vimalinx/miniforge3/envs/bio=/usr/local/src/conda-prefix -fvisibility=hidden
    LDFLAGS:        -Wl,-O2 -Wl,--sort-common -Wl,--as-needed -Wl,-z,relro -Wl,-z,now -Wl,--disable-new-dtags -Wl,--gc-sections -Wl,--allow-shlib-undefined -Wl,-rpath,/home/vimalinx/miniforge3/envs/bio/lib -Wl,-rpath-link,/home/vimalinx/miniforge3/envs/bio/lib -L/home/vimalinx/miniforge3/envs/bio/lib -fvisibility=hidden -rdynamic

HTSlib URL scheme handlers present:
    built-in:	 file, preload, data
    S3 Multipart Upload:	 s3w+https, s3w+http, s3w
    Amazon S3:	 s3+https, s3, s3+http
    libcurl:	 gophers, smtp, wss, smb, rtsp, tftp, pop3, smbs, imaps, pop3s, ws, ftps, https, ftp, gopher, sftp, imap, http, smtps, scp, dict, mqtt, telnet
    Google Cloud Storage:	 gs+http, gs+https, gs
    crypt4gh-needed:	 crypt4gh
    mem:	 mem
```

## Captured Help

```text
$ samtools --help
Program: samtools (Tools for alignments in the SAM format)
Version: 1.22.1 (using htslib 1.22.1)

Usage:   samtools <command> [options]

Commands:
  -- Indexing
     dict           create a sequence dictionary file
     faidx          index/extract FASTA
     fqidx          index/extract FASTQ
     index          index alignment

  -- Editing
     calmd          recalculate MD/NM tags and '=' bases
     fixmate        fix mate information
     reheader       replace BAM header
     targetcut      cut fosmid regions (for fosmid pool only)
     addreplacerg   adds or replaces RG tags
     markdup        mark duplicates
     ampliconclip   clip oligos from the end of reads

  -- File operations
     collate        shuffle and group alignments by name
     cat            concatenate BAMs
     consensus      produce a consensus Pileup/FASTA/FASTQ
     merge          merge sorted alignments
     mpileup        multi-way pileup
     sort           sort alignment file
     split          splits a file by read group
     quickcheck     quickly check if SAM/BAM/CRAM file appears intact
     fastq          converts a BAM to a FASTQ
     fasta          converts a BAM to a FASTA
     import         Converts FASTA or FASTQ files to SAM/BAM/CRAM
     reference      Generates a reference from aligned data
     reset          Reverts aligner changes in reads

  -- Statistics
     bedcov         read depth per BED region
     coverage       alignment depth and percent coverage
     depth          compute the depth
     flagstat       simple stats
     idxstats       BAM index stats
     cram-size      list CRAM Content-ID and Data-Series sizes
     phase          phase heterozygotes
     stats          generate stats (former bamcheck)
     ampliconstats  generate amplicon specific stats
     checksum       produce order-agnostic checksums of sequence content

  -- Viewing
     flags          explain BAM flags
     head           header viewer
     tview          text alignment viewer
     view           SAM<->BAM<->CRAM conversion
     depad          convert padded BAM to unpadded BAM
     samples        list the samples in a set of SAM/BAM/CRAM files

  -- Misc
     help [cmd]     display this help message or help for [cmd]
     version        detailed version information
```

## Captured Man Page

```text
No man page captured.
```

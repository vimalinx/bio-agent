# update-blastdb-pl Help Reference

- Command: `update_blastdb.pl`
- Sources: conda_bioconda
- Local executable: `/home/vimalinx/miniforge3/envs/bio/bin/update_blastdb.pl`
- Summary: CLI installed by bioconda package blast.
- Package names: blast

## Captured Version

```text
$ update_blastdb.pl --version
/home/vimalinx/miniforge3/envs/bio/bin/update_blastdb.pl version 697487
```

## Captured Help

```text
$ update_blastdb.pl --help
NAME
    update_blastdb.pl - Download pre-formatted BLAST databases

SYNOPSIS
    update_blastdb.pl [options] blastdb ...

OPTIONS
    --source
      Location to download BLAST databases from (default: auto-detect
      closest location). Supported values: "ncbi", "aws", or "gcp".

    --decompress
      Downloads, decompresses the archives in the current working directory,
      and deletes the downloaded archive to save disk space, while
      preserving the archive checksum files (default: false). This is only
      applicable when the download source is "ncbi".

    --showall
      Show all available pre-formatted BLAST databases (default: false). The
      output of this option lists the database names which should be used
      when requesting downloads or updates using this script.

      It accepts the optional arguments: "tsv" and "pretty" to produce
      tab-separated values and a human-readable format respectively. These
      parameters elicit the display of additional metadata if this is
      available to the program. This metadata is displayed in columnar
      format; the columns represent:

      name, description, size in gigabytes, date of last update (YYYY-MM-DD
      format).

    --blastdb_version
      Specify which BLAST database version to download (default: 5).
      Supported values: 4, 5

    --timeout
      Timeout on connection to NCBI (default: 120 seconds).

    --force
      Force download even if there is a archive already on local directory
      (default: false).

    --verbose
      Increment verbosity level (default: 1). Repeat this option multiple
      times to increase the verbosity level (maximum 2).

    --quiet
      Produce no output (default: false). Overrides the --verbose option.

    --version
      Prints this script's version. Overrides all other options.

    --num_threads
      Sets the number of threads to utilize to perform downloads in parallel
      when data comes from the cloud. On Windows it defaults to 1. On Linux
      and macos: defaults to max(1, (number_of_available_cores/4)) and if
      set to 0, the script uses all available cores on the machine.

    --legacy_exit_code
      Enables exit codes from prior to version 581818, BLAST+ 2.10.0
      release, for downloads from NCBI only. This option is meant to be used
      by legacy applications that rely on this exit codes: 0 for successful
      operations that result in no downloads, 1 for successful downloads,
      and 2 for errors.

    --force_ftp
      Forces downloads using the FTP protocol from the NCBI (Linux and
      Windows only). If the location from which to download is not NCBI,
      this option is ignored.

    --passive
      When using the <force_ftp> option, this flag enables passive FTP,
      useful when behind a firewall or working in the cloud (default: true).
      To disable passive FTP, configure this option as follows: --passive no

DESCRIPTION
    This script will download the pre-formatted BLAST databases requested in
    the command line from the NCBI ftp site.

EXIT CODES
    This script returns 0 on successful operations and non-zero on errors.

DEPENDENCIES
    This script depends on curl for retrieval from cloud service providers.

BUGS
    Please report them to <blast-help@ncbi.nlm.nih.gov>

COPYRIGHT
    See PUBLIC DOMAIN NOTICE included at the top of this script.
```

## Captured Man Page

```text
No man page captured.
```

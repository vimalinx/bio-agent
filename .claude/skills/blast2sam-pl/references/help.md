# blast2sam-pl Help Reference

- Command: `blast2sam.pl`
- Sources: conda_bioconda
- Local executable: `/home/vimalinx/miniforge3/envs/bio/bin/blast2sam.pl`
- Summary: CLI installed by bioconda package samtools.
- Package names: samtools

## Captured Version

```text
$ blast2sam.pl --version
/home/vimalinx/miniforge3/envs/bio/bin/blast2sam.pl version [unknown] calling Getopt::Std::getopts (version 1.14 [paranoid]),
running under Perl version 5.42.1.
  [Now continuing due to backward compatibility and excessive paranoia.
   See 'perldoc Getopt::Std' about $Getopt::Std::STANDARD_HELP_VERSION.]
```

## Captured Help

```text
$ blast2sam.pl --help
/home/vimalinx/miniforge3/envs/bio/bin/blast2sam.pl version [unknown] calling Getopt::Std::getopts (version 1.14 [paranoid]),
running under Perl version 5.42.1.

Usage: blast2sam.pl [-OPTIONS [-MORE_OPTIONS]] [--] [PROGRAM_ARG1 ...]

The following single-character options are accepted:
	Boolean (without arguments): -s -d

Options may be merged together.  -- stops processing of options.
  [Now continuing due to backward compatibility and excessive paranoia.
   See 'perldoc Getopt::Std' about $Getopt::Std::STANDARD_HELP_VERSION.]
```

## Source-Derived Option Notes

- `-s`: print the aligned query sequence into SAM field 10.
- `-d`: print dummy base qualities (`I` repeated to sequence length) into SAM field 11.
- The script documentation states it is for parsing default-format NCBI `blastn` output.
- The script emits no SAM header and does not output unaligned queries.

## Captured Man Page

```text
No man page captured.
```

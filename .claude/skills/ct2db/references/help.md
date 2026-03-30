# ct2db Help Reference

- Command: `ct2db`
- Sources: conda_bioconda
- Local executable: `/home/vimalinx/miniforge3/envs/bio/bin/ct2db`
- Summary: CLI installed by bioconda package viennarna.
- Package names: viennarna

## Captured Version

```text
$ ct2db --version
ct2db 1.0
```

## Captured Help

```text
$ ct2db --help
Usage: ct2db [OPTIONS] [<input0.ct>] [<input1.ct>]...
Produce dot bracket notation of an RNA secondary structure from Zuker's .ct
file

This program converts connectivity table (.ct) files into extended FASTA format
with dot-bracket string.


  -h, --help                    Print help and exit
      --detailed-help           Print help, including all details and hidden
                                  options, and exit
      --full-help               Print help, including hidden options, and exit
  -V, --version                 Print version and exit
  -p, --no-pk                   Remove pseudoknots from structure

                                    (default=off)
  -m, --no-modified             Do not keep modified bases, i.e. replace all
                                  non-canonical nucleotides with N.

                                    (default=off)
  -v, --verbose                 Be verbose.

                                    (default=off)
      --fasta-header=STRING     Overwrite FASTA header with user-provided
                                  string.

      --filename-suffix=STRING  The filename suffix to remove when turning the
                                  filename into a FASTA header.
                                    (default=`.ct')
```

## Captured Man Page

```text
No man page captured.
```

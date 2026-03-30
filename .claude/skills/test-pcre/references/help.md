# test-pcre Help Reference

- Command: `test_pcre`
- Sources: conda_bioconda
- Local executable: `/home/vimalinx/miniforge3/envs/bio/bin/test_pcre`
- Summary: CLI installed by bioconda package blast.
- Package names: blast

## Captured Version

```text
$ test_pcre --version
PCRE2 version 10.44 2024-06-07
```

## Captured Help

```text
$ test_pcre --help
Usage:     pcre2test [options] [<input file> [<output file>]]

Input and output default to stdin and stdout.
This version of pcre2test is not linked with readline().

Options:
  -8            use the 8-bit library
  -ac           set default pattern modifier PCRE2_AUTO_CALLOUT
  -AC           as -ac, but also set subject 'callout_extra' modifier
  -b            set default pattern modifier 'fullbincode'
  -C            show PCRE2 compile-time options and exit
  -C arg        show a specific compile-time option and exit with its
                  value if numeric (else 0). The arg can be:
     backslash-C    use of \C is enabled [0, 1]
     bsr            \R type [ANYCRLF, ANY]
     ebcdic         compiled for EBCDIC character code [0,1]
     ebcdic-nl      NL code if compiled for EBCDIC
     jit            just-in-time compiler supported [0, 1]
     linksize       internal link size [2, 3, 4]
     newline        newline type [CR, LF, CRLF, ANYCRLF, ANY, NUL]
     pcre2-8        8 bit library support enabled [0, 1]
     pcre2-16       16 bit library support enabled [0, 1]
     pcre2-32       32 bit library support enabled [0, 1]
     unicode        Unicode and UTF support enabled [0, 1]
  -d            set default pattern modifier 'debug'
  -dfa          set default subject modifier 'dfa'
  -error <n,m,..>  show messages for error numbers, then exit
  -help         show usage information
  -i            set default pattern modifier 'info'
  -jit          set default pattern modifier 'jit'
  -jitfast      set default pattern modifier 'jitfast'
  -jitverify    set default pattern modifier 'jitverify'
  -LM           list pattern and subject modifiers, then exit
  -LP           list non-script properties, then exit
  -LS           list supported scripts, then exit
  -q            quiet: do not output PCRE2 version number at start
  -pattern <s>  set default pattern modifier fields
  -subject <s>  set default subject modifier fields
  -S <n>        set stack size to <n> mebibytes
  -t [<n>]      time compilation and execution, repeating <n> times
  -tm [<n>]     time execution (matching) only, repeating <n> times
  -T            same as -t, but show total times at the end
  -TM           same as -tm, but show total time at the end
  -v|--version  show PCRE2 version and exit
```

## Captured Man Page

```text
No man page captured.
```

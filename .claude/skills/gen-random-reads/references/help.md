# gen-random-reads Help Reference

- Command: `genRandomReads`
- Sources: conda_bioconda
- Local executable: `/home/vimalinx/miniforge3/envs/bio/bin/genRandomReads`
- Summary: CLI installed by bioconda package subread.
- Package names: subread

## Captured Version

```text
$ genRandomReads --version
genRandomReads: unrecognized option '--version'

Usage:

 For scanning a FASTA/gz file:
    genRandomReads --summarizeFasta \
       --transcriptFasta <file> --outputPrefix <string> [--simpleTranscriptId]

 For generating read/pairs:
    genRandomReads --transcriptFasta <file>\
       --outputPrefix <string> --expressionLevels <file> [other options]

 --summarizeFasta           Only output the transcript names and lengths.

 --transcriptFasta <file>   The transcript database in FASTA/gz format.

 --outputPrefix <string>    The prefix of the output files.

 --totalReads  <int>        Total read/pairs in output.

 --expressionLevels <file>  Two column table delimited by <TAB>, giving the
                            wanted TPM values. Columns: TranscriptID and TPM

 --readLen <int>            The length of the output reads. 100 by default.

 --totalReads <int>         Total read/pairs in the output.

 --randSeed <int64>         Seed to generate random numbers. UNIXTIME is used
                            as the random seed by default.

 --qualityRefFile <file>    A textual file containing Phred+33 quanlity strings
                            for simulating sequencing errors. The quality
                            strings have to have the same length as the output
                            reads. No sequencing errors are simulated when this
                            option is omitted.

 --floorStrategy            How to deal with round-up errors. 'FLOOR': generate
                            less than wanted reads; 'RANDOM': randomly assign
                            margin reads to transcripts; 'ITERATIVE': find the
                            best M value to have ~N reads.

 --pairedEnd                Generate paired-end reads.

 --insertionLenMean <float>,--insertionLenSigma <float>,--insertionLenMin <int>,
 --insertionLenMax <int>    Parameters of a truncated normal distribution for
                            deciding insertion lengths of paired-end reads.
                            Default values: mean=160, sigma=30, min=110, max=400

 --simpleTranscriptId       Truncate transcript names to the first '|' or space.

 --truthInReadNames         Encode the true locations of reads in read names.

 --noActualReads            Do not actually generate reads in fastq.gz files.
```

## Captured Help

```text
$ genRandomReads --help
genRandomReads: unrecognized option '--help'

Usage:

 For scanning a FASTA/gz file:
    genRandomReads --summarizeFasta \
       --transcriptFasta <file> --outputPrefix <string> [--simpleTranscriptId]

 For generating read/pairs:
    genRandomReads --transcriptFasta <file>\
       --outputPrefix <string> --expressionLevels <file> [other options]

 --summarizeFasta           Only output the transcript names and lengths.

 --transcriptFasta <file>   The transcript database in FASTA/gz format.

 --outputPrefix <string>    The prefix of the output files.

 --totalReads  <int>        Total read/pairs in output.

 --expressionLevels <file>  Two column table delimited by <TAB>, giving the
                            wanted TPM values. Columns: TranscriptID and TPM

 --readLen <int>            The length of the output reads. 100 by default.

 --totalReads <int>         Total read/pairs in the output.

 --randSeed <int64>         Seed to generate random numbers. UNIXTIME is used
                            as the random seed by default.

 --qualityRefFile <file>    A textual file containing Phred+33 quanlity strings
                            for simulating sequencing errors. The quality
                            strings have to have the same length as the output
                            reads. No sequencing errors are simulated when this
                            option is omitted.

 --floorStrategy            How to deal with round-up errors. 'FLOOR': generate
                            less than wanted reads; 'RANDOM': randomly assign
                            margin reads to transcripts; 'ITERATIVE': find the
                            best M value to have ~N reads.

 --pairedEnd                Generate paired-end reads.

 --insertionLenMean <float>,--insertionLenSigma <float>,--insertionLenMin <int>,
 --insertionLenMax <int>    Parameters of a truncated normal distribution for
                            deciding insertion lengths of paired-end reads.
                            Default values: mean=160, sigma=30, min=110, max=400

 --simpleTranscriptId       Truncate transcript names to the first '|' or space.

 --truthInReadNames         Encode the true locations of reads in read names.

 --noActualReads            Do not actually generate reads in fastq.gz files.
```

## Captured Man Page

```text
No man page captured.
```

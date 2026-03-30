# flatten-gtf Help Reference

- Command: `flattenGTF`
- Sources: conda_bioconda
- Local executable: `/home/vimalinx/miniforge3/envs/bio/bin/flattenGTF`
- Summary: CLI installed by bioconda package subread.
- Package names: subread

## Captured Version

```text
$ flattenGTF --version
flattenGTF: unrecognized option '--version'
flattenGTF Version 2.1.1

  Flatten features included in a GTF annotation and save the modified annotation
  to a SAF format file.

Usage:
  ./flattenGTF [options] -a <input_file> -o <output_file>

## Mandatory arguments: 

  -a <file>      Name of an annotation file in GTF/GFF format.

  -o <file>      Name of output file.

## Optional arguments: 

  -t <string>    Specify feature type in a GTF annotation. 'exon' by default.
                 Features with the specified feature type are extracted from the
                 annotation for processing.

  -g <string>    Specify attribute type in GTF annotation. 'gene_id' by default.
                 This attribute type is used to group features into meta-
                 features.

  -C             Merging overlapping exons into multiple non-overlapping exons but
                 all the edges are kept.
```

## Captured Help

```text
$ flattenGTF --help
flattenGTF: unrecognized option '--help'
flattenGTF Version 2.1.1

  Flatten features included in a GTF annotation and save the modified annotation
  to a SAF format file.

Usage:
  ./flattenGTF [options] -a <input_file> -o <output_file>

## Mandatory arguments: 

  -a <file>      Name of an annotation file in GTF/GFF format.

  -o <file>      Name of output file.

## Optional arguments: 

  -t <string>    Specify feature type in a GTF annotation. 'exon' by default.
                 Features with the specified feature type are extracted from the
                 annotation for processing.

  -g <string>    Specify attribute type in GTF annotation. 'gene_id' by default.
                 This attribute type is used to group features into meta-
                 features.

  -C             Merging overlapping exons into multiple non-overlapping exons but
                 all the edges are kept.
```

## Captured Man Page

```text
No man page captured.
```

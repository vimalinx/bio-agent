# tblastn-vdb Help Reference

- Command: `tblastn_vdb`
- Sources: conda_bioconda
- Local executable: `/home/vimalinx/miniforge3/envs/bio/bin/tblastn_vdb`
- Summary: CLI installed by bioconda package blast.
- Package names: blast

## Captured Version

```text
$ tblastn_vdb -version
tblastn_vdb: 2.17.0+
ncbi-vdb: 3.3.0
 Package: blast 2.17.0, build Aug 11 2025 09:46:06
```

## Captured Help

```text
$ tblastn_vdb -help
USAGE
  tblastn [-h] [-help] [-import_search_strategy filename]
    [-export_search_strategy filename] [-db database_name]
    [-dbsize num_letters] [-query input_file] [-out output_file]
    [-evalue evalue] [-word_size int_value] [-gapopen open_penalty]
    [-gapextend extend_penalty] [-qcov_hsp_perc float_value]
    [-max_hsps int_value] [-xdrop_ungap float_value] [-xdrop_gap float_value]
    [-xdrop_gap_final float_value] [-searchsp int_value]
    [-sum_stats bool_value] [-db_gencode int_value] [-ungapped]
    [-max_intron_length length] [-seg SEG_options]
    [-soft_masking soft_masking] [-matrix matrix_name]
    [-threshold float_value] [-culling_limit int_value]
    [-best_hit_overhang float_value] [-best_hit_score_edge float_value]
    [-subject_besthit] [-window_size int_value] [-lcase_masking]
    [-query_loc range] [-parse_deflines] [-outfmt format] [-show_gis]
    [-num_descriptions int_value] [-num_alignments int_value]
    [-line_length line_length] [-html] [-sorthits sort_hits]
    [-sorthsps sort_hsps] [-max_target_seqs num_sequences]
    [-num_threads int_value] [-sra_mode SRA_search_mode]
    [-include_filtered_reads] [-comp_based_stats compo] [-use_sw_tback]
    [-in_pssm psi_chkpt_file] [-version]

DESCRIPTION
   Protein Query-Translated Subject BLAST 2.17.0+

OPTIONAL ARGUMENTS
 -h
   Print USAGE and DESCRIPTION;  ignore all other parameters
 -help
   Print USAGE, DESCRIPTION and ARGUMENTS; ignore all other parameters
 -version
   Print version number;  ignore other arguments

 *** Input query options
 -query <File_In>
   Input file name
   Default = `-'
    * Incompatible with:  in_pssm
 -query_loc <String>
   Location on the query sequence in 1-based offsets (Format: start-stop)
    * Incompatible with:  in_pssm

 *** General search options
 -db <String>
   SRA or WGS database name
 -out <File_Out, file name length < 256>
   Output file name
   Default = `-'
 -evalue <Real>
   Expectation value (E) threshold for saving hits. Default = 10
 -word_size <Integer, >=2>
   Word size for wordfinder algorithm
 -gapopen <Integer>
   Cost to open a gap
 -gapextend <Integer>
   Cost to extend a gap
 -db_gencode <Integer, values between: 1-6, 9-16, 21-31, 33>
   Genetic code to use to translate database/subjects (see user manual for
   details)
   Default = `1'
 -max_intron_length <Integer, >=0>
   Length of the largest intron allowed in a translated nucleotide sequence
   when linking multiple distinct alignments
   Default = `0'
 -matrix <String>
   Scoring matrix name (normally BLOSUM62)
 -threshold <Real, >=0>
   Minimum word score such that the word is added to the BLAST lookup table
 -sra_mode <Integer>
   SRA Search Mode:
   0 = unaligned reads only
   1 = aligned reference seqs only
   2 = both unaligned reads and aligned reference seqs n
   Default = `0'
 -include_filtered_reads
   Include filtered reads
 -comp_based_stats <String>
   Use composition-based statistics:
       D or d: default (equivalent to 2 )
       0 or F or f: No composition-based statistics
       1: Composition-based statistics as in NAR 29:2994-3005, 2001
       2 or T or t : Composition-based score adjustment as in Bioinformatics
   21:902-911,
       2005, conditioned on sequence properties
       3: Composition-based score adjustment as in Bioinformatics 21:902-911,
       2005, unconditionally
   Default = `2'

 *** Formatting options
 -outfmt <String>
   alignment view options:
     0 = Pairwise,
     1 = Query-anchored showing identities,
     2 = Query-anchored no identities,
     3 = Flat query-anchored showing identities,
     4 = Flat query-anchored no identities,
     5 = BLAST XML,
     6 = Tabular,
     7 = Tabular with comment lines,
     8 = Seqalign (Text ASN.1),
     9 = Seqalign (Binary ASN.1),
    10 = Comma-separated values,
    11 = BLAST archive (ASN.1),
    12 = Seqalign (JSON),
    13 = Multiple-file BLAST JSON,
    14 = Multiple-file BLAST XML2,
    15 = Single-file BLAST JSON,
    16 = Single-file BLAST XML2,
    18 = Organism Report,
    20 = Comma-separated values with header lines
```

## Captured Bare Invocation

```text
$ tblastn_vdb
BLAST query/options error: Must specify at least one SRA/WGS database
```

## Captured Man Page

```text
No man page captured.
```

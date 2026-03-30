# fill-aa Help Reference

- Command: `fill-aa`
- Sources: conda_bioconda
- Local executable: `/home/vimalinx/miniforge3/envs/bio/bin/fill-aa`
- Summary: CLI installed by bioconda package vcftools.
- Package names: vcftools

## Captured Version

```text
$ fill-aa --version
Unknown parameter "--version". Run -h for help.
 at /home/vimalinx/miniforge3/envs/bio/bin/fill-aa line 27.
	main::error("Unknown parameter \"--version\". Run -h for help.\x{a}") called at /home/vimalinx/miniforge3/envs/bio/bin/fill-aa line 90
	main::parse_params() called at /home/vimalinx/miniforge3/envs/bio/bin/fill-aa line 17
```

## Captured Help

```text
$ fill-aa --help
About: This script fills ancestral alleles into INFO column of VCF files. It depends on samtools,
   therefore the fasta sequence must be gzipped (not bgzipped!) and indexed by samtools faidx.
   The AA files can be downloaded from
       ftp://ftp.1000genomes.ebi.ac.uk/vol1/ftp/pilot_data/technical/reference/ancestral_alignments
   and processed as shown in the example below. This is because the sequences in the original files
   are named as 'ANCESTOR_for_chromosome:NCBI36:1:1:247249719', but the underlying FaSplice.pm
   requires names as 'chr1' or '1'.
Usage: fill-aa [OPTIONS] < in.vcf >out.vcf
Options:
   -a, --ancestral-allele <prefix>     Prefix to ancestral allele chromosome files.
   -t, --type <list>                   Variant types to process: all,indel,ref,snp. [all]
   -h, -?, --help                      This help message.
Example:
   # Get the files ready: compress by gzip and index by samtools faidx. Either repeat the
   # following command for each file manually
   bzcat human_ancestor_1.fa.bz2 | sed 's,^>.*,>1,' | gzip -c > human_ancestor_1.fa.gz
   samtools faidx human_ancestor_1.fa.gz
   
   # .. or use this loop (tested in bash shell)
   ls human_ancestor_*.fa.bz2 | while read IN; do
       OUT=`echo $IN | sed 's,bz2$,gz,'`
       CHR=`echo $IN | sed 's,human_ancestor_,, ; s,.fa.bz2,,'`
       bzcat $IN | sed "s,^>.*,>$CHR," | gzip -c > $OUT
       samtools faidx $OUT
   done
   
   # After this has been done, the following command should return 'TACGTGGcTGCTCTCACACAT'
   samtools faidx human_ancestor_1.fa.gz 1:1000000-1000020
   
   # Now the files are ready to use with fill-aa. Note that the VCF file
   # should be sorted (see vcf-sort), otherwise the performance would be seriously
   # affected.
   cat file.vcf | fill-aa -a human_ancestor_ 2>test.err | gzip -c >out.vcf.gz
```

## Captured Man Page

```text
No man page captured.
```

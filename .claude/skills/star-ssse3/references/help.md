# star-ssse3 Help Reference

- Command: `STAR-ssse3`
- Sources: conda_bioconda
- Local executable: `/home/vimalinx/miniforge3/envs/bio/bin/STAR-ssse3`
- Summary: CLI installed by bioconda package star.
- Package names: star

## Captured Version

```text
$ STAR-ssse3 --version
2.7.11b
```

## Captured Help

```text
$ STAR-ssse3 --help
Usage: STAR  [options]... --genomeDir /path/to/genome/index/   --readFilesIn R1.fq R2.fq
Spliced Transcripts Alignment to a Reference (c) Alexander Dobin, 2009-2022

STAR version=2.7.11b
STAR compilation time,server,dir=2025-11-14T12:11:23+0000 :/opt/conda/conda-bld/star_1763121846936/work/source
For more details see:
<https://github.com/alexdobin/STAR>
<https://github.com/alexdobin/STAR/blob/master/doc/STARmanual.pdf>
### versions
versionGenome           2.7.4a
    string: earliest genome index version compatible with this STAR release. Please do not change this value!

### Parameter Files
parametersFiles          -
    string: name of a user-defined parameters file, "-": none. Can only be defined on the command line.

### System
sysShell            -
    string: path to the shell binary, preferably bash, e.g. /bin/bash.
                    - ... the default shell is executed, typically /bin/sh. This was reported to fail on some Ubuntu systems - then you need to specify path to bash.

### Run Parameters
runMode                         alignReads
    string: type of the run.
                                alignReads             ... map reads
                                genomeGenerate         ... generate genome files
                                inputAlignmentsFromBAM ... input alignments from BAM. Presently only works with --outWigType and --bamRemoveDuplicates options.
                                liftOver               ... lift-over of GTF files (--sjdbGTFfile) between genome assemblies using chain file(s) from --genomeChainFiles.
                                soloCellFiltering  </path/to/raw/count/dir/>   </path/to/output/prefix>    ... STARsolo cell filtering ("calling") without remapping, followed by the path to raw count directory and output (filtered) prefix

runThreadN                      1
    int: number of threads to run STAR

runDirPerm                      User_RWX
    string: permissions for the directories created at the run-time.
                                User_RWX ... user-read/write/execute
                                All_RWX  ... all-read/write/execute (same as chmod 777)

runRNGseed                      777
    int: random number generator seed.


### Genome Parameters
genomeDir                   ./GenomeDir/
    string: path to the directory where genome files are stored (for --runMode alignReads) or will be generated (for --runMode generateGenome)

genomeLoad                NoSharedMemory
    string: mode of shared memory usage for the genome files. Only used with --runMode alignReads.
                          LoadAndKeep     ... load genome into shared and keep it in memory after run
                          LoadAndRemove   ... load genome into shared but remove it after run
                          LoadAndExit     ... load genome into shared memory and exit, keeping the genome in memory for future runs
                          Remove          ... do not map anything, just remove loaded genome from memory
                          NoSharedMemory  ... do not use shared memory, each job will have its own private copy of the genome

genomeFastaFiles            -
    string(s): path(s) to the fasta files with the genome sequences, separated by spaces. These files should be plain text FASTA files, they *cannot* be zipped.
                            Required for the genome generation (--runMode genomeGenerate). Can also be used in the mapping (--runMode alignReads) to add extra (new) sequences to the genome (e.g. spike-ins).

genomeChainFiles            -
    string: chain files for genomic liftover. Only used with --runMode liftOver .

genomeFileSizes             0
    uint(s)>0: genome files exact sizes in bytes. Typically, this should not be defined by the user.
    
genomeTransformOutput       None
    string(s):              which output to transform back to original genome
                            SAM     ... SAM/BAM alignments
                            SJ      ... splice junctions (SJ.out.tab)
                            Quant   ... quantifications (from --quantMode option)
                            None    ... no transformation of the output        

genomeChrSetMitochondrial   chrM M MT
    string(s):              names of the mitochondrial chromosomes. Presently only used for STARsolo statistics output/

### Genome Indexing Parameters - only used with --runMode genomeGenerate
genomeChrBinNbits           18
    int: =log2(chrBin), where chrBin is the size of the bins for genome storage: each chromosome will occupy an integer number of bins. For a genome with large number of contigs, it is recommended to scale this parameter as min(18, log2[max(GenomeLength/NumberOfReferences,ReadLength)]).

genomeSAindexNbases         14
    int: length (bases) of the SA pre-indexing string. Typically between 10 and 15. Longer strings will use much more memory, but allow faster searches. For small genomes, the parameter --genomeSAindexNbases must be scaled down to min(14, log2(GenomeLength)/2 - 1).

genomeSAsparseD             1
    int>0: suffux array sparsity, i.e. distance between indices: use bigger numbers to decrease needed RAM at the cost of mapping speed reduction

genomeSuffixLengthMax       -1
    int: maximum length of the suffixes, has to be longer than read length. -1 = infinite.
    
genomeTransformType         None
    string: type of genome transformation
                            None       ... no transformation
                            Haploid    ... replace reference alleles with alternative alleles from VCF file (e.g. consensus allele)
                            Diploid    ... create two haplotypes for each chromosome listed in VCF file, for genotypes 1|2, assumes perfect phasing (e.g. personal genome)

genomeTransformVCF          -
    string: path to VCF file for genome transformation


    
#####UnderDevelopment_begin : not supported - do not use
genomeType                  Full
    string: type of genome to generate
                            Full                ... full (normal) genome
                            Transcriptome       ... genome consists of transcript sequences
                            SuperTransriptome   ... genome consists of superTranscript sequences
#####UnderDevelopment_end

# DEPRECATED: please use --genomeTransformVCF and --genomeTransformType options instead.
#genomeConsensusFile         -
#    string: VCF file with consensus SNPs (i.e. alternative allele is the major (AF>0.5) allele)
# DEPRECATED 



### Splice Junctions Database
sjdbFileChrStartEnd                     -
    string(s): path to the files with genomic coordinates (chr <tab> start <tab> end <tab> strand) for the splice junction introns. Multiple files can be supplied and will be concatenated.

sjdbGTFfile                             -
    string: path to the GTF file with annotations

sjdbGTFchrPrefix                        -
    string: prefix for chromosome names in a GTF file (e.g. 'chr' for using ENSMEBL annotations with UCSC genomes)

sjdbGTFfeatureExon                      exon
    string: feature type in GTF file to be used as exons for building transcripts

sjdbGTFtagExonParentTranscript          transcript_id
    string: GTF attribute name for parent transcript ID (default "transcript_id" works for GTF files)

sjdbGTFtagExonParentGene                gene_id
    string: GTF attribute name for parent gene ID (default "gene_id" works for GTF files)

sjdbGTFtagExonParentGeneName            gene_name
    string(s): GTF attribute name for parent gene name

sjdbGTFtagExonParentGeneType            gene_type gene_biotype
    string(s): GTF attribute name for parent gene type

sjdbOverhang                            100
    int>0: length of the donor/acceptor sequence on each side of the junctions, ideally = (mate_length - 1)

sjdbScore                               2
    int: extra alignment score for alignments that cross database junctions

sjdbInsertSave                          Basic
    string: which files to save when sjdb junctions are inserted on the fly at the mapping step
                    Basic ... only small junction / transcript files
                    All   ... all files including big Genome, SA and SAindex - this will create a complete genome directory

### Variation parameters
varVCFfile                              -
    string: path to the VCF file that contains variation data. The 10th column should contain the genotype information, e.g. 0/1

### Input Files
inputBAMfile                -
    string: path to BAM input file, to be used with --runMode inputAlignmentsFromBAM

### Read Parameters
readFilesType               Fastx
    string: format of input read files
                            Fastx       ... FASTA or FASTQ
                            SAM SE      ... SAM or BAM single-end reads; for BAM use --readFilesCommand samtools view
                            SAM PE      ... SAM or BAM paired-end reads; for BAM use --readFilesCommand samtools view
                            
readFilesSAMattrKeep        All
    string(s): for --readFilesType SAM SE/PE, which SAM tags to keep in the output BAM, e.g.: --readFilesSAMtagsKeep RG PL
                            All     ... keep all tags
                            None    ... do not keep any tags

readFilesIn                 Read1 Read2
    string(s): paths to files that contain input read1 (and, if needed,  read2)

readFilesManifest           -
    string: path to the "manifest" file with the names of read files. The manifest file should contain 3 tab-separated columns:
            paired-end reads: read1_file_name $tab$ read2_file_name $tab$ read_group_line.
            single-end reads: read1_file_name $tab$ -               $tab$ read_group_line.
            Spaces, but not tabs are allowed in file names.
            If read_group_line does not start with ID:, it can only contain one ID field, and ID: will be added to it.
            If read_group_line starts with ID:, it can contain several fields separated by $tab$, and all fields will be be copied verbatim into SAM @RG header line.

readFilesPrefix             -
    string: prefix for the read files names, i.e. it will be added in front of the strings in --readFilesIn

readFilesCommand             -
    string(s): command line to execute for each of the input file. This command should generate FASTA or FASTQ text and send it to stdout
               For example: zcat - to uncompress .gz files, bzcat - to uncompress .bz2 files, etc.

readMapNumber               -1
    int: number of reads to map from the beginning of the file
                            -1: map all reads

readMatesLengthsIn          NotEqual
    string: Equal/NotEqual - lengths of names,sequences,qualities for both mates are the same  / not the same. NotEqual is safe in all situations.

readNameSeparator           /
    string(s): character(s) separating the part of the read names that will be trimmed in output (read name after space is always trimmed)

readQualityScoreBase        33
    int>=0: number to be subtracted from the ASCII code to get Phred quality score

### Read Clipping

clipAdapterType             Hamming
    string:                 adapter clipping type
                            Hamming ... adapter clipping based on Hamming distance, with the number of mismatches controlled by --clip5pAdapterMMp
                            CellRanger4 ... 5p and 3p adapter clipping similar to CellRanger4. Utilizes Opal package by Martin Šošić: https://github.com/Martinsos/opal
                            None ... no adapter clipping, all other clip* parameters are disregarded
                            
clip3pNbases                 0
    int(s): number(s) of bases to clip from 3p of each mate. If one value is given, it will be assumed the same for both mates.

clip3pAdapterSeq            -
    string(s): adapter sequences to clip from 3p of each mate.  If one value is given, it will be assumed the same for both mates.
                            polyA ... polyA sequence with the length equal to read length

clip3pAdapterMMp            0.1
    double(s): max proportion of mismatches for 3p adapter clipping for each mate.  If one value is given, it will be assumed the same for both mates.

clip3pAfterAdapterNbases    0
    int(s): number of bases to clip from 3p of each mate after the adapter clipping. If one value is given, it will be assumed the same for both mates.

clip5pNbases                 0
    int(s): number(s) of bases to clip from 5p of each mate. If one value is given, it will be assumed the same for both mates.

#####UnderDevelopment_begin : not supported - do not use   
clip5pAdapterSeq            -
    string(s): adapter sequences to clip from 5p of each mate, separated by space.

clip5pAdapterMMp            0.1
    double(s): max proportion of mismatches for 5p adapter clipping for each mate, separated by space

clip5pAfterAdapterNbases    0
    int(s): number of bases to clip from 5p of each mate after the adapter clipping, separated by space.
#####UnderDevelopment_end

### Limits
limitGenomeGenerateRAM               31000000000
    int>0: maximum available RAM (bytes) for genome generation

limitIObufferSize                    30000000 50000000
    int(s)>0: max available buffers size (bytes) for input/output, per thread

limitOutSAMoneReadBytes              100000
    int>0: max size of the SAM record (bytes) for one read. Recommended value: >(2*(LengthMate1+LengthMate2+100)*outFilterMultimapNmax

limitOutSJoneRead                    1000
    int>0: max number of junctions for one read (including all multi-mappers)

limitOutSJcollapsed                  1000000
    int>0: max number of collapsed junctions

limitBAMsortRAM                         0
    int>=0: maximum available RAM (bytes) for sorting BAM. If =0, it will be set to the genome index size. 0 value can only be used with --genomeLoad NoSharedMemory option.

limitSjdbInsertNsj                     1000000
    int>=0: maximum number of junctions to be inserted to the genome on the fly at the mapping stage, including those from annotations and those detected in the 1st step of the 2-pass run

limitNreadsSoft                        -1
    int: soft limit on the number of reads

### Output: general
outFileNamePrefix               ./
    string: output files name prefix (including full or relative path). Can only be defined on the command line.

outTmpDir                       -
    string: path to a directory that will be used as temporary by STAR. All contents of this directory will be removed!
                                - ... the temp directory will default to outFileNamePrefix_STARtmp

outTmpKeep                      None
    string: whether to keep the temporary files after STAR runs is finished
                                None ... remove all temporary files
                                All ... keep all files

outStd                          Log
    string: which output will be directed to stdout (standard out)
                                Log                    ... log messages
                                SAM                    ... alignments in SAM format (which normally are output to Aligned.out.sam file), normal standard output will go into Log.std.out
                                BAM_Unsorted           ... alignments in BAM format, unsorted. Requires --outSAMtype BAM Unsorted
                                BAM_SortedByCoordinate ... alignments in BAM format, sorted by coordinate. Requires --outSAMtype BAM SortedByCoordinate
                                BAM_Quant              ... alignments to transcriptome in BAM format, unsorted. Requires --quantMode TranscriptomeSAM

outReadsUnmapped                None
   string: output of unmapped and partially mapped (i.e. mapped only one mate of a paired end read) reads in separate file(s).
                                None    ... no output
                                Fastx   ... output in separate fasta/fastq files, Unmapped.out.mate1/2

outQSconversionAdd              0
   int: add this number to the quality score (e.g. to convert from Illumina to Sanger, use -31)

outMultimapperOrder             Old_2.4
    string: order of multimapping alignments in the output files
                                Old_2.4             ... quasi-random order used before 2.5.0
                                Random              ... random order of alignments for each multi-mapper. Read mates (pairs) are always adjacent, all alignment for each read stay together. This option will become default in the future releases.

### Output: SAM and BAM
outSAMtype                      SAM
    strings: type of SAM/BAM output
                                1st word:
                                BAM  ... output BAM without sorting
                                SAM  ... output SAM without sorting
                                None ... no SAM/BAM output
                                2nd, 3rd:
                                Unsorted           ... standard unsorted
                                SortedByCoordinate ... sorted by coordinate. This option will allocate extra memory for sorting which can be specified by --limitBAMsortRAM.

outSAMmode                      Full
    string: mode of SAM output
                                None ... no SAM output
                                Full ... full SAM output
                                NoQS ... full SAM but without quality scores

outSAMstrandField               None
    string: Cufflinks-like strand field flag
                                None        ... not used
                                intronMotif ... strand derived from the intron motif. This option changes the output alignments: reads with inconsistent and/or non-canonical introns are filtered out.

outSAMattributes                Standard
    string(s): a string of desired SAM attributes, in the order desired for the output SAM. Tags can be listed in any combination/order.
                                ***Presets:
                                None        ... no attributes
                                Standard    ... NH HI AS nM
                                All         ... NH HI AS nM NM MD jM jI MC ch                                                                    
                                ***Alignment:
                                NH          ... number of loci the reads maps to: =1 for unique mappers, >1 for multimappers. Standard SAM tag.
                                HI          ... multiple alignment index, starts with --outSAMattrIHstart (=1 by default). Standard SAM tag.
                                AS          ... local alignment score, +1/-1 for matches/mismateches, score* penalties for indels and gaps. For PE reads, total score for two mates. Stadnard SAM tag.
                                nM          ... number of mismatches. For PE reads, sum over two mates.
                                NM          ... edit distance to the reference (number of mismatched + inserted + deleted bases) for each mate. Standard SAM tag.
                                MD          ... string encoding mismatched and deleted reference bases (see standard SAM specifications). Standard SAM tag.
                                jM          ... intron motifs for all junctions (i.e. N in CIGAR): 0: non-canonical; 1: GT/AG, 2: CT/AC, 3: GC/AG, 4: CT/GC, 5: AT/AC, 6: GT/AT. If splice junctions database is used, and a junction is annotated, 20 is added to its motif value.
                                jI          ... start and end of introns for all junctions (1-based).
                                XS          ... alignment strand according to --outSAMstrandField.
                                MC          ... mate's CIGAR string. Standard SAM tag.
                                ch          ... marks all segment of all chimeric alingments for --chimOutType WithinBAM output.
```

## Captured Man Page

```text
No man page captured.
```

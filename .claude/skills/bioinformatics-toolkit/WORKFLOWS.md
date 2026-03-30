# Bioinformatics Workflows

Complete step-by-step analysis pipelines for common bioinformatics tasks.

## Table of Contents
- [Whole Genome Sequencing Analysis](#whole-genome-sequencing-analysis)
- [RNA-seq Differential Expression](#rna-seq-differential-expression)
- [16S rRNA Amplicon Analysis](#16s-rrna-amplicon-analysis)
- [Gene Prediction and Annotation](#gene-prediction-and-annotation)
- [Metagenome Analysis](#metagenome-analysis)
- [Variant Calling](#variant-calling)

---

## Whole Genome Sequencing Analysis

### Overview
Process raw sequencing reads, align to reference genome, and call variants.

### Prerequisites
- Reference genome in FASTA format
- Paired-end sequencing reads (FASTQ)
- Installed tools: `bwa`, `samtools`, `bcftools`

### Pipeline

```bash
#!/bin/bash
# WGS Analysis Pipeline

# 1. Setup
REF="reference.fasta"
READ1="sample_R1.fastq.gz"
READ2="sample_R2.fastq.gz"
OUTPUT_DIR="wgs_results"
THREADS=4

mkdir -p $OUTPUT_DIR

# 2. Index reference genome
echo "Indexing reference..."
bwa index $REF
samtools faidx $REF

# 3. Align reads
echo "Aligning reads..."
bwa mem -t $THREADS -R "@RG\\tID:sample1\\tSM:sample1\\tPL:ILLUMINA" \
  $REF $READ1 $READ2 | \
  samtools view -bS - > $OUTPUT_DIR/sample.bam

# 4. Sort alignments
echo "Sorting alignments..."
samtools sort -@ $THREADS -o $OUTPUT_DIR/sample.sorted.bam $OUTPUT_DIR/sample.bam

# 5. Mark duplicates
echo "Marking duplicates..."
samtools markdup $OUTPUT_DIR/sample.sorted.bam $OUTPUT_DIR/sample.dedup.bam

# 6. Index final BAM
echo "Indexing BAM..."
samtools index $OUTPUT_DIR/sample.dedup.bam

# 7. Generate alignment metrics
echo "Generating metrics..."
samtools flagstat $OUTPUT_DIR/sample.dedup.bam > $OUTPUT_DIR/flagstat.txt
samtools idxstats $OUTPUT_DIR/sample.dedup.bam > $OUTPUT_DIR/idxstats.txt

# 8. Call variants
echo "Calling variants..."
bcftools mpact -f $REF $OUTPUT_DIR/sample.dedup.bam | \
  bcftools call -mv -Oz -o $OUTPUT_DIR/variants.vcf.gz

# 9. Index VCF
bcftools index $OUTPUT_DIR/variants.vcf.gz

echo "Complete! Results in $OUTPUT_DIR"
```

### Output Files
- `sample.sorted.bam`: Sorted alignments
- `sample.dedup.bam`: Duplicate-marked alignments
- `variants.vcf.gz`: Compressed variant calls
- `flagstat.txt`: Alignment statistics

---

## RNA-seq Differential Expression

### Overview
Quantify gene expression from RNA-seq data and identify differentially expressed genes.

### Prerequisites
- Reference genome and annotation (GTF)
- RNA-seq reads
- Tools: `hisat2`, `samtools`, `htseq-count` (or featureCounts)

### Pipeline

```bash
#!/bin/bash
# RNA-seq Analysis Pipeline

# 1. Setup
REF="reference.fasta"
GTF="annotation.gtf"
READ1="sample_R1.fastq.gz"
READ2="sample_R2.fastq.gz"
THREADS=4

# 2. Build HISAT2 index
echo "Building index..."
hisat2-build $REF ref_index

# 3. Align reads
echo "Aligning reads..."
hisat2 -p $THREADS -x ref_index -1 $READ1 -2 $READ2 \
  -S sample.sam

# 4. Convert and sort
samtools view -bS sample.sam | samtools sort -o sample.sorted.bam
samtools index sample.sorted.bam

# 5. Count reads per gene
echo "Counting reads..."
htseq-count -f bam -r pos -s no -t exon -i gene_id \
  sample.sorted.bam $GTF > gene_counts.txt

# Alternative: featureCounts
# featureCounts -a $GTF -o counts.txt sample.sorted.bam

# 6. Differential expression (requires DESeq2 in R)
# See R script below

echo "Complete! Gene counts in gene_counts.txt"
```

### R Script for Differential Expression

```r
# differential_expression.R

# Install required packages
if (!require("DESeq2")) install.packages("DESeq2")
if (!require("ggplot2")) install.packages("ggplot2")

library(DESeq2)

# Read count data
count_data <- read.table("gene_counts.txt", header=FALSE, row.names=1)
colnames(count_data) <- c("control1", "control2", "treat1", "treat2")

# Create sample information
sample_info <- data.frame(
  condition = c("control", "control", "treated", "treated")
)
rownames(sample_info) <- colnames(count_data)

# Create DESeq2 object
dds <- DESeqDataSetFromMatrix(
  countData = count_data,
  colData = sample_info,
  design = ~ condition
)

# Run DESeq2
dds <- DESeq(dds)

# Get results
res <- results(dds, contrast=c("condition", "treated", "control"))

# Order by adjusted p-value
res_ordered <- res[order(res$padj), ]

# Save results
write.csv(as.data.frame(res_ordered), "differential_expression.csv")

# MA plot
pdf("ma_plot.pdf")
plotMA(res, main="DESeq2 MA Plot")
dev.off()

# PCA plot
vsd <- vst(dds, blind=FALSE)
pdf("pca_plot.pdf")
plotPCA(vsd, intgroup="condition")
dev.off()
```

---

## 16S rRNA Amplicon Analysis

### Overview
Analyze 16S rRNA gene amplicons for microbial community profiling.

### Prerequisites
- Demultiplexed FASTQ files
- QIIME2 or mothur (or use BLAST + custom scripts)

### Pipeline (QIIME2)

```bash
#!/bin/bash
# 16S Analysis with QIIME2

# 1. Import data
qiime tools import \
  --type 'SampleData[PairedEndSequencesWithQuality]' \
  --input-path demux-paired-end.qza \
  --output-path demux.qza \
  --input-format PairedEndFastqManifestPhred33V2

# 2. Quality control
qiime demux summarize \
  --i-data demux.qza \
  --o-visualization demux-summary.qzv

# 3. DADA2 denoising
qiime dada2 denoise-paired \
  --i-demultiplexed-seqs demux.qza \
  --p-trim-left-f 0 \
  --p-trim-left-r 0 \
  --p-trunc-len-f 240 \
  --p-trunc-len-r 200 \
  --o-table table.qza \
  --o-representative-sequences rep-seqs.qza \
  --o-denoising-stats stats.qza

# 4. Phylogenetic tree
qiime phylogeny align-to-tree-mafft-fasttree \
  --i-sequences rep-seqs.qza \
  --o-alignment aligned-rep-seqs.qza \
  --o-masked-alignment masked-aligned-rep-seqs.qza \
  --o-tree unrooted-tree.qza \
  --o-rooted-tree rooted-tree.qza

# 5. Alpha and beta diversity
qiime diversity core-metrics-phylogenetic \
  --i-phylogeny rooted-tree.qza \
  --i-table table.qza \
  --p-sampling-depth 1000 \
  --output-dir core-metrics-results

# 6. Taxonomic classification
qiime feature-classifier classify-sklearn \
  --i-classifier classifier.qza \
  --i-reads rep-seqs.qza \
  --o-classification taxonomy.qza

# 7. Visualize
qiime taxa barplot \
  --i-table table.qza \
  --i-taxonomy taxonomy.qza \
  --m-metadata-file sample-metadata.tsv \
  --o-visualization taxa-bar-plots.qzv
```

### Alternative: BLAST-based Analysis

```bash
# Merge paired reads
usearch -fastq_mergepairs R1.fq -reverse R2.fq -fastqout merged.fq

# Quality filter
usearch -fastq_filter merged.fq -fastq_maxee_rate 1.0 -fastaout filtered.fasta

# BLAST against 16S database
blastn -query filtered.fasta -db silva_16s_db \
  -outfmt 6 -max_target_seqs 1 -num_threads 4 \
  -out blast_results.txt

# Parse results for taxonomy
python scripts/parse_blast_taxonomy.py blast_results.txt
```

---

## Gene Prediction and Annotation

### Overview
Predict protein-coding genes in prokaryotic genomes and annotate functions.

### Pipeline

```bash
#!/bin/bash
# Gene Prediction and Annotation

GENOME="genome.fasta"
OUTPUT_DIR="annotation"

mkdir -p $OUTPUT_DIR

# 1. Predict genes with Prodigal
echo "Predicting genes..."
prodigal -i $GENOME -a $OUTPUT_DIR/proteins.faa \
  -d $OUTPUT_DIR/genes.fna \
  -f gff -o $OUTPUT_DIR/genes.gff \
  -p single

# 2. Functional annotation with BLAST
echo "Annotating functions..."
makeblastdb -in $OUTPUT_DIR/proteins.faa -dbtype prot -out proteins_db
blastp -query $OUTPUT_DIR/proteins.faa \
  -db nr -num_threads 4 \
  -evalue 1e-5 -max_target_seqs 5 \
  -outfmt "6 qseqid sseqid pident length mismatch gapopen qstart qend sstart send evalue bitscore stitle" \
  -out $OUTPUT_DIR/blast_annotations.tsv

# 3. HMMER for domain search
echo "Searching domains..."
hmmscan --domtblout $OUTPUT_DIR/pfam_domains.tbl \
  --cpu 4 pfam_db $OUTPUT_DIR/proteins.faa

# 4. tRNA prediction with tRNAscan-SE
echo "Predicting tRNAs..."
tRNAscan-SE -B -o $OUTPUT_DIR/trnas.txt $GENOME

# 5. rRNA prediction with barrnap
echo "Predicting rRNAs..."
barrnap --kingdom bac $GENOME > $OUTPUT_DIR/rrnas.gff

echo "Complete! Results in $OUTPUT_DIR"
```

---

## Metagenome Analysis

### Overview
Analyze shotgun metagenomic sequencing data.

### Pipeline

```bash
#!/bin/bash
# Metagenome Analysis

READS="metagenome.fastq.gz"
OUTPUT_DIR="metagenome_results"
THREADS=4

mkdir -p $OUTPUT_DIR

# 1. Quality control
echo "Quality control..."
fastqc $READS -o $OUTPUT_DIR/
trimmomatic SE -phred33 $READS \
  $OUTPUT_DIR/trimmed.fq.gz \
  LEADING:20 TRAILING:20 SLIDINGWINDOW:4:20 MINLEN:50

# 2. Host read removal (if needed)
bowtie2-build host_genome.fasta host_db
bowtie2 -x host_db -U $OUTPUT_DIR/trimmed.fq.gz \
  --very-sensitive -p $THREADS \
  --un-conc-gz $OUTPUT_DIR/nonhost.fq.gz \
  -S /dev/null

# 3. Assembly (optional)
echo "Assembling..."
megahit -r $OUTPUT_DIR/nonhost_1.fq.gz \
  -o $OUTPUT_DIR/assembly \
  -t $THREADS

# 4. Taxonomic profiling
echo "Profiling taxonomy..."
kraken2 --db kraken2_db --threads $THREADS \
  --report $OUTPUT_DIR/kraken_report.txt \
  --output $OUTPUT_DIR/kraken_output.txt \
  $OUTPUT_DIR/nonhost_1.fq.gz

# 5. Functional profiling
echo "Functional annotation..."
humann --input $OUTPUT_DIR/nonhost_1.fq.gz \
  --output $OUTPUT_DIR/humann_output \
  --threads $THREADS

echo "Complete!"
```

---

## Variant Calling

### Overview
Call SNPs and indels from sequencing data.

### Pipeline

```bash
#!/bin/bash
# Variant Calling Pipeline

REF="reference.fasta"
BAM="sample.dedup.bam"
OUTPUT_DIR="variants"
THREADS=4

mkdir -p $OUTPUT_DIR

# Freebayes variant calling
freebayes -f $REF -p 1 -C 2 -F 0.01 -t $THREADS \
  $BAM > $OUTPUT_DIR/raw_variants.vcf

# Filter variants
vcffilter -f "QUAL > 20 & DP > 10" \
  $OUTPUT_DIR/raw_variants.vcf > $OUTPUT_DIR/filtered_variants.vcf

# Normalize variants
bcftools norm -f $REF \
  $OUTPUT_DIR/filtered_variants.vcf -Oz \
  -o $OUTPUT_DIR/normalized_variants.vcf.gz

# Index VCF
bcftools index $OUTPUT_DIR/normalized_variants.vcf.gz

# Generate statistics
vcftools --vcf $OUTPUT_DIR/normalized_variants.vcf.gz \
  --freq --out $OUTPUT_DIR/frequency
vcftools --vcf $OUTPUT_DIR/normalized_variants.vcf.gz \
  --site-depth --out $OUTPUT_DIR/depth
vcftools --vcf $OUTPUT_DIR/normalized_variants.vcf.gz \
  --site-quality --out $OUTPUT_DIR/quality

echo "Complete! Variants in $OUTPUT_DIR"
```

---

## Workflow Tips

### General Best Practices

1. **Always use absolute paths or set variables** for file locations
2. **Check intermediate files** before proceeding to next step
3. **Log all commands** for reproducibility
4. **Use quality control tools** (FastQC, MultiQC) regularly
5. **Keep raw data read-only**: Work in copies
6. **Compress large files** with `gzip` or `pigz` (parallel gzip)

### Parallel Processing

```bash
# Use GNU parallel for multiple samples
ls *.fastq.gz | parallel -j 4 "process_sample {}"
```

### Resource Monitoring

```bash
# Monitor disk space
df -h

# Monitor memory
free -h

# Monitor running jobs
htop  # or top
```

### Automation

Save workflows as bash scripts with:
- Shebang line: `#!/bin/bash`
- Comments explaining each step
- Variables for easy customization
- Error checking with `set -e` (exit on error)

---

## Quick Reference Commands

```bash
# Count sequences in FASTA
grep -c "^>" sequences.fasta

# Extract sequence by ID
samtools faidx reference.fasta chr1:1000-2000

# Convert SAM to sorted BAM
samtools view -bS input.sam | samtools sort -o output.bam

# Count reads in BAM
samtools view -c aligned.bam

# Get FASTQ statistics
seqtk seq -A input.fastq | head -n 1000 | tee subset.fasta

# Compress FASTQ
gzip input.fastq

# Split FASTQ by read count
seqtk split input.fastq 1000000
```

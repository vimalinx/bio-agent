# Bioinformatics Tools Reference

Detailed reference for all bioinformatics tools available in this project.

## Table of Contents
- [BLAST](#blast)
- [HMMER](#hmmer)
- [bowtie2](#bowtie2)
- [bwa](#bwa)
- [samtools](#samtools)
- [prodigal](#prodigal)
- [ViennaRNA](#viennarna)
- [Biopython](#biopython)

---

## BLAST

**Purpose**: Basic Local Alignment Search Tool - finds regions of similarity between biological sequences.

**Version**: 2.16.0+
**Location**: `/usr/bin/blastn`

### Key Commands

#### blastn (Nucleotide-Nucleotide BLAST)

```bash
# Basic usage
blastn -query <input_file> -db <database> -out <output_file>

# Common parameters
blastn -query sequences.fasta -db nt \
  -out results.txt \
  -outfmt 6 \              # Tabular format
  -evalue 1e-10 \          # E-value threshold
  -num_threads 4 \         # Use 4 CPU cores
  -max_target_seqs 10      # Limit hits per query
```

### Output Formats (`-outfmt`)
- `0`: Pairwise (default)
- `5`: XML
- `6`: Tabular (best for parsing)
- `7`: Tabular with comments

### Example Workflows

```bash
# Local BLAST against custom database
makeblastdb -in reference.fasta -dbtype nucl -out mydb
blastn -query query.fasta -db mydb -out results.txt -outfmt 6

# Remote BLAST against NCBI
blastn -query sequence.fasta -db nt -remote -out results.txt
```

---

## HMMER

**Purpose**: Search sequence databases for homologs using profile hidden Markov models.

**Version**: 3.4
**Conda Package**: `hmmer`

### Key Commands

#### hmmscan
Search sequences against a profile database.

```bash
hmmscan --domtblout output.tbl pfam_db input.fasta
```

#### hmmsearch
Search profile against sequence database.

```bash
hmmsearch --tblout output.tbl profile.hmm sequence_db.fasta
```

### Key Parameters
- `--domtblout`: Domain table output format
- `--tblout`: Table output (simpler format)
- `-E`: E-value threshold (default: 10)
- `--cpu`: Number of CPU threads

---

## bowtie2

**Purpose**: Ultrafast, memory-efficient short read aligner.

**Location**: `/usr/bin/bowtie2`

### Key Commands

#### Building Index
```bash
bowtie2-build reference.fasta index_name
```

#### Alignment
```bash
# Single-end reads
bowtie2 -x index_name -U reads.fq -S output.sam

# Paired-end reads
bowtie2 -x index_name -1 reads1.fq -2 reads2.fq -S output.sam

# With parameters
bowtie2 -x index_name -U reads.fq -S output.sam \
  --very-sensitive \    # Preset sensitivity modes
  -p 4 \               # 4 threads
  --un-conc-gz unaligned_%#.fq  # Save unaligned reads
```

### Alignment Modes
- `--very-fast`: Fastest, least sensitive
- `--fast`: Fast alignment
- `--sensitive`: Balanced
- `--very-sensitive`: Most sensitive (default for most cases)

### Output Formats
- `-S`: SAM format
- `--sam-nohead`: SAM without header
- `--un-conc`: Unaligned pairs in separate files

---

## bwa

**Purpose**: Burrows-Wheeler Aligner for mapping low-divergent sequences.

**Location**: `/usr/bin/bwa`

### Key Commands

#### Index
```bash
bwa index reference.fasta
```

#### mem (Recommended)
```bash
# Align single-end
bwa mem reference.fasta reads.fq > aln.sam

# Align paired-end
bwa mem reference.fasta reads1.fq reads2.fq > aln.sam

# With parameters
bwa mem -t 4 -R "@RG\\tID:sample1\\tSM:sample1" \
  reference.fasta reads.fq > aln.sam
```

#### aln (Older algorithm)
```bash
bwa aln reference.fasta reads.fq > reads.sai
bwa samse reference.fasta reads.sai reads.fq > aln.sam
```

### Key Parameters
- `-t`: Threads
- `-M`: Mark shorter split hits as secondary
- `-R`: Read group header (important for GATK)

---

## samtools

**Purpose**: Suite of utilities for processing SAM/BAM/CRAM files.

**Version**: 1.21
**Location**: `/usr/bin/samtools`

### Common Commands

#### View (Convert formats)
```bash
# SAM to BAM
samtools view -bS input.sam -o output.bam

# BAM to SAM
samtools view -h input.bam > output.sam

# View specific regions
samtools view input.bam chr1:1000-2000

# Extract mapped reads only
samtools view -b -F 4 input.bam > mapped.bam
```

#### Sort
```bash
# Sort by coordinate
samtools sort input.bam -o sorted.bam

# Sort by name
samtools sort -n input.bam -o sorted_names.bam
```

#### Index
```bash
samtools index sorted.bam
# Creates sorted.bam.bai
```

#### Statistics
```bash
# Flag statistics
samtools flagstat aligned.bam

# Index statistics
samtools idxstats aligned.bam

# Coverage statistics
samtools depth aligned.bam > coverage.txt
```

#### Merge
```bash
samtools merge merged.bam sample1.bam sample2.bam sample3.bam
```

#### Filtering
```bash
# Extract properly paired reads
samtools view -b -f 2 input.bam > properly_paired.bam

# Extract reads with mapping quality >= 30
samtools view -b -q 30 input.bam > high_quality.bam

# Extract reads NOT mapped (-F 4)
samtools view -b -f 4 input.bam > unmapped.bam
```

### SAM Flags
- `1`: Paired
- `2`: Properly paired
- `4`: Unmapped
- `8`: Mate unmapped
- `16`: Reverse strand
- `32`: Mate on reverse strand

---

## prodigal

**Purpose**: Fast, accurate protein-coding gene prediction for prokaryotic genomes.

**Version**: 2.6.3
**Conda Package**: `prodigal`

### Usage

```bash
# Basic usage
prodigal -i genome.fasta -a proteins.faa -d genes.fna -o genes.gff

# Single genome mode (default)
prodigal -i genome.fasta -a proteins.faa \
  -d genes.fna -f gff -o genes.gff -p single

# Metagenomic mode
prodigal -i contigs.fasta -a proteins.faa \
  -d genes.fna -f gff -o genes.gff -p meta
```

### Key Parameters
- `-i`: Input file (FASTA)
- `-a`: Amino acid output (proteins)
- `-d`: Nucleotide gene output
- `-f`: Output format (gff, sco, gbk)
- `-o`: Output file
- `-p`: Procedure (single, meta)

### Output Formats
- `gff`: GFF format (recommended)
- `sco`: Simplified output
- `gbk`: GenBank format

---

## ViennaRNA

**Purpose**: RNA secondary structure prediction and analysis.

**Version**: 2.7.2
**Conda Package**: `viennarna`

### Key Commands

#### RNAfold
Predict minimum free energy (MFE) structure.

```bash
# Basic prediction
echo "GGGAAACCC" | RNAfold

# From file
RNAfold < sequence.fasta

# With constraints
RNAfold -C < sequence.fasta
```

#### RNAplfold
Calculate base pairing probabilities.

```bash
RNAplfold -W 150 -L 100 -u 1 < sequences.fasta
```

#### RNAcofold
Predict hybridization of two RNAs.

```bash
echo -e "GGGGGG\\nCCCCCC" | RNAcofold
```

### Key Parameters
- `-T`: Temperature (Celsius, default: 37)
- `-p`: Compute partition function
- `-d2`: Use dangling end energies
- `-noLP`: No lone pairs

---

## Biopython

**Purpose**: Python library for biological computation.

**Version**: 1.86
**Environment**: bio conda environment

### Common Operations

#### Reading Sequences

```python
from Bio import SeqIO

# Read FASTA file
for record in SeqIO.parse("sequences.fasta", "fasta"):
    print(f"ID: {record.id}")
    print(f"Length: {len(record.seq)}")
    print(f"Sequence: {record.seq}")
```

#### Sequence Manipulation

```python
from Bio.Seq import Seq

# Create sequence
seq = Seq("ATGGTG")

# Complement
complement = seq.complement()  # TACCAC

# Reverse complement
rev_comp = seq.reverse_complement()  # CACCAT

# Translate
protein = seq.translate()  # MV
```

#### BLAST with Biopython

```python
from Bio.Blast import NCBIWWW

# Online BLAST
result = NCBIWWW.qblast("blastn", "nt", "ATGGTG")

# Parse results
from Bio.Blast import NCBIXML
blast_record = NCBIXML.read(result)

for alignment in blast_record.alignments:
    print(f"Hit: {alignment.hit_id}")
```

#### Writing Sequences

```python
from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord

# Create sequence record
record = SeqRecord(
    Seq("ATGGTG"),
    id="seq1",
    description="Example sequence"
)

# Write to file
SeqIO.write(record, "output.fasta", "fasta")
```

---

## Environment Management

### Checking Tool Availability

```bash
# System tools
which blastn bowtie2 bwa samtools

# Conda packages in bio environment
conda activate bio
conda list | grep -E "(blast|bowtie|bwa|samtools|biopython)"

# Check versions
blastn -version
samtools --version
python -c "import Bio; print(Bio.__version__)"
```

### Installing Additional Tools

```bash
# Activate bio environment
conda activate bio

# Install from bioconda
conda install -c bioconda bedtools
conda install -c bioconda bcftools
conda install -c bioconda hisat2
```

---

## Performance Tips

1. **Use BAM instead of SAM**: Smaller file size, faster processing
2. **Compress intermediate files**: Use `.gz` extension
3. **Parallel processing**: Always use `-t` or `--num_threads`
4. **Stream when possible**: Pipe commands to avoid I/O
5. **Index files**: `samtools index` for random access

---

## File Format Quick Reference

| Format | Extension | Description |
|--------|-----------|-------------|
| FASTA | .fasta, .fa | Sequences |
| FASTQ | .fastq, .fq | Sequences + quality |
| SAM | .sam | Alignment (text) |
| BAM | .bam | Alignment (binary) |
| CRAM | .cram | Alignment (compressed) |
| GFF/GTF | .gff, .gtf | Genome annotation |
| VCF | .vcf | Variant calls |
| BED | .bed | Genomic intervals |

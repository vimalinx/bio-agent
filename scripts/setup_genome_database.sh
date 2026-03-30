#!/bin/bash
# 配置人类参考基因组数据库（GRCh38/hg38）
# 适合学习和研究使用

set -e

BASE_DIR="$HOME/bio_studio/shared_data/databases"
GENOME_DIR="$BASE_DIR/genomes/human/GRCh38"
echo "📁 数据库目录: $GENOME_DIR"

# 创建目录结构
mkdir -p "$GENOME_DIR"/{sequence,annotation,variation,transcripts}
cd "$GENOME_DIR"

echo "✅ 目录创建完成"
echo ""
echo "📥 开始下载基础数据库..."
echo ""

# ========================================
# 1. 参考基因组序列（FASTA）
# ========================================
echo "1️⃣ 下载参考基因组序列 (GRCh38)..."
wget -c ftp://ftp.ensembl.org/pub/release-112/fasta/homo_sapiens/dna/Homo_sapiens.GRCh38.dna.primary_assembly.fa.gz

echo "   解压中..."
gunzip -k Homo_sapiens.GRCh38.dna.primary_assembly.fa.gz

# 创建索引（用于 BLAST、BWA 等）
echo "   创建序列索引..."
samtools faidx Homo_sapiens.GRCh38.dna.primary_assembly.fa

echo "   ✅ 基因组序列完成"
echo ""

# ========================================
# 2. 基因注释（GTF）
# ========================================
echo "2️⃣ 下载基因注释..."
wget -c ftp://ftp.ensembl.org/pub/release-112/gtf/homo_sapiens/Homo_sapiens.GRCh38.112.gtf.gz

echo "   解压中..."
gunzip -k Homo_sapiens.GRCh38.112.gtf.gz

echo "   ✅ 基因注释完成"
echo ""

# ========================================
# 3. 参考转录本
# ========================================
echo "3️⃣ 下载参考转录本序列..."
wget -c ftp://ftp.ensembl.org/pub/release-112/fasta/homo_sapiens/cds/Homo_sapiens.GRCh38.cds.all.fa.gz
wget -c ftp://ftp.ensembl.org/pub/release-112/fasta/homo_sapiens/ncrna/Homo_sapiens.GRCh38.ncrna.fa.gz

echo "   解压中..."
gunzip -k Homo_sapiens.GRCh38.cds.all.fa.gz
gunzip -k Homo_sapiens.GRCh38.ncrna.fa.gz

echo "   ✅ 转录本完成"
echo ""

# ========================================
# 4. 已知变异（dbSNP）
# ========================================
echo "4️⃣ 下载 dbSNP 变异数据..."
wget -c ftp://ftp.ncbi.nlm.nih.gov/snp/latest_release/VCF/GCF_000001405.40/GCF_000001405.40.vcf.gz

echo "   创建索引..."
tabix -p vcf GCF_000001405.40.vcf.gz

echo "   ✅ 变异数据完成"
echo ""

# ========================================
# 5. 创建 BLAST 数据库
# ========================================
echo "5️⃣ 创建 BLAST 数据库（用于序列比对）..."
makeblastdb -in Homo_sapiens.GRCh38.dna.primary_assembly.fa \
           -dbtype nucl \
           -parse_seqids \
           -title "Human GRCh38 Primary Assembly" \
           -out human_grch38_blast

echo "   ✅ BLAST 数据库完成"
echo ""

# ========================================
# 6. 下载说明文档
# ========================================
echo "6️⃣ 下载说明文档..."
wget -O README.txt ftp://ftp.ensembl.org/pub/release-112/readme.txt

echo "   ✅ 文档下载完成"
echo ""

# ========================================
# 完成信息
# ========================================
echo "================================"
echo "✅ 人类基因组数据库配置完成！"
echo "================================"
echo ""
echo "📊 数据库内容："
du -sh "$GENOME_DIR"/*
echo ""
echo "📁 数据库位置: $GENOME_DIR"
echo ""
echo "🔍 验证安装："
echo "   - 序列文件: $(ls -lh Homo_sapiens.GRCh38.dna.primary_assembly.fa | awk '{print $5}')"
echo "   - 注释文件: $(ls -lh Homo_sapiens.GRCh38.112.gtf | awk '{print $5}')"
echo "   - BLAST DB: 已创建"
echo ""
echo "💡 下一步："
echo "   1. 测试查询: samtools faidx Homo_sapiens.GRCh38.dna.primary_assembly.fa 1"
echo "   2. 查看 gene 数: grep -c '^Gene' Homo_sapiens.GRCh38.112.gtf"
echo "   3. BLAST 测试: blastn -db human_grch38_blast -query <序列文件>"
echo ""

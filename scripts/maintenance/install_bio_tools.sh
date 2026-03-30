#!/bin/bash
set -e

# 尝试定位 mamba 或 conda
if command -v mamba &> /dev/null; then
    CONDA_CMD="mamba"
elif command -v conda &> /dev/null; then
    CONDA_CMD="conda"
else
    echo "❌ 找不到 mamba 或 conda。请确保已激活 Conda 环境。"
    exit 1
fi

echo "🧬 Bio Studio 生信工具补全脚本"
echo "=============================="
echo "工具: $CONDA_CMD"
echo "环境: $CONDA_DEFAULT_ENV"
echo ""

if [ -z "$CONDA_DEFAULT_ENV" ] || [ "$CONDA_DEFAULT_ENV" == "base" ]; then
    echo "⚠️  警告: 你似乎没有激活 'bio' 环境 (当前: ${CONDA_DEFAULT_ENV:-无})"
    echo "建议先运行: source activate bio"
    read -p "是否继续安装到当前环境? [y/N] " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# 定义要安装的生信工具列表 (来自 bioconda)
TOOLS=(
    "multiqc"       # 整合QC报告
    "seqkit"        # FASTA/Q 处理神器
    "mafft"         # 高速多序列比对
    "iqtree"        # 系统发育树构建
    "star"          # RNA-seq 比对标准
    "hisat2"        # RNA-seq 比对 (快速)
    "subread"       # 包含 featureCounts
    "fastp"         # 极速质控过滤
    "sra-tools"     # 下载 NCBI 数据 (fastq-dump)
)

echo "📦 准备安装以下工具 (Bioconda):"
for tool in "${TOOLS[@]}"; do
    echo "  - $tool"
done
echo ""

# 执行安装
echo "🚀 开始安装 (这可能需要几分钟)..."
$CONDA_CMD install -y -c bioconda -c conda-forge "${TOOLS[@]}"

echo ""
echo "✨ 安装完成！"
echo "📊 验证工具版本:"
echo "----------------"
tools_to_check=("multiqc" "seqkit" "mafft" "iqtree2" "STAR" "hisat2" "featureCounts" "fastp")
for tool in "${tools_to_check[@]}"; do
    if command -v $tool &> /dev/null; then
        echo "✅ $tool: $(command -v $tool)"
    else
        echo "⚠️  $tool: 未找到 (可能安装名不同或路径未刷新)"
    fi
done

echo ""
echo "✅ 所有生信软件补全成功。"

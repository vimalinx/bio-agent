#!/bin/bash
set -e  # 遇到错误立即停止

CONDA_EXE="${CONDA_EXE:-}"
if [[ -z "$CONDA_EXE" ]]; then
    if command -v mamba >/dev/null 2>&1; then
        CONDA_EXE="mamba"
    elif command -v conda >/dev/null 2>&1; then
        CONDA_EXE="conda"
    else
        echo "❌ 错误: 找不到 conda/mamba。请先激活/初始化 conda 后再运行。"
        exit 1
    fi
fi

echo "🧬 Bio Studio 环境补全脚本"
echo "=============================="
echo "目标环境: conda env 'bio'"
echo ""

if ! $CONDA_EXE env list | grep -q "^bio\b"; then
    echo "❌ 错误: 找不到 conda 环境 'bio'"
    echo "请先创建环境后再运行。"
    exit 1
fi

# 定义要安装的包列表
PACKAGES=(
    "pandas"
    "scipy"
    "matplotlib"
    "seaborn"
    "scikit-learn"
    "jupyter"
    "notebook"
    "pysam"
    "scanpy"  # 推荐：单细胞分析标准
    "openpyxl" # 推荐：读写Excel
)

echo "📦 准备安装以下软件包:"
for pkg in "${PACKAGES[@]}"; do
    echo "  - $pkg"
done
echo ""

# 执行安装
echo "🚀 开始安装..."
$CONDA_EXE run -n bio python -m pip install "${PACKAGES[@]}"

echo ""
echo "✨ 所有依赖安装完成！"
echo "📊 验证安装版本:"
$CONDA_EXE run -n bio python -m pip list | grep -E "pandas|scipy|matplotlib|seaborn|scikit-learn|jupyter|pysam|scanpy"

echo ""
echo "✅ 环境补全成功。你可以使用 './start.sh' 启动工作区了。"

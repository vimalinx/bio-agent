#!/bin/bash
set -e

# 配置路径
REPO_DIR="repositories/active/RFdiffusion"
MODELS_DIR="$REPO_DIR/models"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(dirname "$(dirname "$SCRIPT_DIR")")" # 回退两级到根目录

echo "🧬 RFdiffusion 设置脚本"
echo "========================"
echo "工作目录: $ROOT_DIR"

cd "$ROOT_DIR"

# 1. 检查仓库
if [ ! -d "$REPO_DIR" ]; then
    echo "⬇️  Cloning RFdiffusion repository..."
    git clone https://github.com/RosettaCommons/RFdiffusion.git "$REPO_DIR"
else
    echo "✅ RFdiffusion repository found."
fi

# 2. 下载模型 (如果尚未下载)
# 检查关键模型文件是否存在
if [ ! -f "$MODELS_DIR/Base_ckpt.pt" ]; then
    echo "⬇️  Downloading weights (This may take a while)..."
    echo "    Creating directory: $MODELS_DIR"
    mkdir -p "$MODELS_DIR"
    
    # 使用官方脚本下载
    bash "$REPO_DIR/scripts/download_models.sh" "$MODELS_DIR"
else
    echo "✅ Models already exist in $MODELS_DIR"
fi

# 3. 构建 Docker 镜像
if docker images | grep -q "rfdiffusion"; then
    read -p "⚠️  Docker image 'rfdiffusion' already exists. Rebuild? [y/N] " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "✅ Skipping build."
        exit 0
    fi
fi

echo "🐳 Building Docker image 'rfdiffusion'..."
echo "    This process compiles SE3-Transformer and other dependencies."
# 注意：Dockerfile 在 docker/ 子目录下
docker build -t rfdiffusion -f "$REPO_DIR/docker/Dockerfile" "$REPO_DIR"

echo ""
echo "✨ RFdiffusion setup complete!"
echo "   Test it with:"
echo "   docker run --rm --gpus all rfdiffusion --help"

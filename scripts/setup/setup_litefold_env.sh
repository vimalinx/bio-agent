#!/bin/bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DEFAULT_WORKSPACE_ROOT="$(dirname "$(dirname "$SCRIPT_DIR")")"

WORKSPACE_ROOT="$DEFAULT_WORKSPACE_ROOT"
PYTHON_EXECUTABLE="${BIO_STUDIO_PYTHON:-python}"
DRY_RUN=0

while [[ $# -gt 0 ]]; do
    case "$1" in
        --workspace-root)
            WORKSPACE_ROOT="$2"
            shift 2
            ;;
        --python-executable)
            PYTHON_EXECUTABLE="$2"
            shift 2
            ;;
        --dry-run)
            DRY_RUN=1
            shift
            ;;
        *)
            echo "错误: 不支持的参数: $1" >&2
            exit 1
            ;;
    esac
done

REQUIREMENTS_FILE="$WORKSPACE_ROOT/requirements-litefold-selfhosted.txt"

if [[ ! -f "$REQUIREMENTS_FILE" ]]; then
    echo "错误: 找不到 LiteFold requirements 文件: $REQUIREMENTS_FILE" >&2
    exit 1
fi

if ! command -v "$PYTHON_EXECUTABLE" >/dev/null 2>&1 && [[ ! -x "$PYTHON_EXECUTABLE" ]]; then
    echo "错误: 找不到 Python 可执行文件: $PYTHON_EXECUTABLE" >&2
    exit 1
fi

INSTALL_CMD=("$PYTHON_EXECUTABLE" -m pip install -r "$REQUIREMENTS_FILE")

echo "LiteFold 环境补全"
echo "=================="
echo "工作区: $WORKSPACE_ROOT"
echo "Python: $PYTHON_EXECUTABLE"
echo "Requirements: $REQUIREMENTS_FILE"
printf "命令:"
for arg in "${INSTALL_CMD[@]}"; do
    printf " %q" "$arg"
done
printf "\n"

if [[ "$DRY_RUN" -eq 1 ]]; then
    echo "dry-run: 未执行安装"
    exit 0
fi

"${INSTALL_CMD[@]}"

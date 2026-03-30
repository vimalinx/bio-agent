# Bio Studio AI 操作手册

> **重要**: 这是你的核心行为准则。每次开始工作前必须阅读本文件。

## 🧠 你是谁

你是 Bio Studio 的 AI 操作员，负责：
1. **部署工具** - 安装、配置、测试生物信息学工具
2. **运行分析** - 设计流程、执行分析、生成报告
3. **维护系统** - 保持环境稳定、文档更新

## 📍 关键路径

```
/run/media/vimalinx/Data/bio_studio/          # 或 ~/bio_studio (符号链接)
├── CLAUDE.md                 # 本文件 (必读)
├── docs/
│   ├── AI_TOOL_PROTOCOL.md   # 工具部署协议 ⚠️ 部署工具前必读
│   ├── AI_ANALYSIS_PROTOCOL.md # 分析执行协议 ⚠️ 跑分析前必读
│   ├── BEST_PRACTICES.md     # 踩坑记录
│   ├── ENVIRONMENT.md        # 当前环境快照
│   └── README.md             # 文档索引
├── lib/                      # 通用模块库
├── projects/                 # 分析项目 (每个项目独立)
├── mcp-servers/              # MCP 服务器
├── scripts/maintenance/       # 环境维护脚本
├── .claude/skills/           # AI 技能定义
├── tools/scripts/             # 工具部署/封装脚本
└── repositories/             # 外部工具源码
    └── active/               # 当前使用的仓库
        ├── Biomni/           # 生物医学 AI Agent
        ├── evo2/             # Evo 2 基因组大模型
        └── RFdiffusion/      # 蛋白质设计工具
```

## 🚨 核心规则 (必须遵守)

### 规则 1: 先读文档再动手
- 部署工具 → 先读 `docs/AI_TOOL_PROTOCOL.md`
- 跑分析 → 先读 `docs/AI_ANALYSIS_PROTOCOL.md`
- 不确定 → 先读 `docs/BEST_PRACTICES.md`

### 规则 2: 不要破坏现有环境
- 任何操作前，先运行 `python scripts/maintenance/generate_env_report.py` 并检查关键工具状态
- 如果发现异常，**停止操作**，先修复现有问题
- 操作完成后，**再次生成报告**，确保环境未被破坏

### 规则 3: 测试通过才算完成
- 工具部署 → 必须能 `--help` 且能跑示例
- 分析流程 → 必须有输出文件且内容正确
- 没测试 = 没完成

### 规则 4: 记录一切
- 每次部署/分析，更新 `docs/CHANGELOG.md`
- 踩坑了，更新 `docs/BEST_PRACTICES.md`
- 环境变了，运行 `python scripts/maintenance/generate_env_report.py`

### 规则 5: 失败要回滚
- 如果搞砸了，手动回滚变更（卸载包/删除仓库/恢复配置）
- 不要留下半成品状态

### 规则 6: 保持工作区洁癖
- **严禁**在根目录存放 `data/`, `notebooks/`, `test/` 等临时文件夹
- 所有分析必须在 `projects/<项目名>/` 下进行
- 根目录只允许系统级文件 (`lib/`, `docs/`, `scripts/`)

## 📋 常用操作清单

### 部署新工具
```bash
# 1. 阅读协议
cat docs/AI_TOOL_PROTOCOL.md

# 2. 安装/添加工具（按协议完成）

# 3. 生成/更新 Skill 模板
python tools/scripts/deploy_tool.py --scan

# 4. 记录环境快照
python scripts/maintenance/generate_env_report.py
```

### 创建分析项目
```bash
# 1. 阅读协议
cat docs/AI_ANALYSIS_PROTOCOL.md

# 2. 创建项目
python lib/create_project.py <项目名> --type <类型>

# 3. 设计并执行流程
cd projects/<项目名>/scripts
# 编辑 pipeline.py 或让 AI 自动生成
```

### 环境检查
```bash
# 完整报告
python scripts/maintenance/generate_env_report.py
```

### 回滚
```bash
# 手动回滚变更（示例）
conda remove -n bio <包名>
pip uninstall <包名>
rm -rf repositories/active/<工具名>
```

## 🔧 环境信息

- **Conda 环境**: `bio` (主环境)
- **激活命令**: `conda activate bio` 或 `source <conda_install>/bin/activate bio`（conda 安装路径可能不同）
- **Python**: 3.10.x
- **GPU**: RTX 5070 Ti (CUDA 可用)

### PATH 陷阱 ⚠️
在 Python 脚本中调用命令行工具时，必须显式设置 PATH：

```python
import os
conda_prefix = os.environ.get("CONDA_PREFIX")
conda_bin = f"{conda_prefix}/bin" if conda_prefix else "/path/to/envs/bio/bin"
os.environ["PATH"] = f"{conda_bin}:{os.environ.get('PATH', '')}"
```

## 📝 变更日志位置

所有变更记录在 `docs/CHANGELOG.md`，格式：
```markdown
## [日期] - 操作类型
- **操作**: 做了什么
- **结果**: 成功/失败
- **影响**: 对环境的影响
- **验证**: 如何验证
```

## 🆘 出问题怎么办

1. **停下来** - 不要继续操作
2. **保存现场** - 记录错误信息
3. **检查日志** - 项目内 `projects/<name>/logs/`
4. **尝试回滚** - 手动撤销变更
5. **报告用户** - 说明发生了什么、尝试了什么、需要什么帮助

## 🎯 成功标准

每次操作完成后，问自己：
- [ ] 测试通过了吗？
- [ ] 文档更新了吗？
- [ ] 原有功能还正常吗？
- [ ] 用户能立即使用吗？

全部是 ✅ 才算完成。

# bio-agent

`bio-agent` 是一个面向 agent 的生物信息技能调度原型，目标是把下面这条主流程做扎实：

用户自然语言需求 → AI 生成候选 plan → 用户选择 / 修改 / 批准 → 分阶段执行 → 结果与证据包回传

当前仓库重点包括：

- `lib/` 与 `scripts/`：控制面原型与 CLI
- `registry/`：skills / workflows / routing rules 注册表
- `registry/analysis_flows.yaml`：真实分析信息流注册表
- `schemas/`：request / plan / run 的结构约束
- `docs/system/`：系统页面与审计页面
- `reference/COMPARATIVE_ANALYSIS_REPORT.md`：仓库对比原始报告

## Grounded Workflow Families

当前优先支持的、带官方来源 grounding 的真实 workflow family 有 4 条：

- `rnaseq-differential-expression`
- `scrnaseq-preprocessing`
- `atacseq-differential-accessibility`
- `germline-short-variant-discovery`

这些 family 现在都同时具备：

- workflow registry 路由定义
- family / strategy profile 知识层
- example request / plan
- 真实分析信息流定义

分析信息流不是另一个 marketing 文档，而是显式记录：

- primary inputs
- reference inputs
- metadata inputs
- stage-level consumes / transforms / produces
- evidence points
- final delivery bundle

对应文件：

- `registry/workflow_knowledge.yaml`
- `registry/analysis_flows.yaml`
- `docs/system/data/real-bioinformatics-workflows.json`
- `docs/system/data/real-analysis-information-flows.json`

## Session Workflow

现在除了底层的 `propose / review / approve / draft / run-*` 子命令之外，还补了一条更适合 agent 使用的 session 主链路：

```bash
python3 scripts/bio_skill_system.py session-start \
  --session-dir sessions/demo-rnaseq \
  --request-text "I have bulk RNA-seq FASTQ files for treated and control samples and want a differential expression result bundle." \
  --goal "Generate candidate plans for RNA-seq differential expression analysis."

python3 scripts/bio_skill_system.py session-approve \
  --session-dir sessions/demo-rnaseq \
  --plan-id plan_rnaseq-differential-expression_conservative

python3 scripts/bio_skill_system.py session-render-plan \
  --session-dir sessions/demo-rnaseq \
  --approved \
  --output sessions/demo-rnaseq/editable-plan.md

# edit sessions/demo-rnaseq/editable-plan.md

python3 scripts/bio_skill_system.py session-approve \
  --session-dir sessions/demo-rnaseq \
  --plan-file sessions/demo-rnaseq/editable-plan.md \
  --reason "User accepted the edited plan after removing one manual checkpoint."

python3 scripts/bio_skill_system.py session-next-stage \
  --session-dir sessions/demo-rnaseq

python3 scripts/bio_skill_system.py session-status \
  --session-dir sessions/demo-rnaseq

python3 scripts/bio_skill_system.py session-history \
  --session-dir sessions/demo-rnaseq

python3 scripts/bio_skill_system.py session-export-console \
  --session-dir sessions/demo-rnaseq \
  --output sessions/demo-rnaseq/session-export.json

python3 scripts/bio_skill_system.py session-serve-console \
  --session-dir sessions/demo-rnaseq \
  --port 8040
```

session 目录会持续落盘这些工件：

- `request.json`
- `plans.json`
- `review.json`
- `approved-plan.json`
- `execution-draft.json`
- `run.json`
- `run-status.json`
- `run-review.json`
- `history.json`
- `session.json`

另外，`session-render-plan` 会导出一个带嵌入 YAML 计划块的 Markdown 编辑视图，适合人和 agent 协作修改后再回灌批准。
`history.json` 会记录 session 生命周期事件，包括开始、审批、审批理由、plan diff、推进阶段、暂停和恢复。
`session-export-console` 会把真实 session 目录导出成控制台页面可直接消费的 bundle JSON。
`session-serve-console` 会启动一个本地控制服务，同时托管 `docs/` 页面并暴露一个很薄的 session API。

## Runtime Truth Model

这个仓库现在不再把“skill 已定义”和“当前机器真能执行”混为一谈。

`execution-draft.json` 里会显式区分：

- `unresolved_skill_ids`：连 skill 定义都还没接上的占位项
- `unavailable_runtime_skill_ids`：skill 已定义，但当前机器没有对应可执行工具

`run-review.json` 也会显式区分：

- `blocking_issues`
- `future_issues`
- `delivery_issues`

当前默认行为是：

- 如果当前 stage 依赖的本地工具缺失，`session-next-stage` 会把 run 置为 `paused`
- `run_review.verdict` 会变成 `blocked`
- `history.json` 会追加 `run_blocked`

只有显式传入 `--allow-missing-tools` 时，才允许带着环境缺口继续推进。
即便这样把 run 推到完成，最终 verdict 也会是 `completed_with_environment_gaps`，而不是误报 `ready_to_deliver`。

这意味着：

- 仓库现在能真实表达“控制面已跑通，但本机环境不满足执行条件”
- 不会再把缺少本地 GATK 这类情况假装成绿色交付

## Recommended Trial

如果你想快速体验一条 grounded workflow family，推荐从 `germline-short-variant-discovery` 开始：

```bash
python3 scripts/bio_skill_system.py session-start \
  --session-dir sessions/germline-short-variants-demo \
  --workflow-family germline-short-variant-discovery \
  --strategy-profile bwa-gatk-hardfilter

python3 scripts/bio_skill_system.py session-approve \
  --session-dir sessions/germline-short-variants-demo \
  --plan-id plan_germline-short-variant-discovery_conservative

python3 scripts/bio_skill_system.py session-status \
  --session-dir sessions/germline-short-variants-demo
```

如果本机缺少当前 stage 需要的工具，系统会在推进时直接给出 `blocked`，而不是偷偷继续。

控制台页面现在支持三种加载方式：

- 默认 demo bundle：直接打开 `docs/system/bio-skill-console.html`
- URL bundle：`docs/system/bio-skill-console.html?bundle=data/session-export.json`
- 本地上传：在页面顶部点击 `Upload JSON`

如果你希望网页直接驱动本地 session，而不是只复制 CLI 命令，可以这样用：

- 启动本地控制服务：`python3 scripts/bio_skill_system.py session-serve-console --session-dir sessions/demo-rnaseq --port 8040`
- 本地 live 控制台：`http://127.0.0.1:8040/system/bio-skill-console.html`
- GitHub Pages + 本地 API：`https://vimalinx.xyz/bio-agent/system/bio-skill-console.html?api=http://127.0.0.1:8040`

本地控制服务现在默认只接受这些来源发起的浏览器 API 请求：

- `http://127.0.0.1:*`
- `http://localhost:*`
- `https://vimalinx.xyz`
- `https://www.vimalinx.xyz`

如果你要从别的网页 origin 调本地 API，需要启动时追加 `--allow-origin https://your-origin.example`。

现在网页里的 `Plan Editor` 也已经接上本地 API，可直接完成这条闭环：

- `Load Current`：拉取当前 candidate / approved plan 的 markdown 编辑视图
- `Upload Draft`：把本地改过的 `.md/.yaml/.json` 放进编辑器
- `Approve Edited`：直接把编辑后的文档重新批准回 session
- 侧栏 `+ New Session`：把请求框里的自然语言直接创建成一个新 session
- 侧栏 `Recent Sessions`：读取 `sessions_root` 下已有 session，点击即可切换查看和执行
- 侧栏搜索框：按 session id、状态、阶段、推荐 plan 等文本即时过滤
- 侧栏快速过滤：`All / Pinned / Needs Plan / In Run` 四档切换
- 侧栏本地归档：把不常用 session 隐藏出默认列表，通过 `Archived` 视图再恢复
- 侧栏本地 metadata：给 session 追加自定义 label 和 note，进入列表展示与搜索
- 侧栏布局切换：`Flat / Grouped`，可按 label 分组查看 session
- 分组折叠：`Grouped` 模式下每个 label 组可单独折叠/展开，并保存在本地
- 批量动作：对当前过滤结果一键 `Pin Visible / Archive Visible / Clear Visible Notes`
- Saved Views：把当前 `query / scope / layout` 保存成命名视图，后续一键切回
- Workflow Family Start：从控制台首页按 family 和 strategy profile 直接启动新 session
- Strategy Panel：审批前在控制台右侧显式查看当前 strategy、availability、warning，并可切换/重建 candidate plans
- 侧栏 pin：把关键 session 固定到列表顶部，状态保存在浏览器本地
- 中间主按钮：如果请求框内容被改过，会变成 `Start Session`；否则执行当前 session 的主动作，例如批准推荐 plan 或推进运行阶段

注意：当前实现里，重新批准一个编辑后的 plan 会重新初始化 run 工件，因此执行阶段会从 `s1` 重新开始。

本地控制服务当前提供这些端点：

- `GET /api/health`
- `GET /api/sessions`
- `POST /api/session/start`
- `GET /api/session/bundle`
- `GET /api/session/plan-markdown`
- `POST /api/session/action`

## Tests

当前仓库的标准测试入口是：

```bash
python3 -m pytest -q
```

或者：

```bash
bash scripts/ci/run_stable_tests.sh
```

## Documentation

- 系统页：`docs/system/bio-skill-system.html`
- 控制台页：`docs/system/bio-skill-console.html`
- 真实流程地图页：`docs/system/real-bioinformatics-workflow-map.html`
- 真实分析信息流页：`docs/system/real-analysis-information-flows.html`
- 四仓代码真实性审计页：`docs/system/biomed-repo-code-audit.html`

公开仓库：

- https://github.com/vimalinx/bio-agent

GitHub Pages 文档入口：

- https://vimalinx.xyz/bio-agent/

审计页子网址：

- https://vimalinx.xyz/bio-agent/system/biomed-repo-code-audit.html

## Status

这是一个正在快速演化中的原型仓库。
目前最清晰、最稳的部分是：

- plan-first 控制面
- grounded workflow family 路由
- session 工件持久化
- 本地控制台展示
- 真实分析信息流建模
- 缺工具时的运行时阻断与环境缺口表达

仍在补齐的部分主要是：

- 真正的 stage execution bridge
- 更多 workflow family / strategy profile
- console 内部对环境缺口的更细粒度可视化
- 更强的外部工具与远程执行集成

## License

MIT

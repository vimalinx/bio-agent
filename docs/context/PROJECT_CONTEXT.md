# PROJECT_CONTEXT

最后更新：2026-04-02

## 1. 项目是什么

`bio-agent` 是一个面向 agent 的生物信息技能调度原型，当前核心模式是：

用户自然语言需求
→ 生成候选 plan
→ 用户选择 / 修改 / 批准
→ 分阶段执行
→ 回传结果与证据包

当前最稳的部分不是具体生信算法执行，而是 plan-first 控制面、session 工件组织、控制台展示与基础 run-state 管理。

## 2. 当前仓库重点

高价值目录：
- `scripts/bio_skill_system.py`：主 CLI 入口
- `lib/bio_skill_system.py`：核心控制逻辑
- `lib/bio_skill_console_server.py`：本地控制台服务
- `registry/`：skills / workflows / routing 规则
- `registry/analysis_flows.yaml`：真实分析信息流定义
- `schemas/`：request / plan / run 结构约束
- `sessions/`：session 落盘工件
- `docs/system/`：系统页、控制台页、审计页
- `examples/`：request / plan / run 示例
- `tests/`：CLI、文档、控制台服务相关测试

辅助但非长期上下文源：
- `task_plan.md`
- `findings.md`
- `progress.md`

这些文件更像阶段性工作记录；项目级长期上下文应优先回写到本目录。

## 3. 当前已实现主链路

较清晰的使用方式：
- `session-start`
- `session-approve`
- `session-render-plan`
- 再次 `session-approve`（回灌编辑后的 plan）
- `session-next-stage`
- `session-status`
- `session-history`
- `session-export-console`
- `session-serve-console`

这条链路已经覆盖：
- 请求归档
- 候选 plans
- 审批
- 可编辑 plan 视图
- 分阶段推进
- session 历史
- 浏览器控制台消费

## 4. 关键对象

- `Request`：用户请求的结构化版本
- `Plan`：候选或已批准的执行方案
- `Review`：plan 推荐与比较结果
- `Execution Draft`：从 plan 到运行所需技能/阶段的草案
- `Run` / `Run Status`：执行阶段状态与摘要
- `Run Review`：阻塞项、未来风险、当前阶段判断
- `Session`：把上述对象组织成同一工作单元的持久化容器

## 5. Session 工件落盘约定

典型 session 目录包含：
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

示例可见：`sessions/demo-rnaseq/`

## 6. 浏览器与文档入口

- `docs/index.html`：静态文档入口
- `docs/system/bio-skill-system.html`：系统架构页
- `docs/system/bio-skill-console.html`：控制台页
- `docs/system/data/bio-skill-console-demo.json`：控制台 demo bundle

## 7. workflow 知识层

当前除了 registry 与 example plan 之外，项目已经新增一层更稳定的 workflow 知识层：
- `registry/workflow_knowledge.yaml`：结构化 family / stage / 管理规则
- `docs/context/WORKFLOW_KNOWLEDGE_BASE.md`：给人和 agent 共读的组织方法论
- `docs/system/real-bioinformatics-workflow-map.html`：官方来源驱动的可视化流程地图

这层的作用不是直接执行，而是给 request routing、candidate plan 设计、stage taxonomy 和后续 agent 管理提供 grounded 参考。

另外现在又补了一层更贴近“分析本身”的结构化数据：
- `registry/analysis_flows.yaml`：真实分析信息流定义，显式记录各 family 的 primary inputs、reference inputs、stage handoff、evidence points 和 delivery bundle
- `docs/system/real-analysis-information-flows.html`：面向人类阅读的可视化入口
- `docs/system/data/real-analysis-information-flows.json`：给静态页面或控制台消费的 JSON 版本

## 7. 当前实现边界

已相对成型：
- plan-first 控制面
- session 生命周期骨架
- 本地控制台页面与基础 API
- registry / schema / 示例数据
- 针对核心文档与 CLI 的自动化测试

仍需谨慎看待：
- 外部工具与真实生信运行环境的深度集成
- 项目级桥接层的一致性
- 部分历史文档与 README 对目录现状的同步程度
- 大规模技能资产与真实执行语义之间的闭环完整性

## 8. 已知注意点

- README 提到 `lib/` 与 `scripts/` 为控制面原型与 CLI；当前仓库中确实已有相关实现。
- `README.md` 里仍有少量文档链接/描述需要持续校准，例如某些页面命名与文档索引是否完全一致。
- 根目录已有 `CLAUDE.md`，但其内容更像外部 Bio Studio 总操作手册，不是本仓库专属上下文。
- `.gitignore` 当前忽略了 `task_plan.md`、`findings.md`、`progress.md`，说明这些文件偏本地过程记录。

## 9. 建议的后续上下文维护方式

每次做较大改动时，优先更新：
1. 本文件的“当前仓库重点 / 已实现主链路 / 当前实现边界”
2. `OPEN_QUESTIONS.md`
3. `WORKING_AGREEMENTS.md`
4. 必要时再更新 `README.md`

## 10. 对后续 agent 最重要的事实

- 这是一个“先 plan、后 approve、再 run”的系统，不应跳过审批语义。
- session 目录是当前最重要的状态落盘单元。
- `docs/system/` 已经是可用的演示与审查界面，不只是草稿。
- 真正的项目级上下文此前分散在 `README.md`、`task_plan.md`、`findings.md`、`progress.md`；本目录用于把这些信息收敛成更稳定的入口。

# bio-agent

`bio-agent` 是一个面向 agent 的生物信息技能调度原型，目标是把下面这条主流程做扎实：

用户自然语言需求 → AI 生成候选 plan → 用户选择 / 修改 / 批准 → 分阶段执行 → 结果与证据包回传

当前仓库重点包括：

- `lib/` 与 `scripts/`：控制面原型与 CLI
- `registry/`：skills / workflows / routing rules 注册表
- `schemas/`：request / plan / run 的结构约束
- `docs/system/`：系统页面与审计页面
- `reference/COMPARATIVE_ANALYSIS_REPORT.md`：仓库对比原始报告

## Documentation

- 系统页：`docs/system/bio-skill-system.html`
- 控制台页：`docs/system/bio-skill-console.html`
- 四仓代码真实性审计页：`docs/system/biomed-repo-code-audit.html`

部署到 GitHub Pages 后，文档入口页位于：

- `/bio-agent/`

审计页位于：

- `/bio-agent/system/biomed-repo-code-audit.html`

## Status

这是一个正在快速演化中的原型仓库。
目前最清晰、最稳的部分是 plan-first 控制面；项目级桥接和部分外部集成仍在补齐。

## License

MIT

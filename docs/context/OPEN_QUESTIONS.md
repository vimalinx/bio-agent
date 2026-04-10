# OPEN_QUESTIONS

## 当前待确认

1. `bio-agent` 的长期主入口应以 session 命令为中心，还是继续同时维护更底层的 `propose / review / approve / draft / run-*` 命令族？
2. registry 中的技能、workflow、routing 规则与真实可执行工具之间，哪些已经是生产可依赖映射，哪些仍然是原型层描述？
3. 文档体系中，哪些页面是“对外展示”，哪些是“对内实现说明”，是否需要更明确分层？
4. README 与 `docs/index.html` 是否要把“项目级上下文”入口正式纳入首页导航？
5. session API 的稳定边界是什么，未来是否会扩充更多本地控制动作？

## 当前风险

- 历史设计记录很多，但项目级稳定上下文入口此前缺失，后续维护容易继续分散。
- 部分文档反映的是阶段性状态，若不回写本目录，容易让后续 agent 读到过时结论。
- 控制面能力已经较丰富，但与真实外部生信工具环境的闭环程度仍需谨慎验证。

## 建议补充来源

后续若要继续充实本文件，优先核对：
- `README.md`
- `tests/`
- `scripts/bio_skill_system.py`
- `lib/bio_skill_system.py`
- `lib/bio_skill_console_server.py`
- `sessions/demo-rnaseq/`

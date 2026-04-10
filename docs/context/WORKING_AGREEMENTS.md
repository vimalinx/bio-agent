# WORKING_AGREEMENTS

## 面向后续 agent 的最小协作约定

1. 先检查 `docs/context/PROJECT_CONTEXT.md`，再决定改动入口。
2. 涉及主链路变化时，同时检查：
   - `README.md`
   - `docs/index.html`
   - `tests/`
3. 若改动 session 生命周期或控制台 API，至少同步更新：
   - `docs/context/PROJECT_CONTEXT.md`
   - 相关系统页或 README
4. 尽量把“长期有效的上下文”写进 `docs/context/`，不要只留在一次性工作记录里。
5. 如果发现 README 与真实实现不一致，以代码和测试为准，并回写文档。

## 推荐侦察顺序

1. `README.md`
2. `docs/context/PROJECT_CONTEXT.md`
3. `scripts/bio_skill_system.py`
4. `lib/bio_skill_system.py`
5. `tests/test_bio_skill_system_cli.py`
6. `tests/test_system_docs.py`

## 非目标

- 本目录不替代详细设计文档
- 本目录不记录逐次变更日志
- 本目录不保存临时实验结论

# WORKFLOW_KNOWLEDGE_BASE

最后更新：2026-04-03

## 1. 这份文档是干什么的

这不是又一篇“流程介绍”。它是给本地 agent 管理层看的 workflow 知识层，目的是回答两个问题：

1. 一个新的生信 workflow 应该如何组织？
2. 哪些真实流程已经被本项目视为优先支持对象？

它和 `registry/workflows.yaml` 的关系是：
- `workflows.yaml` 负责“系统当前有哪些 workflow 条目可路由”。
- 本文和 `registry/workflow_knowledge.yaml` 负责“workflow 家族应该如何建模、拆 stage、设置确认点和输出合同”。
- `registry/analysis_flows.yaml` 负责“每个 grounded family 的真实分析信息如何在 stage 之间流动，以及最后交付包由哪些 artifact 组成”。

## 2. workflow 组织原则

### 2.1 先按分析家族组织，不按工具名组织

本地 agent 不应该把 `STAR`、`MACS3`、`HaplotypeCaller` 当成 workflow 的一级单位。更稳定的做法是先按分析家族组织：

- bulk RNA-seq differential expression
- scRNA-seq preprocessing
- ATAC-seq differential accessibility
- germline short variant discovery

工具是 stage 内部的策略选择，而不是 workflow 家族本身。控制台中的 workflow family 卡片现在可以进一步选择 strategy profile，例如 RNA-seq 的 `STAR + featureCounts` 或 `Salmon + tximport`。

### 2.2 每个 workflow 家族要有 canonical stage chain

所谓 canonical stage chain，就是一条默认阶段骨架。它的作用不是限制实现，而是让不同 plan 可比较、可审查、可恢复。

建议统一遵守：
- `input-and-reference-check`
- `heavy-compute` 或其家族特化版本
- `intermediate-artifact-generation`
- `statistical-or-interpretive-stage`
- `report-review`

家族化落地时，可以映射成更具体的名字，例如 RNA-seq 里的 `qc-and-alignment`、variant 里的 `joint-genotyping`。

### 2.3 把 confirmation gate 设计成管理机制，而不是异常处理

下列场景默认应该进入确认点：
- 大规模 alignment / matrix generation / joint genotyping
- 外部参考资源下载
- 输出覆盖写入
- 物种或参考版本不明确
- 过滤策略存在重大歧义

### 2.4 输出合同必须写清楚

workflow 不是“跑完就算完成”，而是要有输出合同。输出合同至少应包括：
- 核心中间产物
- 最终统计或分析结果
- 人可复查的 summary / report
- 对应 validation rule

## 3. 当前已纳入的真实流程家族

### 3.1 bulk-rnaseq
- registry workflow: `rnaseq-differential-expression`
- 代表来源：nf-core/rnaseq、Galaxy RNA-seq tutorial
- canonical chain:
  - input-and-environment-check
  - qc-and-alignment
  - quantification
  - statistical-analysis
  - report-review

### 3.2 scrnaseq
- registry workflow: `scrnaseq-preprocessing`
- 代表来源：nf-core/scrnaseq、Galaxy scRNA preprocessing tutorial
- canonical chain:
  - input-and-reference-check
  - barcode-and-umi-processing
  - count-matrix-generation
  - qc-and-clustering
  - marker-review

### 3.3 atacseq
- registry workflow: `atacseq-differential-accessibility`
- 代表来源：nf-core/atacseq
- canonical chain:
  - input-and-reference-check
  - trim-and-align
  - filtering-and-qc
  - peak-calling-and-consensus
  - differential-accessibility-and-report

### 3.4 germline-short-variants
- registry workflow: `germline-short-variant-discovery`
- 代表来源：GATK Germline Discovery、GATK Hard Filtering、nf-core/sarek
- canonical chain:
  - input-and-reference-check
  - align-and-bqsr
  - gvcf-calling
  - joint-genotyping
  - filtering-and-review

## 4. 本地 agent 应该如何使用这层知识

建议顺序：
1. 先看 `registry/routing_rules.yaml` 和 `registry/workflows.yaml`，确认系统当前会怎么路由。
2. 再看 `registry/workflow_knowledge.yaml`，理解这个 family 的 stage 设计和管理规则。
3. 最后看 `examples/plans/*.yaml`，用示例 plan 生成或修改 candidate plan。

## 5. 后续扩展约定

新增 workflow family 时，至少同步更新：
- `registry/workflows.yaml`
- `registry/routing_rules.yaml`
- `registry/workflow_knowledge.yaml`
- `registry/analysis_flows.yaml`
- `examples/plans/<workflow>.plan.yaml`
- `examples/requests/<workflow>.request.json`
- `docs/system/real-bioinformatics-workflow-map.html`
- `docs/system/real-analysis-information-flows.html` / `docs/system/data/real-analysis-information-flows.json`

如果只改了一处，说明这还不是可管理知识，而只是局部说明。

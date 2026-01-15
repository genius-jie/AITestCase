@workflow_type: reusable
@usage_mode: hybrid
@enforcement: optional
@version: 1.1.0
@author: QA Team
@description: AI语音交互系统测试 6A 工业级工作流模板，作为 Agent 执行与推理的唯一阶段宪法
@created_at: 2026-01-14
@last_updated: 2026-01-14

# AI语音交互系统测试 6A 工作流（工业宪法模板）

## 核心定位
- 本文档是 **阶段定义与执行约束的唯一真理源**
- 不描述“如何实现”，只定义“必须产出什么”和“结构长什么样”
- 所有 Agent、脚本、Solo 执行均需遵循本 Workflow

---
## 阶段三件套生成与完成判定规范（强制约束）

### 1. 阶段最小完成定义（Definition of Done）

任一阶段（A1 ~ A6）被视为“执行完成”，必须同时满足以下条件：

1. 阶段 workflow.md 已被补全为**可执行状态**
2. 阶段 role.prompt.md 已被补全为**明确可调用的 Agent 身份定义**
3. 阶段 mistakes.md 已被补全，包含：
   - 本阶段高频错误模式
   - 风险触发条件
   - 规避与修正策略
4. 阶段结果文档（如 output.md）已生成，并与 workflow 定义的 outputs 一致

**缺失任一文件，均视为阶段未完成。**

---

### 2. 阶段三件套职责划分（不可省略）

每个阶段目录必须包含以下三类核心文档：

- `workflow.md`
  - 定义本阶段的执行目标、输入输出、Skeleton 结构
  - 作为 Agent 的阶段级“执行宪法”

- `role.prompt.md`
  - 定义本阶段 Agent 的身份、能力边界与执行策略
  - 必须与 workflow.md 中的 goal / outputs 严格对齐

- `mistakes.md`
  - 记录本阶段在历史执行中暴露的错误模式
  - 作为 Agent 执行时的风险约束与纠偏依据

上述三件套由 Agent 在阶段执行过程中 **自动生成或补全**，
不得仅保留模板或空壳内容。

---

### 3. Skeleton 与三件套的关系约束

- Skeleton 中定义的是：
  - 本阶段**结果文档的结构**
- 三件套定义的是：
  - 本阶段**如何被执行、由谁执行、如何避免失败**

Skeleton ≠ Workflow  
Skeleton ≠ Role  
Skeleton ≠ Mistakes  

Agent 不得仅生成 Skeleton 内容即宣告阶段完成。

---

### 4. Solo 执行对齐规则（硬约束）

在 Solo 执行模式下：

- 每个 stage 的执行目标，默认为：
  **“补全该阶段的三件套 + 生成阶段结果文档”**
- `solo_execute.yaml` 中声明的 output，
  不应被理解为唯一产物，而是阶段产物之一

若 Solo 执行结果未补全阶段三件套，
视为违反 Workflow 执行约束。

---

### 5. 演进与版本约束

- 阶段三件套可被 Agent 在执行后迭代更新
- Skeleton 结构未经版本升级不得擅自修改
- Workflow 版本升级必须记录：
  - 变更原因
  - 影响阶段
  - 对 Agent 行为的影响

## 阶段 A1：Analyze｜需求分析与规则提取
@phase_id: A1
@role: 业务规则解析Agent
@human_review: required
@upstream_phases: []

@goal:
- 将原始输入文档转化为“可测试、可执行、可验收”的结构化规则集合

@inputs:
- 原始需求文档
- 设计文档
- 接口文档
- 领域知识库（语音 / ASR / TTS / LM）

@outputs:
- 结构化需求清单
- 需求澄清与验收标准

@validation_rules:
- 无上游依赖，直接执行

@skeleton:
  sections:
    - 输入文档概览
    - 业务规则提取
    - 接口与参数约束
    - 质量与性能指标
    - 待澄清问题列表

---

## 阶段 A2：Architect｜流程架构与标准制定
@phase_id: A2
@role: 流程设计Agent
@human_review: optional
@upstream_phases: [A1]

@goal:
- 将需求规则转化为可协同执行的测试流程与产物标准

@inputs:
- A1 输出文档：结构化需求清单
- A1 输出文档：需求澄清与验收标准
- 数据契约模板
- 测试报告模板

@outputs:
- 测试架构设计文档
- Agent 协同调度手册

@validation_rules:
- 必须校验 A1 阶段已完成（三件套+结果文档）
- 必须校验 A1 输出的结构化需求清单已通过人工审核
- 必须校验 A1 输出的需求澄清与验收标准无未解决问题

@skeleton:
  sections:
    - 测试总体架构
    - 阶段划分与依赖关系
    - 中间产物契约定义
    - Agent 协作与触发规则

---

## 阶段 A3：Assemble｜资产聚合与标准化
@phase_id: A3
@role: 文档整理Agent
@human_review: required
@upstream_phases: [A1, A2]

@goal:
- 将分散产物固化为“可复用、可版本化”的测试资产

@inputs:
- A1 输出文档：结构化需求清单（需求分析报告）
- A1 输出文档：需求澄清与验收标准（需求分析报告）
- A2 输出文档：测试架构设计文档
- A2 输出文档：Agent 协同调度手册
- 知识库

@outputs:
- 测试任务拆分文档
- 标准化测试资产库
- 标准化数据契约

@validation_rules:
- 必须校验 A1 阶段已完成（三件套+结果文档）
- 必须校验 A2 阶段已完成（三件套+结果文档）
- 必须校验 A1 输出的需求分析报告已通过人工审核
- 必须校验 A2 输出的测试架构设计文档已完成

@skeleton:
  sections:
    - 可复用资产清单
    - 测试任务拆分结构
    - 资产版本与变更记录

---

## 阶段 A4：Automate｜数据构造与工具适配
@phase_id: A4
@role: 测试数据设计Agent / 工具适配Agent
@human_review: optional
@upstream_phases: [A3]

@goal:
- 生成“可直接被工具消费”的自动化测试输入资产

@inputs:
- A3 输出文档：测试任务拆分文档
- A3 输出文档：标准化测试资产库
- A3 输出文档：标准化数据契约（文档整理节点的输出）

@outputs:
- 测试数据集
- 工具参数化与适配说明

@validation_rules:
- 必须校验 A3 阶段已完成（三件套+结果文档）
- 必须校验 A3 输出的标准化数据契约已通过人工审核，未通过则拒绝执行
- 必须校验标准化数据契约的格式符合约定规范
- 必须校验测试资产库的完整性和可用性

@skeleton:
  sections:
    - 数据设计策略说明
    - 数据覆盖范围定义
    - 数据样例与格式
    - 工具适配说明

---

## 阶段 A5：Apply｜测试执行与问题调试
@phase_id: A5
@role: 执行调度Agent
@human_review: optional
@upstream_phases: [A4]

@goal:
- 自动化执行测试并定位问题根因

@inputs:
- A4 输出文档：测试数据集
- A4 输出文档：工具参数化与适配说明
- 测试脚本

@outputs:
- 测试执行日志
- 问题根因分析报告

@validation_rules:
- 必须校验 A4 阶段已完成（三件套+结果文档）
- 必须校验 A4 输出的测试数据集格式正确且完整
- 必须校验 A4 输出的工具参数化与适配说明符合要求
- 必须校验测试脚本与测试数据集的兼容性

@skeleton:
  sections:
    - 执行环境说明
    - 执行结果汇总
    - 异常与问题定位
    - 根因分析结论

---

## 阶段 A6：Assess｜结果评估与体系迭代
@phase_id: A6
@role: 报告生成Agent
@human_review: required
@upstream_phases: [A5]

@goal:
- 评估测试效果并反向优化流程与 Agent 能力

@inputs:
- A5 输出文档：测试执行日志
- A5 输出文档：问题根因分析报告
- 历史知识库

@outputs:
- 多维度评估报告
- 流程与 Agent 优化建议

@validation_rules:
- 必须校验 A5 阶段已完成（三件套+结果文档）
- 必须校验 A5 输出的测试执行日志完整且可解析
- 必须校验 A5 输出的问题根因分析报告已完成

@skeleton:
  sections:
    - 测试效果评估
    - 流程效率分析
    - Agent 表现评估
    - 优化建议与改进项

---

## 使用与演进原则
- 本 Workflow 可被 Agent 引用、继承、裁剪
- Skeleton 结构 **不得由脚本或 Agent 擅自修改**
- 版本升级必须记录差异与原因

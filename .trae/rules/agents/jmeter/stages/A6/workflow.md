@workflow_type: structural
@usage_mode: execution
@enforcement: executable
@version: 1.0.0
@author: QA Team
@description: A6阶段工作流 - 评估总结与体系迭代
@created_at: 2026-01-14
@last_updated: 2026-01-14

# A6 Assess - 评估总结与体系迭代

## 二、适用场景
- WebSocket性能测试评估总结
- 测试结果多维度评估
- 性能瓶颈分析与优化建议
- 测试体系迭代优化

## 三、核心特点
- ✅ 汇总全流程测试结果
- ✅ 生成多维度评估报告
- ✅ 输出性能瓶颈与优化建议
- ✅ 反向优化 workflow 与 agent 设计
- ✅ 补全 A6 阶段三件套文档

## 四、阶段划分

### 阶段1: 结果汇总
@phase_id: A6-1
@role: 结果汇总Agent
@output: [全流程测试结果汇总]
@human_review: required
@metadata:
  core_objectives: 汇总全流程测试结果
  key_nodes: 结果汇总审核节点
  references: stages/A1/output.md, stages/A2/output.md, stages/A3/output.md, stages/A4/output.md, stages/A5/output.md

#### 核心动作
1. 汇总A1-A5阶段的测试结果
2. 整合各阶段的输出文档
3. 生成全流程测试结果汇总
4. 输出结果汇总文档

### 阶段2: 多维度评估
@phase_id: A6-2
@role: 多维度评估Agent
@output: [多维度评估报告]
@human_review: required
@metadata:
  core_objectives: 生成多维度评估报告
  key_nodes: 评估报告审核节点
  references: 全流程测试结果汇总

#### 核心动作
1. 从多个维度评估测试结果
2. 评估系统性能表现
3. 评估测试过程和方法
4. 输出多维度评估报告

### 阶段3: 瓶颈分析与优化建议
@phase_id: A6-3
@role: 瓶颈分析与优化建议Agent
@output: [性能瓶颈与优化建议]
@human_review: required
@metadata:
  core_objectives: 输出性能瓶颈与优化建议
  key_nodes: 优化建议审核节点
  references: 多维度评估报告

#### 核心动作
1. 深入分析系统性能瓶颈
2. 提出针对性的优化建议
3. 评估优化建议的可行性和预期效果
4. 输出性能瓶颈与优化建议文档

### 阶段4: 测试体系迭代
@phase_id: A6-4
@role: 测试体系迭代Agent
@output: [测试体系迭代建议]
@human_review: required
@metadata:
  core_objectives: 反向优化 workflow 与 agent 设计
  key_nodes: 迭代建议审核节点
  references: 多维度评估报告, 性能瓶颈与优化建议

#### 核心动作
1. 评估当前测试流程的有效性
2. 提出workflow优化建议
3. 提出agent设计优化建议
4. 输出测试体系迭代建议

### 阶段5: 阶段文档补全
@phase_id: A6-5
@role: 文档补全Agent
@output: [补全后的阶段三件套文档]
@human_review: optional
@metadata:
  core_objectives: 补全阶段三件套文档
  key_nodes: 文档审核节点
  references: 所有前期输出文档

#### 核心动作
1. 补全A6阶段workflow.md执行细节
2. 强化A6阶段role.prompt.md中的职责、能力与输出要求
3. 在mistakes.md中沉淀本阶段易错点
4. 输出完整的阶段三件套文档

## 五、落地建议
- 文档先行：每个阶段启动前先生成对应节点工作流文档
- 保留人工入口：关键节点人工介入
- 可选使用 & 可组合使用：Agent可根据任务需求选择和覆盖模板
- 版本管理：记录版本变化

## 六、Skill能力映射

### 6.1 核心职责与能力需求分析
**A6阶段核心职责**：评估总结与体系迭代，汇总全流程测试结果，生成多维度评估报告，输出性能瓶颈与优化建议，反向优化workflow与agent设计。

### 6.2 针对性Skill能力映射

| 能力类别 | 适用Skill | 能力等级 | 应用场景 | 核心价值 |
|---------|---------|---------|---------|---------|
| **执行验证** | JMeter 执行层设计 | L4 | 结果分析、性能瓶颈分析、执行评估 | 提供结果分析和性能瓶颈分析能力，支持测试体系迭代 |
| **方法封装** | JMeter 方法层设计 | L3 | 测试流程评估、方法设计优化 | 评估测试方法设计的有效性，提出优化建议 |
| **组件配置** | JMeter 组件层设计 | L2 | 组件使用评估、配置优化 | 评估组件配置的合理性，提出改进建议 |
| **测试数据设计** | 接口测试数据设计 | L1 | 数据策略评估、数据使用优化 | 评估数据策略的执行效果，提出优化建议 |

### 6.3 阶段专属Skill能力配置

**A6阶段专属能力配置**：
- ✅ **JMeter 执行层设计**：用于结果分析、性能瓶颈分析和执行评估
- ✅ **JMeter 方法层设计**：用于测试流程评估和方法设计优化
- ✅ **JMeter 组件层设计**：用于组件使用评估和配置优化
- ✅ **接口测试数据设计**：用于数据策略评估和数据使用优化

**能力使用原则**：
- **多维度评估**：从多个维度评估测试结果和过程
- **体系迭代**：基于评估结果反向优化测试体系
- **持续改进**：不断优化测试流程和方法设计
- **价值导向**：关注测试的实际价值和效果

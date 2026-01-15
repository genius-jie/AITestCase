@workflow_type: structural
@usage_mode: execution
@enforcement: executable
@version: 1.0.0
@author: QA Team
@description: A2阶段工作流 - 测试架构与流程设计
@created_at: 2026-01-14
@last_updated: 2026-01-14

# A2 Architect - 测试架构与流程设计

## 适用场景
- 接口测试架构设计
- 基于A1输出设计整体接口测试架构
- 明确测试工具在体系中的角色与边界
- 设计数据流、执行流、结果流
- **业务规则变更时的架构文档更新**

## 核心特点
- ✅ 基于A1输出设计整体接口测试架构
- ✅ 明确测试工具在体系中的角色与边界
- ✅ 设计数据流、执行流、结果流
- ✅ 补全并优化A2阶段三件套文档
- ✅ **响应业务规则变更，更新架构设计文档**

## 阶段划分

### 阶段1: 测试架构设计
@phase_id: A2-1
@role: 测试架构设计Agent
@output: [测试架构设计文档]
@human_review: required
@metadata:
  core_objectives: 基于A1输出设计整体接口测试架构
  key_nodes: 架构审核节点
  references: stages/A1/output.md, 数据契约文档, 接口分析文档

#### 核心动作
1. 分析A1阶段输出的需求清单和业务规则
2. 分析数据契约文档和接口分析文档
3. 设计整体接口测试架构
4. 明确测试工具在体系中的角色与边界
5. 输出测试架构设计文档

### 阶段2: 流程设计
@phase_id: A2-2
@role: 流程设计Agent
@output: [数据流、执行流、结果流设计文档, 数据策略详细分析]
@human_review: required
@metadata:
  core_objectives: 设计数据流、执行流、结果流
  key_nodes: 流程审核节点
  references: 测试架构设计文档

#### 核心动作
1. 设计接口测试数据流
2. 设计接口测试执行流
3. 设计接口测试结果流
4. **进行数据策略详细分析**
   - 分析是否可以通过接口构造数据
   - 评估构造成本是否可接受
   - 验证数据构造的稳定性
5. **输出数据策略详细分析结果**
6. 输出流程设计文档

### 阶段3: Agent协同设计
@phase_id: A2-3
@role: Agent协同设计Agent
@output: [Agent协同调度手册]
@human_review: required
@metadata:
  core_objectives: 设计Agent协同机制
  key_nodes: 协同机制审核节点
  references: 测试架构设计文档, 流程设计文档

#### 核心动作
1. 设计Agent协同机制
2. 明确各Agent的职责和交互方式
3. 输出Agent协同调度手册

### 阶段4: 阶段文档补全
@phase_id: A2-4
@role: 文档补全Agent
@output: [补全后的阶段三件套文档]
@human_review: optional
@metadata:
  core_objectives: 补全阶段三件套文档
  key_nodes: 文档审核节点
  references: 所有前期输出文档

#### 核心动作
1. 补全A2阶段workflow.md执行细节
2. 强化A2阶段role.prompt.md中的职责、能力与输出要求
3. 在mistakes.md中沉淀本阶段易错点
4. 输出完整的阶段三件套文档

### 阶段5: 业务规则变更响应（跨阶段流程）
@phase_id: A2-5
@role: 架构文档更新Agent
@output: [更新后的架构设计文档]
@human_review: required
@upstream_phases: [A1]
@depends_on: [CROSS-FLOW-001-1]
@cross_flow: CROSS-FLOW-001
@metadata:
  core_objectives: 响应业务规则变更，更新架构设计文档
  key_nodes: 架构更新审核节点
  references: CROSS-FLOW-001, 业务规则变更影响分析报告

#### 核心动作
1. **分析业务规则变更影响**：
   - 识别变更的业务规则内容
   - 分析变更影响的接口、字段、场景
   - 确定对架构设计的影响程度

2. **更新接口依赖关系图**：
   - 根据业务规则变更更新接口依赖关系
   - 更新接口调用顺序
   - 更新变量传递关系

3. **更新测试架构设计**：
   - 根据业务规则变更更新测试架构
   - 更新场景设计规则
   - 在SCENARIO-004等场景规则中添加新的业务约束

4. **更新Agent协同调度手册**：
   - 根据架构变更更新Agent协同机制
   - 更新各Agent的职责和交互方式

5. **输出更新后的文档**：
   - 更新后的测试架构设计文档
   - 更新后的Agent协同调度手册
   - 变更历史记录

#### 更新原则
- **完整性原则**：所有受影响的架构设计内容都必须更新
- **一致性原则**：更新后的架构设计必须与业务规则保持一致
- **可追溯原则**：所有变更都必须记录变更原因、日期和影响范围
- **验证原则**：更新后必须验证架构设计的正确性

#### 触发条件
- 业务规则文档（如OTA测试业务规则约定.md）发生变更
- 接口文档发生变更
- 测试需求发生变更
- 发现业务规则与实际实现不一致

#### 输出内容
- 变更内容摘要
- 影响的架构设计部分
- 更新后的接口依赖关系图
- 更新后的测试架构设计
- 更新后的场景设计规则
- 变更历史记录

## 落地建议
- 文档先行：每个阶段启动前先生成对应节点工作流文档
- 保留人工入口：关键节点人工介入
- 可选使用 & 可组合使用：Agent可根据任务需求选择和覆盖模板
- 版本管理：记录版本变化
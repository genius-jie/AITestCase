@workflow_type: structural
@usage_mode: execution
@enforcement: executable
@version: 1.0.0
@author: QA Team
@description: A1阶段工作流 - 需求分析与规则提取
@created_at: 2026-01-14
@last_updated: 2026-01-14

# A1 Analyze - 需求分析与规则提取

## 适用场景
- 接口测试需求分析
- 基于原始需求提取可测试规则
- 明确接口测试目标与约束

## 核心特点
- ✅ 从原始需求中提取可测试业务规则
- ✅ 明确接口测试目标、约束条件与关键指标
- ✅ 补全阶段执行细节
- ✅ 沉淀本阶段易错点

## 阶段划分

### 阶段1: 需求收集与分析
@phase_id: A1-1
@role: 需求分析Agent
@output: [需求清单, 需求澄清文档, 数据策略初步分析]
@human_review: required
@metadata:
  core_objectives: 收集并分析原始需求
  key_nodes: 需求对齐节点
  references: 数据契约文档, 接口分析文档

#### 核心动作
1. 读取数据契约文档
2. 读取接口分析文档
3. **访问接口文档时，检查是否遇到404错误**
4. **如果遇到404错误，立即中断执行，提示用户重新提供正确的接口文档链接**
5. **禁止基于推测的内容进行分析，所有内容必须基于实际接口文档**
6. 生成结构化需求清单
7. **输出需求澄清文档，待澄清问题列表必须包含：问题ID、接口名称、URL文档、问题描述、优先级、建议解决方案**
8. **如果确实没有URL文档，URL文档列可以留空**
9. **进行数据策略初步分析**
   - 分析是否依赖已有业务实体
   - 识别"数据前置条件"
   - 评估业务约束强度
10. **输出数据策略初步分析结果**

### 阶段2: 业务规则提取
@phase_id: A1-2
@role: 业务规则提取Agent
@output: [可测试业务规则清单]
@human_review: required
@metadata:
  core_objectives: 提取可测试业务规则
  key_nodes: 规则验证节点
  references: 需求清单, 需求澄清文档

#### 核心动作
1. 基于需求清单提取可测试业务规则
2. 验证业务规则的可测试性
3. 输出可测试业务规则清单

### 阶段3: 接口测试目标定义
@phase_id: A1-3
@role: 接口测试目标定义Agent
@output: [接口测试目标文档]
@human_review: required
@metadata:
  core_objectives: 定义接口测试目标、约束条件与关键指标
  key_nodes: 目标确认节点
  references: 可测试业务规则清单

#### 核心动作
1. 明确接口测试目标
2. 定义接口测试约束条件
3. 确定关键接口测试指标
4. 输出接口测试目标文档

### 阶段4: 阶段文档补全
@phase_id: A1-4
@role: 文档补全Agent
@output: [补全后的阶段三件套文档]
@human_review: optional
@metadata:
  core_objectives: 补全阶段三件套文档
  key_nodes: 文档审核节点
  references: 所有前期输出文档

#### 核心动作
1. 补全A1阶段workflow.md执行细节
2. 强化A1阶段role.prompt.md中的职责、能力与输出要求
3. 在mistakes.md中沉淀本阶段易错点
4. 输出完整的阶段三件套文档

## 落地建议
- 文档先行：每个阶段启动前先生成对应节点工作流文档
- 保留人工入口：关键节点人工介入
- 可选使用 & 可组合使用：Agent可根据任务需求选择和覆盖模板
- 版本管理：记录版本变化
@workflow_type: business
@usage_mode: execution
@enforcement: executable

# Prompt Architect工作流

## 阶段1: 需求解析

### 步骤1.1: 解析用户需求
- 操作：分析用户提供的模糊需求
- 输入：用户需求
- 输出：需求分析结果

### 步骤1.2: 锁定核心要素
- 操作：明确Agent Identity、Core Task、Constraints、Audience
- 输入：需求分析结果
- 输出：核心要素清单

### 步骤1.3: 补齐缺失要素
- 操作：若任一核心要素缺失，补齐默认约束
- 输入：核心要素清单
- 输出：完整的核心要素清单

## 阶段2: Prompt类型判定

### 步骤2.1: 判定Prompt类型
- 操作：根据需求判定是通用能力Prompt还是具体业务Prompt
- 输入：完整的核心要素清单
- 输出：Prompt类型判定结果

### 步骤2.2: 确定设计规范
- 操作：根据Prompt类型确定设计规范
- 输入：Prompt类型判定结果
- 输出：设计规范

## 阶段3: Prompt架构设计

### 步骤3.1: 设计Prompt结构
- 操作：根据设计规范设计Prompt的整体结构
- 输入：设计规范
- 输出：Prompt结构设计

### 步骤3.2: 编写Role & Objectives
- 操作：编写Agent的角色和目标
- 输入：核心要素清单
- 输出：Role & Objectives部分

### 步骤3.3: 设计Core Workflow
- 操作：设计Agent的核心工作流
- 输入：核心要素清单
- 输出：Core Workflow部分

### 步骤3.4: 制定Rules & Constraints
- 操作：制定Agent必须遵循的规则和约束
- 输入：核心要素清单
- 输出：Rules & Constraints部分

### 步骤3.5: 添加Skills & Knowledge
- 操作：添加Agent所需的技能和知识
- 输入：核心要素清单
- 输出：Skills & Knowledge部分

### 步骤3.6: 设计Few-Shot Examples
- 操作：设计可验证的Few-Shot示例
- 输入：核心要素清单
- 输出：Few-Shot Examples部分

### 步骤3.7: 定义Output Format
- 操作：定义Agent的输出格式
- 输入：核心要素清单
- 输出：Output Format部分

## 阶段4: 具体业务Prompt设计（若适用）

### 步骤4.1: 设计六阶段工作流
- 操作：设计初始化、测试数据生成、测试执行、结果分析、优化迭代、最终交付的工作流
- 输入：设计规范
- 输出：六阶段工作流

### 步骤4.2: 添加业务特定要素
- 操作：添加文件职责、依赖关系、迭代式调试流程、决策树、交付文件清单、命令执行规范
- 输入：设计规范
- 输出：业务特定要素

## 阶段5: 自检验证

### 步骤5.1: 检查结构完整性
- 操作：检查Prompt结构是否完整，无模块缺失
- 输入：完整的Prompt
- 输出：结构检查结果

### 步骤5.2: 检查规则一致性
- 操作：检查Prompt中是否有冲突规则
- 输入：完整的Prompt
- 输出：规则一致性检查结果

### 步骤5.3: 验证Few-Shot
- 操作：验证Few-Shot与目标是否一致
- 输入：完整的Prompt
- 输出：Few-Shot验证结果

### 步骤5.4: 检查指令语气
- 操作：检查Prompt的指令语气是否统一
- 输入：完整的Prompt
- 输出：指令语气检查结果

### 步骤5.5: 验证可执行性
- 操作：验证Prompt是否可独立执行
- 输入：完整的Prompt
- 输出：可执行性验证结果

## 阶段6: 输出最终Prompt

### 步骤6.1: 整合所有部分
- 操作：整合Prompt的所有部分
- 输入：Prompt的各个部分
- 输出：完整的Prompt

### 步骤6.2: 控制长度
- 操作：确保Prompt总长度≤10000字
- 输入：完整的Prompt
- 输出：最终的Prompt

### 步骤6.3: 输出结果
- 操作：输出最终的System Prompt
- 输入：最终的Prompt
- 输出：System Prompt

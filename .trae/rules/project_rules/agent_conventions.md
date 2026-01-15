# Agent使用规范

## 1. Agent目录结构

每个Agent必须遵循以下目录结构：

```
agents/
├── agent_name/
│   ├── role.prompt.md   # Agent的身份和能力定义
│   ├── workflow.md      # Agent的执行流程
│   └── mistakes.md      # Agent的错题本
```

## 2. Agent三件套规范

### 2.1 role.prompt.md

- 清晰的角色定位
- 明确的核心目标
- 详细的核心能力
- 严格的行为准则
- 简洁的语言描述

### 2.2 workflow.md

- 必须包含语义标签
- 清晰的阶段划分
- 详细的步骤描述
- 明确的输入输出

### 2.3 mistakes.md

- 完整的错误记录
- 详细的根因分析
- 有效的解决方案
- 明确的验证结果
- 有价值的经验教训

## 3. Workflow使用规范

### 3.1 语义标签

所有workflow文件必须在顶部声明语义标签：

```
@workflow_type: structural | project | business
@usage_mode: design | generation | execution
@enforcement: reference_only | generate_only | executable
```

## 4. 错题本使用规范

### 4.1 错误记录条件

当遇到以下情况时，应记录到错题本：
- Agent执行失败
- 生成的结果不符合预期
- 发现设计缺陷
- 遇到新的错误类型

### 4.2 错误记录格式

错误记录应包含：
- 错误基本信息
- 错误描述
- 根因分析
- 解决方案
- 验证结果
- 经验教训

---

**创建时间**：2026-01-14
**最后更新**：2026-01-14

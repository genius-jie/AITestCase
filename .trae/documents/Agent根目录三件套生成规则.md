# 通用Agent自举生成计划

## 1. 核心原则
- **输入**：仅原始需求文档
- **输出**：目标Agent三件套（role.prompt.md / workflow.md / mistakes.md）
- **依据**：project_rules + project_design（不依赖拍脑袋决策）
- **适用范围**：任何类型的Agent自举生成

## 2. 自举生成流程

### 阶段1：需求分析与模型构建
- **输入**：原始需求文档
- **操作**：
  1. 提取核心目标：明确Agent需要解决的问题
  2. 识别技术约束：确定可用工具、技术栈和限制
  3. 分析典型场景：梳理Agent需要处理的主要业务场景
  4. 定义能力边界：明确Agent的职责范围和限制
- **输出**：需求分析报告（内部文档）
- **依据**：project_rules中的需求分析方法

### 阶段2：Role Prompt设计与生成
- **输入**：需求分析报告
- **操作**：
  1. 基于 `project_design/agent_design.md` 模板
  2. 定义Agent角色定位：明确专业领域和核心能力
  3. 设定核心职责：列出Agent需要执行的主要任务
  4. 确定能力边界：明确Agent不能做什么
  5. 定义输入输出格式：规范Agent的交互方式
  6. 制定工作原则：设定Agent的行为准则
- **输出**：role.prompt.md文件
- **依据**：project_design/agent_design.md

### 阶段3：Workflow设计与生成
- **输入**：需求分析报告 + role.prompt.md
- **操作**：
  1. 基于 `project_design/workflow_design.md` 模板
  2. 划分执行阶段：根据业务流程设计清晰的阶段
  3. 设计阶段步骤：每个阶段包含具体的执行步骤
  4. 明确输入输出：每个步骤定义清晰的输入和输出
  5. 添加语义标签：@workflow_type: business, @usage_mode: execution, @enforcement: executable
- **输出**：workflow.md文件
- **依据**：project_design/workflow_design.md

### 阶段4：Mistakes Notebook设计与生成
- **输入**：需求分析报告 + role.prompt.md + workflow.md
- **操作**：
  1. 基于 `project_design/agent_design.md` 中的错题本模板
  2. 收集典型错误场景：针对目标Agent的常见错误
  3. 每个错误包含：基本信息、错误描述、根因分析、解决方案、验证结果
  4. 格式符合错题本规范
- **输出**：mistakes.md文件
- **依据**：project_design/agent_design.md

### 阶段5：验证与优化
- **输入**：生成的Agent三件套文件
- **操作**：
  1. 格式验证：检查文件格式是否符合规范
  2. 内容完整性：确保所有必要内容都已包含
  3. 一致性检查：确保三件套之间内容一致
  4. 可执行性验证：确认workflow可执行
  5. 命名规范：检查文件和目录命名是否符合要求
- **输出**：验证报告
- **依据**：project_rules中的文件管理和命名规范

## 3. 技术实现细节

### 3.1 文档模板复用
- 严格使用 `project_design/` 目录下的模板文件
- 确保生成的文档格式统一、结构清晰
- 便于后续维护和扩展

### 3.2 语义标签管理
- 所有文档必须包含正确的语义标签
- 标签用于区分文档类型、使用模式和执行方式
- 便于系统识别和处理

### 3.3 版本控制
- 生成的文件应包含创建时间和版本信息
- 便于追踪变更历史
- 支持回滚和更新

## 4. 输出结果

### 4.1 目录结构
```
agents/
└── [agent_name]/
    ├── role.prompt.md     ✅ 身份与能力定义
    ├── workflow.md        ✅ 执行流程
    └── mistakes.md        ✅ 行为矫正
```

### 4.2 质量标准
- 文档内容清晰、准确、完整
- 符合项目设计规范
- 易于理解和执行
- 支持后续扩展和维护

## 5. 适用场景

- **新Agent创建**：从无到有生成完整的Agent三件套
- **现有Agent升级**：基于新需求更新Agent配置
- **跨领域Agent复用**：将现有Agent模式应用到新领域
- **标准化Agent建设**：确保所有Agent遵循统一规范

## 6. 执行保障

- 严格遵循project_rules中的各项约束
- 基于project_design中的设计指南
- 确保生成的Agent可直接用于实际业务场景
- 支持后续的持续优化和迭代

该计划提供了一个通用的Agent自举生成框架，可以根据不同的原始需求文档，生成符合规范的Agent三件套，实现真正的自举链路。
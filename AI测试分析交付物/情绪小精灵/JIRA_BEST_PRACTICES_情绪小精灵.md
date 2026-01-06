# Jira项目管理最佳实践 - 情绪小精灵

## 项目概述

### 项目信息

- **项目名称**：情绪小精灵
- **项目类型**：Software项目
- **开发模式**：Scrum敏捷开发
- **项目周期**：16周（8个Sprint，每个2周）
- **团队规模**：5人（产品经理、技术负责人、开发人员、测试人员、Scrum Master）

### 项目目标

- 开发一款具有5种情绪人格的智能陪伴设备
- 支持多设备互动和社交功能
- 提供高质量的语音交互体验
- 确保系统稳定性和安全性

---

## Jira项目配置

### 1. 项目类型选择

**选择Software项目的原因**

- 涉及代码开发、构建和发布
- 需要敏捷迭代管理（Sprint/Backlog）
- 需要复杂的工作流（审批、代码评审）
- 需要版本管理和发布跟踪

**配置步骤**

1. [ ] 登录Jira，点击"创建项目"
2. [ ] 选择"Software"项目类型
3. [ ] 选择"Scrum"开发模式
4. [ ] 填写项目名称：情绪小精灵
5. [ ] 填写项目Key：EMOJI（建议）
6. [ ] 选择项目模板：Scrum Software Development
7. [ ] 点击"创建项目"

---

### 2. Issue类型配置

#### Issue类型定义

**Epic（史诗）**

- **定义**：大型功能模块，跨越多个Sprint，需要多个Story完成
- **使用场景**：
  - 小精灵人设和语言风格系统
  - 语音系统
  - 多精灵交互系统
  - 社交功能
  - 物理按键系统
  - 灯光交互系统
  - 电量管理系统
  - 敏感词过滤系统

**字段要求**：
- Summary（必填）
- Description（必填，包含功能概述、验收标准）
- Priority（必填）
- Epic Name（必填）
- Assignee
- Labels（如"hardware"、"firmware"、"cloud"、"app"）

**Story（用户故事）**

- **定义**：从用户角度描述的功能需求，可在一个Sprint内完成
- **使用场景**：
  - 用户可以通过语音指令唤醒设备
  - 用户可以通过语音调整音量
  - 用户可以通过语音调整亮度
  - 用户可以添加好友
  - 多台设备靠近时可以触发互动

**字段要求**：
- Summary（必填，格式："作为[角色]，我想要[功能]，以便[价值]"）
- Description（必填，包含用户故事、验收标准、业务规则）
- Priority（必填）
- Epic Link（必填，关联到对应的Epic）
- Assignee
- Story Points（估算）
- Sprint（关联到Sprint）
- Labels
- Acceptance Criteria（验收标准）
- Test Cases（测试用例）

**Task（任务）**

- **定义**：具体的开发任务，通常在1-3天内完成
- **使用场景**：
  - 实现快乐人格的语言风格库
  - 实现唤醒词识别算法
  - 编写单元测试
  - 优化性能

**字段要求**：
- Summary（必填）
- Description（必填，包含任务描述、验收标准、技术要求）
- Priority（必填）
- Assignee
- Time Tracking（预估时间、实际时间）
- Labels
- Parent（关联到对应的Story）

**Bug（缺陷）**

- **定义**：需要修复的问题或缺陷
- **使用场景**：
  - 唤醒识别准确率低于预期
  - 人格切换有延迟
  - 灯光效果不正确
  - 电量监控不准确

**字段要求**：
- Summary（必填）
- Description（必填，包含Bug描述、复现步骤、期望行为、实际行为、环境信息）
- Priority（必填）
- Severity（严重程度）
- Assignee
- Labels
- Affects Version（受影响的版本）
- Fix Version（修复版本）
- Attachment（附件：截图、日志、视频）

**Sub-task（子任务）**

- **定义**：Story或Task的子任务，用于进一步拆分工作
- **使用场景**：
  - 实现语言风格库的子任务
  - 编写测试用例的子任务

**字段要求**：
- Summary（必填）
- Description（必填）
- Priority（必填）
- Assignee
- Time Tracking
- Labels
- Parent（关联到父Issue）

#### Issue类型配置步骤

1. [ ] 进入项目设置 → Issue Types
2. [ ] 确认已创建以下Issue类型：Epic、Story、Task、Bug、Sub-task
3. [ ] 为每个Issue类型配置必填字段
4. [ ] 为每个Issue类型配置可选字段
5. [ ] 为每个Issue类型配置工作流
6. [ ] 保存配置

---

### 3. 工作流配置

#### Story工作流

**工作流状态**：
```
To Do → In Progress → In Review → Done
```

**状态说明**：
- **To Do**：待办状态，Story已创建但未开始
- **In Progress**：进行中状态，Story正在开发中
- **In Review**：评审中状态，Story已完成开发，等待Code Review和测试
- **Done**：已完成状态，Story已通过测试并合并到主分支

**流转规则**：
- To Do → In Progress：开发人员开始开发
- In Progress → In Review：开发人员完成开发
- In Review → Done：测试人员验证通过
- In Review → In Progress：测试人员验证失败，返回修改

#### Bug工作流

**工作流状态**：
```
New → In Progress → In Review → Done
```

**状态说明**：
- **New**：新建状态，Bug已创建但未开始修复
- **In Progress**：进行中状态，Bug正在修复中
- **In Review**：评审中状态，Bug已修复，等待验证
- **Done**：已完成状态，Bug已修复并验证通过

**流转规则**：
- New → In Progress：开发人员开始修复
- In Progress → In Review：开发人员完成修复
- In Review → Done：测试人员验证通过
- In Review → In Progress：测试人员验证失败，返回继续修复

#### 工作流配置步骤

1. [ ] 进入项目设置 → Workflows
2. [ ] 创建Story工作流
3. [ ] 添加状态：To Do、In Progress、In Review、Done
4. [ ] 添加流转：To Do → In Progress、In Progress → In Review、In Review → Done、In Review → In Progress
5. [ ] 为每个流转设置条件和权限
6. [ ] 保存工作流
7. [ ] 将工作流关联到Story Issue类型
8. [ ] 重复步骤2-7，创建Bug工作流

---

### 4. 字段配置

#### 必填字段

**Epic必填字段**：
- Summary
- Description
- Priority
- Epic Name

**Story必填字段**：
- Summary
- Description
- Priority
- Epic Link
- Story Points

**Task必填字段**：
- Summary
- Description
- Priority
- Parent

**Bug必填字段**：
- Summary
- Description
- Priority
- Severity

#### 可选字段

**Epic可选字段**：
- Assignee
- Labels
- Component
- Fix Version

**Story可选字段**：
- Assignee
- Labels
- Component
- Sprint
- Acceptance Criteria
- Test Cases

**Task可选字段**：
- Assignee
- Labels
- Component
- Time Tracking

**Bug可选字段**：
- Assignee
- Labels
- Component
- Affects Version
- Fix Version
- Attachment

#### 自定义字段

**Story自定义字段**：
- Acceptance Criteria（验收标准）：多行文本字段
- Test Cases（测试用例）：多行文本字段

**Bug自定义字段**：
- Severity（严重程度）：单选字段（Blocker、Critical、Major、Minor、Trivial）
- Environment（环境信息）：多行文本字段

#### 字段配置步骤

1. [ ] 进入项目设置 → Fields
2. [ ] 检查必填字段配置
3. [ ] 检查可选字段配置
4. [ ] 创建自定义字段
5. [ ] 为自定义字段配置显示和编辑权限
6. [ ] 保存配置

---

### 5. 版本配置

#### 版本规划

**Alpha版本（v1.0.0-alpha）**
- 发布时间：Sprint 3结束（第6周）
- 包含功能：
  - 小精灵人设和语言风格系统（5种人格）
  - 语音系统（唤醒/待机、睡眠模式、音量调整、亮度调整）
  - 物理按键系统
  - 灯光交互系统
  - 电量管理系统

**Beta版本（v1.0.0-beta）**
- 发布时间：Sprint 6结束（第12周）
- 包含功能：
  - Alpha版本所有功能
  - 多精灵交互系统
  - 社交功能
  - 敏感词过滤系统

**正式版本（v1.0.0）**
- 发布时间：Sprint 8结束（第16周）
- 包含功能：
  - Beta版本所有功能
  - 性能优化
  - 用户体验优化
  - Bug修复

#### 版本配置步骤

1. [ ] 进入项目设置 → Versions
2. [ ] 创建版本：v1.0.0-alpha
3. [ ] 设置版本发布日期：第6周
4. [ ] 创建版本：v1.0.0-beta
5. [ ] 设置版本发布日期：第12周
6. [ ] 创建版本：v1.0.0
7. [ ] 设置版本发布日期：第16周
8. [ ] 保存配置

---

### 6. Sprint配置

#### Sprint规划

**Sprint 1**（第1-2周）
- 目标：完成基础框架和核心功能
- Story Points：13
- 主要内容：
  - 物理按键系统
  - 电量管理系统

**Sprint 2**（第3-4周）
- 目标：完成核心功能开发
- Story Points：61
- 主要内容：
  - 小精灵人设和语言风格系统（5种人格）
  - 语音系统（唤醒/待机）
  - 灯光交互系统

**Sprint 3**（第5-6周）
- 目标：完成功能完善和优化
- Story Points：42
- 主要内容：
  - 人格自动切换
  - 睡眠模式
  - 音量和亮度调整

**Sprint 4**（第7-8周）
- 目标：完成多精灵交互系统基础功能
- Story Points：26
- 主要内容：
  - 多精灵互动触发
  - 防打扰逻辑
  - 角色分配机制

**Sprint 5**（第9-10周）
- 目标：完成多精灵音效和社交功能
- Story Points：43
- 主要内容：
  - 2-6只设备音效
  - 社交功能

**Sprint 6**（第11-12周）
- 目标：完成敏感词过滤和边界处理
- Story Points：16
- 主要内容：
  - 敏感词过滤系统
  - 电量不足处理

**Sprint 7**（第13-14周）
- 目标：完成系统集成和测试
- Story Points：待定
- 主要内容：
  - 集成测试
  - 系统测试
  - Bug修复

**Sprint 8**（第15-16周）
- 目标：完成优化和发布准备
- Story Points：待定
- 主要内容：
  - 性能优化
  - 用户体验优化
  - 文档完善
  - 发布准备

#### Sprint配置步骤

1. [ ] 进入项目设置 → Sprints
2. [ ] 创建Sprint 1
3. [ ] 设置Sprint开始日期：第1周
4. [ ] 设置Sprint结束日期：第2周
5. [ ] 设置Sprint目标：完成基础框架和核心功能
6. [ ] 重复步骤2-5，创建Sprint 2-8
7. [ ] 保存配置

---

### 7. 权限配置

#### 角色定义

**产品经理（Product Owner）**
- 负责需求分析和验收
- 负责Epic和Story的创建和优先级设置
- 负责Sprint Backlog的规划
- 负责产品决策

**技术负责人（Tech Lead）**
- 负责技术方案评审
- 负责代码评审
- 负责技术决策
- 负责技术债务管理

**开发人员（Developers）**
- 负责Task的开发和实现
- 负责Bug的修复
- 负责代码提交和Code Review
- 负责单元测试

**测试人员（QA）**
- 负责测试用例编写
- 负责功能测试和集成测试
- 负责Bug的发现和验证
- 负责测试报告

**Scrum Master**
- 负责Sprint管理
- 负责进度跟踪
- 负责团队协调
- 负责流程改进

#### 权限配置

**产品经理权限**：
- 创建和编辑Epic、Story
- 设置优先级和Story Points
- 规划Sprint Backlog
- 验收Story和Bug

**技术负责人权限**：
- 评审技术方案
- 进行Code Review
- 设置技术标签
- 管理技术债务

**开发人员权限**：
- 创建和编辑Task
- 提交代码
- 进行Code Review
- 修复Bug

**测试人员权限**：
- 创建和编辑Bug
- 编写测试用例
- 验证Bug
- 生成测试报告

**Scrum Master权限**：
- 管理Sprint
- 跟踪进度
- 协调团队
- 改进流程

#### 权限配置步骤

1. [ ] 进入项目设置 → Permissions
2. [ ] 创建角色：Product Owner、Tech Lead、Developers、QA、Scrum Master
3. [ ] 为每个角色配置权限
4. [ ] 将团队成员分配到对应角色
5. [ ] 保存配置

---

## Jira Issue管理最佳实践

### 1. Epic管理最佳实践

#### Epic创建原则

- **单一职责**：每个Epic只负责一个大型功能模块
- **可拆分性**：Epic应该能够拆分为多个Story
- **可交付性**：Epic应该有明确的交付物和验收标准
- **可追踪性**：Epic应该有明确的优先级和版本规划

#### Epic命名规范

- 格式：[功能模块名称]
- 示例：
  - 小精灵人设和语言风格系统
  - 语音系统
  - 多精灵交互系统

#### Epic描述规范

- **功能概述**：简要描述Epic的功能和目标
- **验收标准**：列出Epic完成的标准
- **技术要求**：列出Epic的技术要求
- **依赖关系**：列出Epic之间的依赖关系

#### Epic验收标准

- 所有Story都已完成
- 所有Story都通过了测试
- 所有Story都符合验收标准
- 没有未解决的Bug
- 文档已更新

---

### 2. Story管理最佳实践

#### Story创建原则

- **用户视角**：Story应该从用户角度描述功能
- **可测试性**：Story应该有明确的验收标准
- **可估算性**：Story应该能够准确估算Story Points
- **可交付性**：Story应该在一个Sprint内完成

#### Story命名规范

- 格式：作为[角色]，我想要[功能]，以便[价值]
- 示例：
  - 作为用户，我想要体验快乐人格的陪伴，以便在需要时获得积极、兴奋的情感支持
  - 作为用户，我想要通过语音指令唤醒设备，以便开始与kikigo的互动

#### Story描述规范

- **用户故事**：使用"作为[角色]，我想要[功能]，以便[价值]"的格式
- **验收标准**：列出Story完成的标准，应该具体、可测试
- **业务规则**：列出Story的业务规则，应该清晰、无歧义
- **技术要求**：列出Story的技术要求，应该明确、可执行

#### Story Points估算

- **相对估算**：Story Points应该基于相对复杂度，而不是绝对时间
- **斐波那契数列**：使用斐波那契数列（1, 2, 3, 5, 8, 13, 21）进行估算
- **团队共识**：Story Points应该由团队共同估算，达成共识
- **定期回顾**：定期回顾Story Points的准确性，调整估算方法

#### Story验收标准

- 所有验收标准都已满足
- 所有Task都已完成
- 代码已通过Code Review
- 功能已通过测试
- 文档已更新

---

### 3. Task管理最佳实践

#### Task创建原则

- **可执行性**：Task应该能够直接执行，不需要进一步拆分
- **可估算性**：Task应该能够准确估算时间
- **可追踪性**：Task应该有明确的负责人和截止日期
- **可测试性**：Task应该有明确的验收标准

#### Task命名规范

- 格式：[动作] + [对象]
- 示例：
  - 实现快乐人格的语言风格库
  - 实现唤醒词识别算法
  - 编写单元测试

#### Task描述规范

- **任务描述**：详细描述任务内容和目标
- **验收标准**：列出任务完成的标准
- **技术要求**：列出任务的技术要求
- **依赖关系**：列出任务之间的依赖关系

#### Task时间估算

- **小时估算**：Task应该以小时为单位估算时间
- **1-3天完成**：Task应该在1-3天内完成，避免过大的Task
- **定期更新**：定期更新Task的实际时间，对比预估时间
- **持续改进**：根据实际时间调整估算方法

#### Task验收标准

- 任务已完成
- 验收标准已满足
- 代码已通过Code Review
- 测试已通过

---

### 4. Bug管理最佳实践

#### Bug创建原则

- **可复现性**：Bug应该能够准确复现
- **可描述性**：Bug应该清晰描述问题和影响
- **可追踪性**：Bug应该有明确的优先级和严重程度
- **可验证性**：Bug应该能够验证修复效果

#### Bug命名规范

- 格式：[模块] + [问题描述]
- 示例：
  - 快乐人格在用户低落时回应不正确
  - 唤醒识别准确率低于预期
  - 灯光效果不正确

#### Bug描述规范

- **Bug描述**：详细描述Bug的表现和影响
- **复现步骤**：详细列出如何复现Bug
- **期望行为**：描述期望的正确行为
- **实际行为**：描述实际观察到的行为
- **环境信息**：列出操作系统、设备型号、软件版本等
- **附件**：提供截图、日志、视频等

#### Bug优先级定义

- **Critical**：系统崩溃或无法使用，必须立即修复
- **High**：核心功能部分不可用，尽快修复
- **Medium**：次要功能有bug，按计划修复
- **Low**：界面小问题，有时间再修复

#### Bug严重程度定义

- **Blocker**：阻塞整个系统或核心功能
- **Critical**：严重影响用户体验
- **Major**：影响部分功能
- **Minor**：影响较小
- **Trivial**：几乎不影响使用

#### Bug修复流程

1. 测试人员创建Bug
2. 开发人员分析Bug
3. 开发人员修复Bug
4. 开发人员提交代码
5. 测试人员验证Bug
6. Bug验证通过，关闭Bug
7. Bug验证失败，返回开发人员继续修复

---

### 5. Sprint管理最佳实践

#### Sprint Planning

**Sprint Planning会议**：
- 时间：每个Sprint开始前，2小时
- 参与人员：产品经理、技术负责人、开发人员、测试人员、Scrum Master
- 目标：规划Sprint Backlog，确定Sprint目标

**Sprint Planning流程**：
1. 产品经理介绍Sprint目标
2. 团队讨论Sprint Backlog中的Story
3. 团队估算Story Points
4. 团队确认Sprint容量
5. 团队选择Story放入Sprint Backlog
6. 团队确认Sprint目标

**Sprint Planning输出**：
- Sprint Backlog
- Sprint目标
- Story分配

#### Daily Standup

**每日站会**：
- 时间：每天上午，15分钟
- 参与人员：开发人员、测试人员、Scrum Master
- 目标：同步进度，发现和解决问题

**每日站会流程**：
1. 每个人回答三个问题：
   - 昨天完成了什么？
   - 今天计划做什么？
   - 有什么阻碍？
2. Scrum Master记录问题和阻碍
3. Scrum Master跟进问题解决

**每日站会输出**：
- 进度同步
- 问题发现
- 阻碍解决

#### Sprint Review

**Sprint评审会议**：
- 时间：每个Sprint结束时，1-2小时
- 参与人员：产品经理、技术负责人、开发人员、测试人员、Scrum Master
- 目标：评审Sprint成果，演示功能

**Sprint Review流程**：
1. 团队演示Sprint完成的功能
2. 产品经理评审功能
3. 团队收集反馈
4. 团队记录问题和改进建议

**Sprint Review输出**：
- 功能演示
- 产品反馈
- 改进建议

#### Sprint Retrospective

**Sprint回顾会议**：
- 时间：每个Sprint结束时，1小时
- 参与人员：开发人员、测试人员、Scrum Master
- 目标：回顾Sprint过程，改进流程

**Sprint Retrospective流程**：
1. 团队回顾Sprint过程中的优点
2. 团队回顾Sprint过程中的问题
3. 团队讨论改进措施
4. 团队制定改进计划

**Sprint Retrospective输出**：
- 优点总结
- 问题总结
- 改进措施
- 改进计划

---

### 6. 版本管理最佳实践

#### 版本发布流程

1. **版本规划**：确定版本发布时间和包含功能
2. **版本开发**：开发版本包含的功能
3. **版本测试**：测试版本包含的功能
4. **版本发布**：发布版本到生产环境
5. **版本监控**：监控版本运行情况
6. **版本维护**：修复版本中的Bug

#### 版本发布检查清单

- [ ] 所有计划功能都已完成
- [ ] 所有功能都通过了测试
- [ ] 所有Bug都已修复
- [ ] 文档已更新
- [ ] 发布说明已编写
- [ ] 回滚计划已准备
- [ ] 监控指标已配置

#### 版本回滚流程

1. 发现严重问题
2. 评估问题影响
3. 决定是否回滚
4. 执行回滚操作
5. 验证回滚结果
6. 分析问题原因
7. 修复问题
8. 重新发布

---

### 7. 报表和监控最佳实践

#### 关键指标

**进度指标**：
- Story完成率
- Task完成率
- Bug修复率
- Sprint完成率

**质量指标**：
- Bug数量
- Bug修复时间
- 代码评审通过率
- 测试通过率

**效率指标**：
- Story Points完成速度
- Task完成时间
- Bug修复时间
- 代码评审时间

#### 报表类型

**Sprint燃尽图**：
- 显示Sprint剩余工作量
- 帮助团队了解Sprint进度
- 及时发现进度偏差

**版本燃尽图**：
- 显示版本剩余工作量
- 帮助团队了解版本进度
- 及时发现进度偏差

**Bug趋势图**：
- 显示Bug数量变化趋势
- 帮助团队了解代码质量
- 及时发现质量问题

**速度图**：
- 显示团队完成Story Points的速度
- 帮助团队了解团队效率
- 及时调整Sprint规划

#### 监控频率

- **每日监控**：Sprint燃尽图、Bug数量
- **每周监控**：版本燃尽图、Bug趋势图
- **每月监控**：速度图、质量指标

---

## Jira使用技巧

### 1. 快捷键

**全局快捷键**：
- `c`：创建Issue
- `.`：快速搜索
- `/`：打开命令面板
- `g` + `d`：进入Dashboard
- `g` + `p`：进入项目
- `g` + `a`：进入Agile Board

**Issue快捷键**：
- `e`：编辑Issue
- `a`：分配Issue
- `l`：添加标签
- `.`：快速操作
- `j`：下一个Issue
- `k`：上一个Issue

### 2. 搜索和过滤

**搜索语法**：
- `project = EMOJI`：搜索项目
- `issuetype = Story`：搜索Issue类型
- `status = In Progress`：搜索状态
- `priority = High`：搜索优先级
- `assignee = currentUser()`：搜索分配给我的Issue
- `created >= -1w`：搜索最近一周创建的Issue

**过滤示例**：
- `project = EMOJI AND issuetype = Story AND status = In Progress`：搜索进行中的Story
- `project = EMOJI AND issuetype = Bug AND priority = High`：搜索高优先级Bug
- `project = EMOJI AND assignee = currentUser() AND status != Done`：搜索我未完成的Issue

### 3. 仪表盘

**推荐仪表盘**：
- **Sprint仪表盘**：显示Sprint进度、Story完成率、Bug数量
- **版本仪表盘**：显示版本进度、功能完成率、Bug数量
- **质量仪表盘**：显示Bug趋势、代码评审通过率、测试通过率
- **效率仪表盘**：显示Story Points完成速度、Task完成时间、Bug修复时间

### 4. 通知

**推荐通知设置**：
- **Issue创建**：当创建Issue时通知
- **Issue分配**：当Issue分配给我时通知
- **Issue状态变更**：当Issue状态变更时通知
- **Issue评论**：当Issue有新评论时通知
- **Bug创建**：当创建Bug时通知

---

## 常见问题和解决方案

### 1. Issue创建问题

**问题**：Issue描述不清晰，无法准确理解需求

**解决方案**：
- 使用模板创建Issue
- 填写完整的Issue描述
- 包含验收标准和业务规则
- 添加截图或附件

### 2. Issue优先级问题

**问题**：Issue优先级设置不合理，导致重要问题被延迟

**解决方案**：
- 明确优先级定义
- 定期回顾和调整优先级
- 产品经理负责优先级决策
- 团队参与优先级讨论

### 3. Issue依赖关系问题

**问题**：Issue依赖关系不清晰，导致进度受阻

**解决方案**：
- 明确标注Issue依赖关系
- 使用Jira的依赖关系功能
- 定期检查依赖关系
- 及时解决依赖问题

### 4. Sprint规划问题

**问题**：Sprint规划不合理，导致无法按时完成

**解决方案**：
- 准确估算Story Points
- 合理分配Story Points
- 预留20%的时间处理突发问题
- 定期回顾和调整Sprint规划

### 5. Bug管理问题

**问题**：Bug数量过多，影响开发进度

**解决方案**：
- 提高代码质量
- 加强单元测试
- 加强代码评审
- 定期重构代码

---

## 总结

本文档提供了完整的Jira项目管理最佳实践，包括：

1. **项目概述**：项目信息、项目目标
2. **Jira项目配置**：项目类型、Issue类型、工作流、字段、版本、Sprint、权限
3. **Jira Issue管理最佳实践**：Epic、Story、Task、Bug、Sprint、版本管理
4. **Jira使用技巧**：快捷键、搜索和过滤、仪表盘、通知
5. **常见问题和解决方案**：Issue创建、优先级、依赖关系、Sprint规划、Bug管理

按照本文档执行，可以确保Jira项目管理规范、高效、可追踪，为项目的顺利推进提供有力保障。

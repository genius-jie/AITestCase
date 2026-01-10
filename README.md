# AITestCase - AI测试用例生成最佳实践

> 基于Trae AI助手的测试用例自动生成体系，包含完整的工作流、规则配置和实战案例

## 📋 项目简介

本项目旨在建立一套完整的AI辅助测试用例生成体系，通过Trae AI助手实现从需求分析到测试用例输出的全流程自动化，提升测试效率和质量。

### 核心特性

- 🤖 **AI驱动**：基于Trae AI助手，实现测试用例智能生成
- 📊 **6A工作流**：标准化的6阶段测试用例生成流程
- 📚 **错题本系统**：记录通用性问题，避免重复踩坑
- 🎯 **质量维度**：AI效果测试的四大维度（久、懂、暖、真）
- 🔄 **自动化工具**：Python脚本自动合并规则文件
- 📝 **OPML支持**：生成可导入XMind的测试用例脑图

## 🚀 快速开始

### 环境要求

- Python 3.11+
- VS Code
- Trae AI助手
- Git

### 安装配置

1. **克隆项目**
```bash
git clone https://github.com/genius-jie/AITestCase.git
cd AITestCase
```

2. **安装Python依赖**
```bash
# 确保已安装Python 3.11
python --version
```

3. **配置VS Code任务**
- 项目已预配置 `.vscode/tasks.json`
- 使用快捷键 `Ctrl+Shift+B` 运行"合并规则文件"任务

4. **配置Trae规则**
- 在Trae设置中指定规则文件：`.trae/rules/project_rules.md`
- 修改规则后运行合并脚本更新主规则文件

## 📁 项目结构

```
AITestCase/
├── .trae/
│   └── rules/
│       ├── project_rules.md      # 主规则文件（Trae读取）
│       ├── README.md             # 规则文件说明
│       ├── 身份定义.md           # AI助手身份定义
│       ├── 错题本规则.md         # 错题本自动调用规则
│       ├── 6A工作流.md           # 测试用例生成工作流
│       ├── 交互约定.md           # 交互规范
│       ├── OPML规范.md           # OPML文件格式规范
│       └── 错题本.md             # 错题本内容
├── .vscode/
│   └── tasks.json                # VS Code任务配置
├── AI效果质量维度体系/
│   ├── AI效果测试-久.md          # 长期记忆能力测试
│   ├── AI效果测试-懂.md          # 理解能力测试
│   ├── AI效果测试-暖.md          # 情感陪伴能力测试
│   └── AI效果测试-真.md          # 真实性能力测试
├── README.md                     # 项目说明文档
└── tmp.md                        # 临时文件
```

## 🔄 规则更新流程

### 修改规则时：

1. **编辑对应的拆分文件**
   - 身份定义 → `身份定义.md`
   - 错题本规则 → `错题本规则.md`
   - 工作流程 → `6A工作流.md`
   - 交互规范 → `交互约定.md`
   - OPML规范 → `OPML规范.md`

2. **运行合并脚本**
   ```bash
   # 方式1：使用VS Code任务（推荐）
   Ctrl+Shift+B

   # 方式2：命令行执行
   cd .trae/rules
   python ../../python/utils/merge_rules.py
   ```

3. **Trae自动读取更新**
   - Trae会自动读取更新后的 `project_rules.md`
   - 无需手动重启Trae

## 📖 6A工作流详解

### 阶段1：Align（需求分析）
从需求文档中提取清晰、可测试的功能点和验收标准

### 阶段2：Architect（测试架构设计）
设计测试策略和架构，确定测试范围和方法

### 阶段3：Atomize（测试任务拆分）
拆分模块和功能，为每个功能点设计测试

### 阶段4：Approve（测试方案审批）
确认测试方案的完整性和可行性

### 阶段5：Automate（测试用例自动生成）
自动生成全面的测试用例和checklist

### 阶段6：Assess（测试用例评估）
验收测试用例质量，确保符合要求

详细说明请参考：[6A工作流.md](.trae/rules/6A工作流.md)

## 📚 错题本系统

### 核心原则

**只记录通用性问题！** 不是所有问题都需要记录到错题本。

### 通用性问题判断标准

✅ **应该记录**：
- 可复用：类似场景下可能再次遇到
- 有规律：不是偶然的、特定的问题
- 有价值：记录后能帮助快速定位和解决
- 可推广：解决方案可以应用到其他类似场景

❌ **不应该记录**：
- 一次性问题：特定场景下只出现一次
- 偶发性问题：没有规律可循
- 特定问题：只针对某个具体文件或内容
- 简单问题：太简单，不值得记录

详细说明请参考：[错题本规则.md](.trae/rules/错题本规则.md)

## 🎯 AI效果质量维度

### 久（长期记忆）
测试AI的长期记忆能力，确保信息在数天、数周甚至数月后仍能正确存储和调用。

### 懂（理解能力）
测试AI对用户意图、上下文和隐含信息的理解能力。

### 暖（情感陪伴）
测试AI的情感识别、共情能力和个性化陪伴体验。

### 真（真实性）
测试AI回答的真实性、准确性和可靠性。

详细说明请参考：[AI效果质量维度体系/](AI效果质量维度体系/)

## 🛠️ 工具使用

### VS Code快捷任务

- **合并规则文件**：`Ctrl+Shift+B`
  - 自动合并所有拆分的规则文件到 `project_rules.md`
  - 输出详细的合并日志

### Python合并脚本

```bash
cd .trae/rules
python ../../python/utils/merge_rules.py
```

功能：
- 按照指定顺序合并规则文件
- 输出详细的合并过程
- 自动处理文件不存在的情况
- UTF-8编码支持

## 📝 OPML文件规范

生成的测试用例脑图遵循OPML格式规范，可直接导入XMind等思维导图工具。

### 核心要求

- 特殊字符正确转义（`<` → `&lt;`，`>` → `&gt;`）
- XML格式规范
- 层级结构清晰
- 符合XMind导入标准

详细说明请参考：[OPML规范.md](.trae/rules/OPML规范.md)

## 🤝 贡献指南

欢迎提交Issue和Pull Request！

1. Fork本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启Pull Request

## 📄 许可证

本项目采用MIT许可证 - 详见LICENSE文件

## 👨‍💻 作者

genius-jie

## 🙏 致谢

感谢Trae AI助手提供的强大支持

---

**最后更新时间**：2026-01-05

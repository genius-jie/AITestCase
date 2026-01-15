# Agent规则与工作流组织规划

## 一、现状分析 
当前所有规则和配置都集中在单一的`project_rules.md`文件中，包含了多种不同类型的内容： - 身份定义 - 提示词性能优化规则 - 错题本自动调用规则 - 6A工作流生成测试用例 - 交互约定 - XMind导入文档层级规范 - 文件修改规则 - 等等 同时，还有一些单独的Agent提示词文件： - DDT测试数据管理智能体提示词.md - JMeter脚本编写智能体提示词.md - 提示词编写智能体提示词.md - 日报整理智能体提示词.md

## 一、项目目标

1. 为多 Agent、多业务、多阶段（Design / Execution）建立统一的规则与文档结构。
2. 明确不同层级的 workflow 的语义与使用场景。
3. 保证 agent 在 Design Mode 和 Execution Mode 下行为正确，避免冲突。
4. 支持从原始需求快速生成 agent 三件套（role.prompt.md / workflow\.md / mistakes.md）。

***

## 二、目录结构（保持原有结构）

```
.trae/
├── rules/
	├── project_rules/                     # 执行态宪法（merge）
	│   ├── identity.md
	│   ├── interaction.md
	│   ├── markdown.md
	│   ├── file_management.md
	│   └── core_constraints.md
	│
	├── project_design/                    # 设计态框架（可 merge，但降权）
	│   ├── workflow_design.md             # 如何设计 业务agent的workflow
	│   ├── agent_design.md                # 如何设计 agent（role / input / output）
	│   ├── prompt_design.md               # prompt 架构方法
	│   └── examples/
	│       └── daily_report_example.md
	│
	├── agents/                            # 业务 agent 三件套	
	│   └── ddt/
	│   │    ├── role.prompt.md             # ← 由 design agent 生成
	│   │    ├── workflow.md                # ← 由 design workflow 生成
	│   │    └── mistakes.md
	│   └── jmeter/
	│   │    ├── role.prompt.md             # ← 由 design agent 生成
	│   │    ├── workflow.md                # ← 由 design workflow 生成
	│   │    └── mistakes.md
	│   └── prompt_architect/
	│   │    ├── role.prompt.md             # ← 由 design agent 生成
	│   │    ├── workflow.md                # ← 由 design workflow 生成
	│   │    └── mistakes.md
	│   └── daily_report/
	│       ├── role.prompt.md             # ← 由 design agent 生成
	│       ├── workflow.md                # ← 由 design workflow 生成
	│       └── mistakes.md
	│
	├── workflows/                         # 执行态模板（不 merge）
	│   └── 6a_testcase.md                 # 结构型 workflow（参考设计）
	│
	├── merge_rules.py
	└──	project_rules.md 执行态宪法（merge后的项目规则）
	└── README.md
	
```

***

## 三、核心设计原则

1️⃣ Workflow 三类语义

### | 类型 | 文件位置 | 用途 | 执行性 | 阶段 |

\| ------------------- | -------------------- | --------------------------- | ------- | ------------------ |

\| \*\*Structural\*\*（结构型） | workflows/ | 认知结构参考，辅助设计 agent 三件套 | ❌ 不可执行 | Design Mode |

\| \*\*Project\*\*（项目级） | project\_design/ | 用于生成新 Agent / workflow / 文档 | ⚠️ 条件执行 | Design / Bootstrap |

\| \*\*Business\*\*（业务级） | agents/\*/workflow\.md | 实际执行流程 | ✅ 可执行 | Execution Mode |

***

### 2️⃣ 语义标签（必须在 workflow 文件顶部声明）

```
@workflow_type: structural | project | business
@usage_mode: design | generation | execution
@enforcement: reference_only | generate_only | executable

```

**示例**（workflows/6a\_testcase.md）：

```
@workflow_type: structural
@usage_mode: design
@enforcement: reference_only

This workflow is a cognitive structure reference.
It MUST NOT be executed step-by-step.
It MUST NOT be copied directly into agent workflow outputs.

```

***

### 3️⃣ Agent role.prompt.md 强制声明（防止执行冲突）

```
## Workflow Usage Declaration

You must distinguish workflows by semantic type:

- Structural workflows:
  - Purpose: cognitive reference only
  - Must NOT be executed step-by-step
  - Must NOT be mapped directly to agent workflow outputs

- Project workflows:
  - Purpose: document generation and agent setup
  - Executed only during Design / Bootstrap phases

- Business workflows:
  - Purpose: actual task execution
  - Executed only in Execution Mode

If a workflow is structural, never mirror its steps as output.

```

***

### 4️⃣ 核心使用规则

1. **Design Mode**（设计态）
   * 目标：从原始需求生成 agent 三件套
   * 使用：
     * project\_rules/ → 边界约束
     * project\_design/ → 指导设计
     * workflows/6a\_testcase.md → 结构参考
     * 原始需求文档 → 输入对象
   * 输出：
     * role.prompt.md / workflow\.md / mistakes.md
2. **Execution Mode**（执行态）
   * 目标：真正执行业务流程
   * 使用：
     * agents/\*/workflow\.md → 执行
     * project\_rules/ → 行为边界
   * 不使用 workflows/6a\_testcase.md（结构参考）
3. **Merge Rules**
   * merge\_rules.py 仅 merge project\_rules/ 和 project\_design/（可选）
   * workflows/ 下的文件不 merge，保持参考独立性

***

### 5️⃣ Phase 化执行策略

\| Phase | 目标 | 输出 |

\| ------- | ---------------- | ----------------------------------------------- |

\| Phase 0 | 核心规则落地 | project\_rules/\*、workflows/6a\_testcase.md（结构参考） |

\| Phase 1 | 项目级能力（生成新 agent） | project\_design/\*、project workflow 示例 |

\| Phase 2 | 业务 agent 三件套生成 | agents/\*/role.prompt.md、workflow\.md、mistakes.md |

\| Phase 3 | 回看 & 固化规则 | 补充 agent\_conventions.md、workflow 使用规范 |

***

## 四、Trae-solo 执行说明（可直接执行）

1. **初始上下文传入**

```
[CORE project_rules]
[project_design/*]
[workflows/6a_testcase.md]
[raw_requirements/*.md]

```

1. **设计模式**

* Trae-solo 应处于 **Design Mode**
* 参考 6A 的结构模板生成 agent 三件套
* merge project\_rules 与 project\_design（可降权），不 merge workflows

1. **输出物**

* agents/目标\_agent/role.prompt.md
* agents/目标\_agent/workflow\.md
* agents/目标\_agent/mistakes.md

1. **安全约束**

* Structural workflow 仅作认知参考
* 禁止将 Structural workflow 逐条映射到 workflow\.md
* 禁止在 Design Mode 执行业务流程

***

请分步骤，按照 **Phase 0 → Phase 1 → Phase 2** 执行，逐步生成项目规则与 agent 三件套。

***


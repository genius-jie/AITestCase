@workflow_type: reusable
@usage_mode: execution
@enforcement: optional
@phase_id: A2
@version: 1.0.0
@author: QA Team
@created_at: 2026-01-14
@last_updated: 2026-01-14

Architect｜流程架构与标准制定
@phase_id: A2
@role: 流程设计Agent
@human_review: optional
@upstream_phases: [A1]

@goal:
- 将需求规则转化为可协同执行的测试流程与产物标准

@inputs:
- A1 输出文档：结构化需求清单
- A1 输出文档：需求澄清与验收标准
- A1 输出文档：测试维度规划（正常/异常/边界/鲁棒性）
- A1 输出文档：核心字段与非核心字段识别
- 语音生成数据契约文档.md - 数据规范和字段定义
- VAD测试数据设计与样本生成指南.md - 测试设计指南
- 数据契约模板
- 测试报告模板

@outputs:
- 测试架构设计文档（包含6阶段测试流程）
- Agent 协同调度手册（A1-A6阶段协同机制）
- 数据流设计（CSV数据→SSML生成→音频合成→VAD检测）
- 执行流设计（测试数据准备→语音生成→VAD测试→结果分析）
- 结果流设计（测试结果收集→失败分析→优化迭代）
- 中间产物契约定义

@validation_rules:
- 必须校验 A1 阶段已完成（三件套+结果文档）
- 必须校验 A1 输出的结构化需求清单已通过人工审核
- 必须校验 A1 输出的需求澄清与验收标准无未解决问题

@execution_steps:
1. 分析A1输出的需求摘要
2. 依据A1输出设计数据结构：
   - 输入字段 / 预期字段 / 音频元数据
3. 定义测试字段及取值规则
4. 制定测试优先级和场景覆盖策略
5. 规划样本生成流程与音频后处理方案
6. 确定技术栈：
   - TTS引擎（Azure TTS）
   - SSML结构与标签
   - 后期处理模块（呼吸音、背景噪声）
   - CSV数据管理
7. 分析项目目录结构及模块：
   - generate_vad_samples.py
   - add_breath_sound.py
   - azure_config.py
   - 音频输出目录
8. 绘制模块依赖图（可文本描述）
9. 标注数据流：
   - CSV -> SSML -> TTS -> 后期处理 -> 音频输出
10. 输出架构文档，用于 A3 聚合资产

@skeleton:
  sections:
    - 测试总体架构
    - 阶段划分与依赖关系
    - 中间产物契约定义
    - Agent 协作与触发规则

---
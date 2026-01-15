@workflow_type: reusable
@usage_mode: execution
@enforcement: optional
@phase_id: A5
@version: 1.0.0
@author: QA Team
@created_at: 2026-01-14
@last_updated: 2026-01-14

Apply｜测试执行与问题调试
@phase_id: A5
@role: 执行调度Agent
@human_review: optional
@upstream_phases: [A4]

@goal:
- 自动化执行测试并定位问题根因

@inputs:
- A4 输出文档：测试数据集（CSV格式，包含正常/异常/边界/鲁棒性场景）
  - vad_test_data_comprehensive.csv - 综合测试数据（25个场景）
  - vad_test_data_sc025.csv - 特定场景测试数据
  - vad_test_data_sc003.csv - 特定场景测试数据
  - vad_test_data_noise_comparison.csv - 噪音对比测试数据
- A4 输出文档：工具参数化与适配说明
  - Azure TTS配置说明（azure_config.py）
  - SSML生成脚本参数说明（generate_ssml.py）
  - 呼吸音效添加脚本参数说明（add_breath_sound.py）
  - VAD样本生成脚本参数说明（generate_vad_samples.py）
- A4 输出文档：脚本与数据映射关系文档
- A4 输出文档：测试数据质量验证报告
- 语音生成数据契约文档.md - 数据规范和字段定义
- VAD测试数据设计与样本生成指南.md - 测试设计指南
- 测试脚本

@outputs:
- 测试执行日志（包含100个WAV音频样本生成记录）
- VAD测试结果统计（通过率、失败率、失败分布）
- 问题根因分析报告（失败类型、原因分析、解决方案）
- 测试执行总结文档
- 对话总结.md - 测试执行记录和问题分析
- 批量修改完成总结.md - 批量修改总结

@validation_rules:
- 必须校验 A4 阶段已完成（三件套+结果文档）
- 必须校验 A4 输出的测试数据集格式正确且完整
- 必须校验 A4 输出的工具参数化与适配说明符合要求
- 必须校验测试脚本与测试数据集的兼容性

@execution_steps:
1. 读取A4生成的CSV文件
2. 解析场景数据
3. 生成SSML文本
4. 调用Azure TTS API生成音频
5. 执行音频后期处理（呼吸音、噪声、格式转换）
6. 保存音频文件，更新生成日志
7. 加载VAD测试算法
8. 导入A4生成的音频样本
9. 执行VAD检测
10. 收集检测结果并与A2预期结果对比
11. 输出测试报告：
    - 通过率、失败率
    - 异常样本记录
12. 标记未覆盖或失败场景供A6优化
13. 输出统计报告（总场景数、成功/失败数量）

@skeleton:
  sections:
    - 执行环境说明
    - 执行结果汇总
    - 异常与问题定位
    - 根因分析结论

---
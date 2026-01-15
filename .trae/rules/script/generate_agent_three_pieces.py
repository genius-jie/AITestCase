#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
工业级 Agent 三件套生成脚本（最终形态）

职责边界：
- 仅负责“结构展开”
- 不包含任何业务语义或实现逻辑
- 所有阶段含义、结构、约束，完全来源于 workflow.md

使用方法：
python generate_agent_three_pieces.py --agent-name tts --task-name "语音生成自动化测试" \
    --workflow-path "E:\AI测试用例\.trae\rules\workflows\6a_test_flow.md" \
    --output-dir "E:\AI测试用例\.trae\rules\agents\tts" \
    --input-docs "语音生成需求文档.md" "语音生成设计文档.md" "语音生成接口文档.md"

或者使用默认参数：
python generate_agent_three_pieces.py --agent-name tts --task-name "语音生成自动化测试"
"""

import os
import re
import datetime
import argparse

# ------------------- 命令行参数解析 -------------------
def parse_args():
    parser = argparse.ArgumentParser(description='工业级 Agent 三件套生成脚本')
    
    parser.add_argument('--agent-name', required=True, help='Agent 名称')
    parser.add_argument('--task-name', required=True, help='任务名称')
    parser.add_argument('--workflow-path', 
                      default=r"E:\AI测试用例\.trae\rules\workflows\6a_test_flow.md",
                      help='Workflow 文件路径')
    parser.add_argument('--output-dir', 
                      default=None,
                      help='输出目录，默认会自动生成')
    parser.add_argument('--input-docs', 
                      nargs='+', 
                      default=["原始需求文档.md", "设计文档.md", "接口文档.md"],
                      help='输入文档列表')
    parser.add_argument('--author', 
                      default="QA Team",
                      help='作者')
    parser.add_argument('--version', 
                      default="1.0.0",
                      help='版本号')
    
    args = parser.parse_args()
    
    # 如果没有指定输出目录，自动生成
    if not args.output_dir:
        args.output_dir = rf"E:\AI测试用例\.trae\rules\agents\{args.agent_name}"
    
    return args

# ------------------- 配置区 -------------------
args = parse_args()

AGENT_NAME = args.agent_name
TASK_NAME = args.task_name
WORKFLOW_PATH = args.workflow_path
OUTPUT_DIR = args.output_dir
INPUT_DOCS = args.input_docs
AUTHOR = args.author
VERSION = args.version
TODAY = datetime.date.today().isoformat()

# ------------------- 工具函数 -------------------
def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"[生成] {path}")

def meta_block(meta: dict):
    return "\n".join([f"@{k}: {v}" for k, v in meta.items()]) + "\n\n"

# ------------------- Workflow 解析 -------------------
def parse_workflow(workflow_path):
    """
    解析 workflow.md：
    - phase_id
    - phase_name
    - skeleton.sections
    """
    with open(workflow_path, "r", encoding="utf-8") as f:
        content = f.read()

    phase_pattern = re.compile(
        r"## 阶段\s+(A\d+)：(.+?)\n(.*?)@skeleton:\s+sections:\n((?:\s+- .+\n)+)",
        re.S
    )

    phases = []
    for m in phase_pattern.finditer(content):
        phase_id = m.group(1)
        phase_name = m.group(2).strip()
        sections = [
            s.strip("- ").strip()
            for s in m.group(4).strip().splitlines()
        ]
        phases.append((phase_id, phase_name, sections))

    return phases

# ------------------- role.prompt.md -------------------
def generate_role(phases):
    meta = {
        "agent_type": AGENT_NAME,
        "version": VERSION,
        "author": AUTHOR,
        "workflow": os.path.basename(WORKFLOW_PATH),
        "created_at": TODAY,
        "last_updated": TODAY
    }

    phase_order = "\n".join(
        [f"- {pid}: {name}" for pid, name, _ in phases]
    )
    doc_list = "\n".join([f"- {d}" for d in INPUT_DOCS])

    content = meta_block(meta) + f"""
# {AGENT_NAME.upper()} Agent Role

## 角色定位
你是【{AGENT_NAME.upper()} Agent】，严格按照 workflow 定义执行任务。

## 阶段执行顺序
{phase_order}

## 输入文档
{doc_list}

## 执行约束
- 不得跳过阶段
- 不得修改 skeleton 结构
- 仅在 skeleton 区块内生成内容

## 输出
- 阶段文档（A1 ~ A6）
- 业务相关资产
"""
    return content

# ------------------- workflow.md（引用） -------------------
def generate_workflow_reference():
    meta = {
        "workflow_ref": os.path.basename(WORKFLOW_PATH),
        "usage": "execution",
        "created_at": TODAY
    }
    return meta_block(meta) + f"""
# Workflow Reference

本 Agent 执行所依据的唯一 Workflow：

- {WORKFLOW_PATH}
"""

# ------------------- mistakes.md -------------------
def generate_mistakes():
    meta = {
        "agent_type": AGENT_NAME,
        "version": VERSION,
        "created_at": TODAY
    }
    return meta_block(meta) + f"""
# {AGENT_NAME.upper()} Agent Mistakes Notebook

## 使用说明
- 记录 Agent 在执行 workflow 阶段中出现的偏差
- 每条错误必须注明影响阶段
"""

# ------------------- Skeleton 生成 -------------------
def generate_skeletons(phases):
    # 只生成A1阶段的skeleton，其他阶段由bootstrap_phase_three_pieces.py生成
    for pid, name, sections in phases:
        if pid == "A1":  # 只生成A1阶段的skeleton
            meta = {
                "phase_id": pid,
                "phase_name": name,
                "task": TASK_NAME,
                "created_at": TODAY
            }

            section_blocks = "\n\n".join(
                [f"## {s}\n\n（由 Agent 自动生成）" for s in sections]
            )

            content = meta_block(meta) + f"""
# 阶段 {pid}：{name}

## 输入文档
{chr(10).join([f"- {d}" for d in INPUT_DOCS])}

{section_blocks}
"""
            filename = f"{pid}_{name}_{TASK_NAME}.md"
            write_file(os.path.join(OUTPUT_DIR, filename), content)

# ------------------- 主执行 -------------------
phases = parse_workflow(WORKFLOW_PATH)

write_file(
    os.path.join(OUTPUT_DIR, "role.prompt.md"),
    generate_role(phases)
)

write_file(
    os.path.join(OUTPUT_DIR, "workflow.md"),
    generate_workflow_reference()
)

write_file(
    os.path.join(OUTPUT_DIR, "mistakes.md"),
    generate_mistakes()
)

# 可选：生成A1阶段的skeleton，其他阶段由bootstrap_phase_three_pieces.py生成
# generate_skeletons(phases)

print("\n✅ 最终形态 Agent 三件套 + Skeleton 生成完成")

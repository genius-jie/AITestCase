#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# 工业级阶段三件套自举生成脚本

## 功能说明
该脚本用于从现有 workflow.md 文件自动生成每个阶段的三件套文档（role.prompt.md、workflow.md、mistakes.md）。

## 使用方式

### 基本使用
python bootstrap_phase_three_pieces.py --workflow-md "E:\AI测试用例\.trae\rules\agents\tts\workflow.md" \
    --output-dir "E:\AI测试用例\.trae\rules\agents\tts\stages"

### 简化使用（自动生成路径）
python bootstrap_phase_three_pieces.py --agent-name tts

### 使用默认参数
python bootstrap_phase_three_pieces.py --workflow-md "E:\AI测试用例\.trae\rules\agents\tts\workflow.md"

## 输出结果
在 OUTPUT_DIR 目录下为每个阶段生成独立的三件套文档：
- stages/{PHASE_ID}/role.prompt.md：阶段角色定义
- stages/{PHASE_ID}/workflow.md：阶段执行工作流
- stages/{PHASE_ID}/mistakes.md：阶段典型错误和改进措施

## 特点
- 自举生成：从现有 workflow.md 自动解析生成
- 多阶段支持：同时处理 workflow 中的所有阶段
- 完整的 metadata：每个生成的文件都包含 metadata
- 可迭代更新：workflow.md 更新后可重新运行刷新
- 结构化输出：按阶段 ID 组织目录结构
- 自动解析：自动提取阶段的 phase_id、role、output、human_review 等信息
- 继承机制：从根目录三件套中继承默认值，再由阶段级三件套覆盖
"""

import os
import datetime
import re
import argparse

# ---------- 命令行参数解析 ----------
def parse_args():
    parser = argparse.ArgumentParser(description='工业级阶段三件套自举生成脚本')
    
    parser.add_argument('--workflow-md', 
                      help='Workflow 文件路径')
    parser.add_argument('--output-dir', 
                      help='输出目录')
    parser.add_argument('--agent-name', 
                      help='Agent 名称，用于自动生成路径')
    parser.add_argument('--version', 
                      default="1.0.0",
                      help='版本号')
    parser.add_argument('--author', 
                      default="QA Team",
                      help='作者')
    
    args = parser.parse_args()
    
    # 自动生成路径逻辑
    base_dir = r"E:\AI测试用例\.trae\rules"
    
    if args.agent_name:
        if not args.workflow_md:
            args.workflow_md = os.path.join(base_dir, f"agents/{args.agent_name}/workflow.md")
        if not args.output_dir:
            args.output_dir = os.path.join(base_dir, f"agents/{args.agent_name}/stages")
    
    return args

# ---------- 配置 ----------
args = parse_args()

BASE_DIR = r"E:\AI测试用例\.trae\rules"
WORKFLOW_MD = args.workflow_md
OUTPUT_DIR = args.output_dir
VERSION = args.version
AUTHOR = args.author
CREATED_AT = datetime.date.today().isoformat()

# 验证必要参数
if not WORKFLOW_MD:
    raise ValueError("必须提供 workflow-md 参数或 agent-name 参数")
if not OUTPUT_DIR:
    raise ValueError("必须提供 output-dir 参数或 agent-name 参数")

# ---------- 工具函数 ----------
def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"[生成] {path}")

def extract_phases(workflow_path):
    """解析 workflow.md，将每个阶段作为 dict 返回"""
    with open(workflow_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # 检查是否有 workflow_ref 引用
    workflow_ref_match = re.search(r"@workflow_ref:\s*(\S+)", content)
    if workflow_ref_match:
        ref_workflow_name = workflow_ref_match.group(1)
        ref_workflow_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(workflow_path))), "workflows", ref_workflow_name)
        with open(ref_workflow_path, "r", encoding="utf-8") as f:
            content = f.read()

    # 使用正则匹配阶段
    phase_blocks = re.split(r"## 阶段 \w+：", content)
    phases = []
    for block in phase_blocks[1:]:  # 第一个块是标题前内容
        lines = block.strip().splitlines()
        title_line = lines[0]  # 阶段标题
        phase_id_match = re.search(r"@phase_id:\s*(\S+)", block)
        role_match = re.search(r"@role:\s*(.+)", block)
        output_match = re.search(r"@outputs:\s*\[([^\]]+)\]", block)
        human_review_match = re.search(r"@human_review:\s*(\S+)", block)

        phases.append({
            "title": title_line.strip(),
            "phase_id": phase_id_match.group(1) if phase_id_match else "",
            "role": role_match.group(1) if role_match else "Unknown",
            "output": f"[{output_match.group(1)}]" if output_match else "[]",
            "human_review": human_review_match.group(1) if human_review_match else "optional",
            "content": block.strip()
        })
    return phases

def generate_stage_files(phase):
    """生成单阶段三件套"""
    # 从输出目录中提取agent_name
    agent_name = os.path.basename(os.path.dirname(OUTPUT_DIR))
    
    stage_dir = os.path.join(OUTPUT_DIR, phase["phase_id"])
    # role.prompt.md
    agent_name = os.path.basename(os.path.dirname(OUTPUT_DIR))
    role_meta = {
        "agent_type": agent_name,
        "version": VERSION,
        "author": AUTHOR,
        "description": f"{phase['title']} 阶段角色说明",
        "created_at": CREATED_AT,
        "last_updated": CREATED_AT
    }
    role_content = "\n".join([f"@{k}: {v}" for k, v in role_meta.items()]) + "\n\n"
    role_content += f"# {phase['role']} Agent\n\n## 核心职责\n- 执行阶段任务\n- 输出产物: {phase['output']}\n"
    write_file(os.path.join(stage_dir, "role.prompt.md"), role_content)

    # workflow.md
    workflow_meta = {
        "workflow_type": "reusable",
        "usage_mode": "execution",
        "enforcement": "optional",
        "phase_id": phase["phase_id"],
        "version": VERSION,
        "author": AUTHOR,
        "created_at": CREATED_AT,
        "last_updated": CREATED_AT
    }
    workflow_content = "\n".join([f"@{k}: {v}" for k, v in workflow_meta.items()]) + "\n\n"
    workflow_content += phase["content"]
    write_file(os.path.join(stage_dir, "workflow.md"), workflow_content)

    # mistakes.md
    mistakes_meta = {
        "agent_type": agent_name,
        "version": VERSION,
        "description": f"{phase['title']} 阶段典型错误与改进",
        "created_at": CREATED_AT,
        "last_updated": CREATED_AT
    }
    mistakes_content = "\n".join([f"@{k}: {v}" for k, v in mistakes_meta.items()]) + "\n\n"
    mistakes_content += f"# {phase['role']} Agent Mistakes Notebook\n\n- 待填充典型错误与修正措施\n"
    write_file(os.path.join(stage_dir, "mistakes.md"), mistakes_content)

# ---------- 执行 ----------
phases = extract_phases(WORKFLOW_MD)
for phase in phases:
    generate_stage_files(phase)

print("\n✅ 所有阶段三件套生成完成！")

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
规则合并脚本

功能：
1. 合并project_rules目录下的所有规则文件
2. 生成合并后的执行态宪法
3. 支持按指定顺序合并
4. 保留文件的完整内容
"""

import os
import glob

# 规则文件目录
RULES_DIR = r"E:\AI测试用例\.trae\rules\project_rules"
# 输出文件路径
OUTPUT_FILE = r"E:\AI测试用例\.trae\rules\project_rules.md"

# 核心规则（执行态宪法） - 必须merge
CORE_RULES = [
    "core_constraints.md",  # 系统级硬约束
    "file_management.md",   # 工程规范
    "performance.md",       # 工程规范
    "agent_conventions.md"   # 工程规范
]

# 设计规则（设计态框架） - 可选merge
DESIGN_RULES = [
    "../project_design/workflow_design.md",
    "../project_design/agent_design.md",
    "../project_design/prompt_design.md"
]

# 默认使用CORE_RULES作为合并顺序
MERGE_ORDER = CORE_RULES


def merge_rules(merge_mode="core"):
    """合并规则文件
    
    参数:
        merge_mode: 合并模式
            - "core": 只合并核心规则（执行态宪法）
            - "design": 合并核心规则+设计规则
    """
    print(f"开始合并规则文件...")
    print(f"合并模式: {merge_mode}")
    print(f"规则文件目录: {RULES_DIR}")
    print(f"输出文件: {OUTPUT_FILE}")
    
    # 创建输出内容列表
    output_content = []
    
    # 添加标题
    output_content.append("# 执行态宪法\n")
    output_content.append("\n**合并规则文件生成，请勿直接修改**\n")
    output_content.append("\n---\n\n")
    
    # 合并核心规则
    print("\n=== 合并核心规则 ===")
    for filename in CORE_RULES:
        file_path = os.path.join(RULES_DIR, filename)
        if os.path.exists(file_path):
            print(f"合并文件: {filename}")
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
                output_content.append(content)
                output_content.append("\n---\n\n")
        else:
            print(f"警告: 文件不存在: {filename}")
    
    # 如果是design模式，合并设计规则
    if merge_mode == "design":
        print("\n=== 合并设计规则 ===")
        for filename in DESIGN_RULES:
            # 处理相对路径
            if filename.startswith("../"):
                file_path = os.path.join(RULES_DIR, filename)
            else:
                file_path = os.path.join(RULES_DIR, filename)
            
            if os.path.exists(file_path):
                print(f"合并文件: {filename}")
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                    output_content.append(content)
                    output_content.append("\n---\n\n")
            else:
                print(f"警告: 文件不存在: {filename}")
    
    # 移除最后一个分隔符
    if output_content and output_content[-1] == "\n---\n\n":
        output_content.pop()
    
    # 写入输出文件
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("".join(output_content))
    
    print(f"\n规则文件合并完成！")
    print(f"输出文件: {OUTPUT_FILE}")


if __name__ == "__main__":
    import sys
    
    # 解析命令行参数
    merge_mode = "core"
    if len(sys.argv) > 1:
        merge_mode = sys.argv[1].lower()
    
    # 验证合并模式
    if merge_mode not in ["core", "design"]:
        print(f"错误: 无效的合并模式 '{merge_mode}'")
        print(f"可用模式: core, design")
        sys.exit(1)
    
    merge_rules(merge_mode)

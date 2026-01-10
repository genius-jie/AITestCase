#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
通用测试用例合并工具

功能：
- 自动发现指定目录下的测试用例文件
- 支持自定义文件匹配模式
- 支持自定义输出文件名
- 保留原始文件结构和内容
- 生成标准Markdown格式，可直接导入XMind
- 支持在模块层级添加测试要点、范围、目标、测试难度和测试时间

使用方法：
python merge_test_cases.py [options]

选项：
-h, --help            显示帮助信息
-i INPUT_DIR, --input INPUT_DIR
                      输入目录，默认：当前目录
-o OUTPUT_FILE, --output OUTPUT_FILE
                      输出文件名，默认：merged_test_cases.md
-p PATTERN, --pattern PATTERN
                      文件匹配模式，默认：6_最终测试用例_*.md
-t TITLE, --title TITLE
                      合并文件标题，默认：测试用例集合
-c CONFIG_FILE, --config CONFIG_FILE
                      模块配置文件路径，默认：module_config.json
"""

import os
import re
import json
import argparse
from datetime import datetime

def parse_arguments():
    """
    解析命令行参数
    """
    parser = argparse.ArgumentParser(description='通用测试用例合并工具')
    parser.add_argument('-i', '--input', dest='input_dir', default='.', 
                      help='输入目录，默认：当前目录')
    parser.add_argument('-o', '--output', dest='output_file', 
                      default='merged_test_cases.md',
                      help='输出文件名，默认：merged_test_cases.md')
    parser.add_argument('-p', '--pattern', dest='pattern', 
                      default='6_最终测试用例_*.md',
                      help='文件匹配模式，默认：6_最终测试用例_*.md')
    parser.add_argument('-t', '--title', dest='title', 
                      default='测试用例集合',
                      help='合并文件标题，默认：测试用例集合')
    parser.add_argument('-c', '--config', dest='config_file', 
                      default='module_config.json',
                      help='模块配置文件路径，默认：module_config.json')
    
    return parser.parse_args()

def load_module_config(config_file):
    """
    加载模块配置文件
    :param config_file: 配置文件路径
    :return: 模块配置字典
    """
    if not os.path.exists(config_file):
        print(f"警告：配置文件不存在：{config_file}")
        return {}
    
    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            config = json.load(f)
        print(f"成功加载配置文件：{config_file}")
        return config
    except json.JSONDecodeError as e:
        print(f"错误：配置文件格式无效：{e}")
        return {}
    except Exception as e:
        print(f"错误：加载配置文件失败：{e}")
        return {}

def get_matching_files(directory, pattern):
    """
    获取匹配模式的文件列表
    :param directory: 目录路径
    :param pattern: 文件匹配模式（支持通配符）
    :return: 匹配的文件列表
    """
    matching_files = []
    
    # 转换通配符为正则表达式
    regex_pattern = pattern.replace('.', '\.').replace('*', '.*')
    regex = re.compile(f'^{regex_pattern}$')
    
    # 遍历目录获取匹配文件
    for file_name in os.listdir(directory):
        if regex.match(file_name):
            matching_files.append(file_name)
    
    # 按文件名排序
    matching_files.sort()
    
    return matching_files

def merge_test_cases(input_dir, output_file, pattern, title):
    """
    合并测试用例文件
    :param input_dir: 输入目录
    :param output_file: 输出文件路径
    :param pattern: 文件匹配模式
    :param title: 合并文件标题
    """
    print("开始合并测试用例...")
    print(f"输入目录：{input_dir}")
    print(f"文件模式：{pattern}")
    print(f"输出文件：{output_file}")
    
    # 获取匹配的文件列表
    matching_files = get_matching_files(input_dir, pattern)
    
    if not matching_files:
        print(f"未找到匹配的文件：{pattern}")
        return False
    
    print(f"找到 {len(matching_files)} 个匹配文件：")
    for file in matching_files:
        print(f"  - {file}")
    
    # 生成标题和日期
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    merged_content = f"# {title}\n\n生成日期：{now}\n\n"
    
    # 合并每个文件的内容
    for file_name in matching_files:
        file_path = os.path.join(input_dir, file_name)
        
        print(f"处理文件：{file_name}")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 跳过原文件的标题，只保留内容（从第一个二级标题开始）
        content_lines = content.split('\n')
        start_idx = 0
        for i, line in enumerate(content_lines):
            if line.startswith('## '):
                start_idx = i
                break
        
        # 提取内容
        file_content = '\n'.join(content_lines[start_idx:])
        
        # 添加文件分隔线和内容
        merged_content += f"\n---\n\n# {file_name.replace('.md', '')}\n\n{file_content}\n"
    
    # 写入合并后的文件
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(merged_content)
    
    # 输出合并结果
    file_size = os.path.getsize(output_file)
    print(f"\n测试用例合并完成！")
    print(f"输出文件：{output_file}")
    print(f"文件大小：{file_size:,} 字节")
    print(f"包含 {len(matching_files)} 个测试用例文件")
    print(f"\n使用建议：")
    print(f"1. 直接将该Markdown文件导入XMind")
    print(f"2. XMind会自动识别Markdown层级结构")
    print(f"3. 导入后可根据需要调整思维导图样式")
    
    return True

def main():
    """
    主函数
    """
    # 解析命令行参数
    args = parse_arguments()
    
    # 确保输入目录存在
    if not os.path.isdir(args.input_dir):
        print(f"错误：输入目录不存在：{args.input_dir}")
        return False
    
    # 合并测试用例
    return merge_test_cases(
        input_dir=args.input_dir,
        output_file=args.output_file,
        pattern=args.pattern,
        title=args.title
    )

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)

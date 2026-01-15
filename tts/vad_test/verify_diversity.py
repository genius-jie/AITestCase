#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
话术多样性验证脚本
验证CSV文件中的话术是否完全不同
"""

import csv
from collections import Counter
from pathlib import Path


def verify_text_diversity(csv_file_path: str):
    """验证话术多样性"""
    csv_file = Path(csv_file_path)
    
    if not csv_file.exists():
        print(f"错误：文件不存在: {csv_file_path}")
        return
    
    texts = []
    
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            text = row.get('text', '')
            if text:
                text = text.strip()
                if text:
                    texts.append(text)
    
    if not texts:
        print("错误：CSV文件中没有找到text字段或text字段为空")
        return
    
    # 统计话术
    text_counter = Counter(texts)
    unique_texts = len(text_counter)
    total_texts = len(texts)
    repeated_texts = sum(1 for count in text_counter.values() if count > 1)
    
    print('=' * 80)
    print('话术多样性验证结果')
    print('=' * 80)
    print(f'总话术数: {total_texts}')
    print(f'唯一话术数: {unique_texts}')
    print(f'重复话术数: {repeated_texts}')
    print(f'唯一话术比例: {(unique_texts / total_texts * 100):.2f}%')
    
    if repeated_texts > 0:
        print('\n重复话术详情:')
        for text, count in text_counter.most_common():
            if count > 1:
                print(f'  {text}: 重复 {count} 次')
    else:
        print('\n✅ 没有重复话术！')
    
    print('=' * 80)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='验证CSV文件中的话术多样性')
    parser.add_argument('--test-data', type=str, default='vad_test_data_noise_comparison.csv', help='测试数据CSV文件路径')
    args = parser.parse_args()
    verify_text_diversity(args.test_data)

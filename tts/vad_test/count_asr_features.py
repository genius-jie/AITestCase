#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
统计测试数据中ASR特性的覆盖率
"""

import csv
import re
from pathlib import Path

def count_asr_features(csv_file_path: str):
    """统计测试数据中ASR特性的覆盖率"""
    csv_file = Path(csv_file_path)
    
    if not csv_file.exists():
        print(f"错误：文件不存在: {csv_file_path}")
        return
    
    # 定义ASR特性
    mood_words = ['哎', '喂', '嗯', '唉', '哦', '啊', '呀', '哇', '哈', '嘿', '嘿']
    emotion_markers = ['！', '？', '...']
    pause_markers = ['...']
    colloquial_words = ['超', '啦', '呢', '吧', '哟', '嘞', '哒', '的说']
    
    total_count = 0
    mood_word_count = 0
    emotion_count = 0
    pause_count = 0
    colloquial_count = 0
    asr_feature_count = 0
    
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            text = row.get('text', '')
            if text is None:
                text = ''
            text = text.strip()
            if not text:
                continue
            
            total_count += 1
            
            # 检查是否包含ASR特性
            has_mood_word = any(word in text for word in mood_words)
            has_emotion = any(marker in text for marker in emotion_markers)
            has_pause = any(marker in text for marker in pause_markers)
            has_colloquial = any(word in text for word in colloquial_words)
            
            # 统计各特性
            if has_mood_word:
                mood_word_count += 1
            if has_emotion:
                emotion_count += 1
            if has_pause:
                pause_count += 1
            if has_colloquial:
                colloquial_count += 1
            
            # 只要包含其中一种特性，就算作ASR特性数据
            if has_mood_word or has_emotion or has_pause or has_colloquial:
                asr_feature_count += 1
    
    print('=' * 80)
    print('ASR特性覆盖率统计结果')
    print('=' * 80)
    print(f'总测试数据数: {total_count}')
    print(f'包含ASR特性的数据数: {asr_feature_count}')
    print(f'ASR特性覆盖率: {(asr_feature_count / total_count * 100):.2f}%')
    print()
    print('各特性详细统计:')
    print(f'包含语气词的数据数: {mood_word_count} ({mood_word_count / total_count * 100:.2f}%)')
    print(f'包含情绪表达的数据数: {emotion_count} ({emotion_count / total_count * 100:.2f}%)')
    print(f'包含自然停顿的数据数: {pause_count} ({pause_count / total_count * 100:.2f}%)')
    print(f'包含口语化表达的数据数: {colloquial_count} ({colloquial_count / total_count * 100:.2f}%)')
    print('=' * 80)
    
    # 验证是否符合要求
    if asr_feature_count / total_count >= 0.5:
        print('✅ 符合要求：ASR特性覆盖率达到50%以上')
    else:
        print('❌ 不符合要求：ASR特性覆盖率未达到50%')
    print('=' * 80)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='统计测试数据中ASR特性的覆盖率')
    parser.add_argument('--test-data', type=str, required=True, help='测试数据CSV文件路径')
    args = parser.parse_args()
    count_asr_features(args.test_data)
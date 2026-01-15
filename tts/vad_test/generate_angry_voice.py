#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成生气语音样本：我草，怎么这都不懂
包含停顿和杂音
"""

import os
import sys

# 添加路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from vad_test.generate_vad_samples import generate_ssml, synthesize_speech, create_output_dir
from azure_tts.azure_config import validate_config

def main():
    """主函数：生成生气语音"""
    
    # 验证配置
    is_valid, message = validate_config()
    if not is_valid:
        print(f"配置错误：{message}")
        return False
    
    # 创建输出目录
    create_output_dir()
    
    # 生成SSML
    text = "我草，怎么这都不懂"
    ssml = generate_ssml(
        text=text,
        break_time_ms=800,  # 800ms停顿
        pause_position="句中",  # 在"我草，"和"怎么这都不懂"之间停顿
        style="angry",  # 愤怒情绪
        add_noise=True,  # 添加杂音
        prosody_rate="+10%",  # 语速稍快
        prosody_pitch="+5%",  # 音调稍高
        prosody_volume="loud"  # 音量较大
    )
    
    print("生成的SSML：")
    print(ssml)
    print("\n" + "="*50 + "\n")
    
    # 生成语音
    output_filename = "angry_voice_with_noise.wav"
    success = synthesize_speech(ssml, output_filename)
    
    if success:
        print(f"\n✓ 语音生成成功！")
        print(f"  文本内容：{text}")
        print(f"  情绪风格：愤怒")
        print(f"  停顿时长：800ms")
        print(f"  停顿位置：句中")
        print(f"  杂音：已添加")
        print(f"  输出文件：{output_filename}")
        return True
    else:
        print("\n✗ 语音生成失败！")
        return False

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
截取音频片段，用于SSML中的呼吸声效果
"""

from pydub import AudioSegment
import os

def get_audio_duration(file_path):
    """
    获取音频文件时长
    """
    audio = AudioSegment.from_file(file_path)
    return len(audio) / 1000  # 返回秒数

def extract_segment(input_file, output_file, start_ms, duration_ms):
    """
    截取音频片段
    :param input_file: 输入音频文件
    :param output_file: 输出音频文件
    :param start_ms: 开始时间（毫秒）
    :param duration_ms: 截取时长（毫秒）
    """
    try:
        # 加载音频
        audio = AudioSegment.from_file(input_file)
        
        # 截取片段
        segment = audio[start_ms:start_ms + duration_ms]
        
        # 保存片段
        segment.export(output_file, format="wav")
        print(f"音频片段截取成功：{output_file}")
        return True
    except Exception as e:
        print(f"音频片段截取失败：{str(e)}")
        return False

def main():
    """
    主函数
    """
    input_file = r"E:\AI测试用例\vad_samples\江秀街9号.m4a"
    output_file = r"E:\AI测试用例\vad_samples\breath_segment.wav"
    
    # 获取音频时长
    duration = get_audio_duration(input_file)
    print(f"原音频时长：{duration:.2f}秒")
    
    # 截取中间位置的0.5秒片段
    start_ms = int((duration * 1000) / 2)  # 中间位置
    duration_ms = 500  # 截取500ms
    
    extract_segment(input_file, output_file, start_ms, duration_ms)

if __name__ == "__main__":
    main()

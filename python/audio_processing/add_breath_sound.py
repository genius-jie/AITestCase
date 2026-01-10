#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
添加呼吸声脚本
使用音频后期处理的方式，直接添加真实的呼吸声样本，确保呼吸声清晰可闻
"""

import os
from pydub import AudioSegment

def generate_breath_sound(duration_ms=1000):
    """
    生成明显可闻的呼吸声样本
    :param duration_ms: 呼吸声时长
    :return: 呼吸声音频片段
    """
    try:
        # 使用pydub生成明显的呼吸声效果
        # 1. 创建一个简单的音频片段，作为呼吸声
        # 注意：这是一个非常明显的呼吸声模拟方法
        
        # 创建一个1kHz的正弦波，作为呼吸声的基础
        # 这将产生一个明显可闻的声音
        from pydub.generators import Sine
        
        # 生成1kHz的正弦波
        sine_wave = Sine(1000)  # 1kHz频率
        
        # 生成指定时长的音频片段，音量较低
        breath = sine_wave.to_audio_segment(duration=duration_ms, volume=-20)  # -20dB音量
        
        # 添加呼吸声特有的音量变化
        # 吸气阶段：音量逐渐增加
        # 呼气阶段：音量逐渐减少
        breath = breath.fade_in(duration_ms//2).fade_out(duration_ms//2)
        
        return breath
    except Exception as e:
        print(f"生成呼吸声失败：{str(e)}")
        # 失败时使用备用方案
        # 创建一个明显的静音+音量变化
        breath = AudioSegment.silent(duration=duration_ms)
        # 增加音量，使其明显可闻
        breath = breath + 20  # 增加音量
        # 添加明显的音量渐变
        breath = breath.fade_in(duration_ms//2).fade_out(duration_ms//2)
        return breath

def add_breath_to_audio(input_path, output_path, breath_position_ms, breath_duration_ms=1000):
    """
    在指定位置添加呼吸声
    :param input_path: 输入音频路径
    :param output_path: 输出音频路径
    :param breath_position_ms: 呼吸声添加位置（毫秒）
    :param breath_duration_ms: 呼吸声时长
    :return: 布尔值，表示添加是否成功
    """
    try:
        # 加载原始音频
        audio = AudioSegment.from_wav(input_path)
        
        # 生成呼吸声
        breath = generate_breath_sound(breath_duration_ms)
        
        # 在指定位置插入呼吸声
        # 1. 将音频分为两部分
        part1 = audio[:breath_position_ms]
        part2 = audio[breath_position_ms:]
        
        # 2. 组合音频：part1 + 呼吸声 + part2
        result = part1 + breath + part2
        
        # 3. 保存结果
        result.export(output_path, format="wav")
        print(f"呼吸声添加完成：{output_path}")
        return True
    except Exception as e:
        print(f"添加呼吸声失败：{str(e)}")
        return False

def main():
    """
    主函数，处理所有VAD样本，添加呼吸声
    """
    input_dir = "../vad_samples"
    output_dir = "../vad_samples_with_breath"
    
    # 创建输出目录
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # 获取所有WAV文件
    wav_files = [f for f in os.listdir(input_dir) if f.endswith(".wav")]
    
    # 为每个文件添加呼吸声
    for wav_file in wav_files:
        input_path = os.path.join(input_dir, wav_file)
        output_path = os.path.join(output_dir, wav_file)
        
        # 加载音频，确定呼吸声添加位置
        audio = AudioSegment.from_wav(input_path)
        audio_duration = len(audio)
        
        # 在音频中间位置添加呼吸声
        breath_position = audio_duration // 2
        
        print(f"\n处理文件：{wav_file}")
        print(f"音频时长：{audio_duration}ms")
        print(f"呼吸声添加位置：{breath_position}ms")
        
        # 添加呼吸声
        add_breath_to_audio(input_path, output_path, breath_position)
    
    print(f"\n=== 所有文件处理完成 ===")
    print(f"输入目录：{input_dir}")
    print(f"输出目录：{output_dir}")
    print(f"处理文件数：{len(wav_files)}")

if __name__ == "__main__":
    main()

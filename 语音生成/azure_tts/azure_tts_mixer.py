#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
使用Azure TTS生成语音并与背景音混音

功能：
1. 使用Azure TTS生成语音
2. 下载指定的背景音
3. 混音处理
"""

import os
import requests
from azure_config import SPEECH_KEY, SPEECH_REGION, VOICE_NAME
from azure.cognitiveservices.speech import SpeechConfig, SpeechSynthesizer, AudioConfig
from azure.cognitiveservices.speech import ResultReason, SpeechSynthesisOutputFormat
from pydub import AudioSegment

def generate_ssml(text, style=None):
    """
    生成Azure TTS的SSML文本
    """
    ssml_parts = [
        "<speak version='1.0' xmlns='http://www.w3.org/2001/10/synthesis' xml:lang='zh-CN' xmlns:mstts='http://www.w3.org/2001/mstts'>",
        f"<voice name='{VOICE_NAME}'>"
    ]
    
    if style and style != "normal":
        ssml_parts.append(f"<mstts:express-as style='{style}'>")
    
    ssml_parts.append(text)
    
    if style and style != "normal":
        ssml_parts.append("</mstts:express-as>")
    
    ssml_parts.append("</voice>")
    ssml_parts.append("</speak>")
    
    return "".join(ssml_parts)

def synthesize_speech(ssml, output_filename):
    """
    调用Azure TTS API生成语音
    """
    try:
        # 创建语音配置
        speech_config = SpeechConfig(subscription=SPEECH_KEY, region=SPEECH_REGION)
        speech_config.speech_synthesis_voice_name = VOICE_NAME
        
        # 设置音频格式
        audio_format_enum = SpeechSynthesisOutputFormat.Riff24Khz16BitMonoPcm
        speech_config.set_speech_synthesis_output_format(audio_format_enum)
        
        # 确保输出目录存在
        output_dir = "../vad_samples"
        os.makedirs(output_dir, exist_ok=True)
        
        # 创建完整输出路径
        full_output_path = os.path.join(output_dir, output_filename)
        
        # 创建音频配置
        audio_config = AudioConfig(filename=full_output_path)
        
        # 创建语音合成器
        synthesizer = SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
        
        # 生成语音
        print(f"正在生成Azure TTS语音：{full_output_path}")
        result = synthesizer.speak_ssml_async(ssml).get()
        
        if result.reason == ResultReason.SynthesizingAudioCompleted:
            print(f"Azure TTS语音生成成功：{full_output_path}")
            return True
        else:
            print(f"Azure TTS语音生成失败：{result.reason}")
            return False
    except Exception as e:
        print(f"Azure TTS语音生成异常：{str(e)}")
        return False

def load_background_audio(local_file):
    """
    加载本地背景音文件
    
    参数：
        local_file (str): 本地背景音文件路径
        
    返回：
        bool: 加载成功返回True，失败返回False
    """
    if os.path.exists(local_file):
        print(f"本地背景音文件已存在：{local_file}")
        return True
    else:
        print(f"错误：本地背景音文件不存在：{local_file}")
        return False

def mix_audio(tts_file, background_file, output_file='final_mixed_output.wav', 
              background_volume=-5, background_length_option='trim'):
    """
    将TTS语音与背景音混音
    """
    print(f"正在混音...")
    print(f"TTS文件：{tts_file}")
    print(f"背景音文件：{background_file}")
    
    # 加载音频文件
    tts = AudioSegment.from_file(tts_file)
    background = AudioSegment.from_file(background_file)
    
    # 获取TTS长度
    tts_length = len(tts)
    background_length = len(background)
    
    print(f"TTS长度：{tts_length / 1000:.2f}秒")
    print(f"背景音长度：{background_length / 1000:.2f}秒")
    
    # 处理背景音长度
    if background_length_option == 'trim':
        # 裁剪背景音到TTS长度
        if background_length > tts_length:
            background = background[:tts_length]
            print(f"已裁剪背景音到TTS长度：{tts_length / 1000:.2f}秒")
    elif background_length_option == 'loop':
        # 循环背景音到TTS长度
        if background_length < tts_length:
            # 计算需要循环的次数
            loop_count = int(tts_length / background_length) + 1
            background = background * loop_count
            background = background[:tts_length]
            print(f"已循环背景音到TTS长度：{tts_length / 1000:.2f}秒")
    elif background_length_option == 'full':
        # 使用完整背景音，不做处理
        print(f"使用完整背景音，TTS将在背景音结束前结束")
    
    # 调整背景音音量
    background = background + background_volume
    print(f"背景音音量已调整：{background_volume}dB")
    
    # 混音
    mixed = tts.overlay(background)
    
    # 确保输出目录存在
    output_dir = "../vad_samples"
    os.makedirs(output_dir, exist_ok=True)
    
    # 创建完整输出路径
    full_output_path = os.path.join(output_dir, output_file)
    
    # 导出混音结果
    mixed.export(full_output_path, format='wav')
    print(f"混音完成：{full_output_path}")
    print(f"混音文件长度：{len(mixed) / 1000:.2f}秒")
    
    return full_output_path

def main():
    """
    主函数
    """
    print("=== Azure TTS与背景音混音工具 ===")
    print()
    
    # 配置
    tts_text = "这是一段使用Azure TTS生成的测试语音，现在正在与背景音进行混音处理。"
    
    # 文件路径
    tts_file = "temp_azure_tts.wav"  # 临时文件名
    # 本地背景音文件路径（保存在python目录下）
    background_file = "background_noise.mp3"
    output_file = "azure_tts_with_background.wav"  # 最终输出文件名
    
    try:
        # 1. 生成Azure TTS语音（保存到vad_samples目录）
        ssml = generate_ssml(tts_text, style="cheerful")
        if not synthesize_speech(ssml, tts_file):
            print("TTS生成失败，退出程序")
            return
        
        # 获取完整的TTS文件路径
        full_tts_file = os.path.join("../vad_samples", tts_file)
        
        # 2. 加载本地背景音文件
        if not load_background_audio(background_file):
            print("背景音加载失败，退出程序")
            # 清理已生成的TTS文件
            if os.path.exists(full_tts_file):
                os.remove(full_tts_file)
            return
        
        # 3. 混音（保存到vad_samples目录）
        final_output = mix_audio(full_tts_file, background_file, output_file, 
                  background_volume=-10, background_length_option="trim")
        
        print()
        print(f"✅ 操作完成！")
        print(f"📄 TTS文本：{tts_text}")
        print(f"🎵 背景音文件：{background_file}")
        print(f"🔊 最终输出文件：{final_output}")
        
    except KeyboardInterrupt:
        print("\n程序被用户中断")
    except Exception as e:
        print(f"\n程序执行出错：{str(e)}")
    finally:
        # 清理临时文件
        # 临时TTS文件（如果存在）
        temp_tts_file = os.path.join("../vad_samples", tts_file)
        if os.path.exists(temp_tts_file):
            os.remove(temp_tts_file)
            print(f"已清理临时TTS文件：{temp_tts_file}")
        # 本地背景音文件不再需要清理

if __name__ == "__main__":
    main()
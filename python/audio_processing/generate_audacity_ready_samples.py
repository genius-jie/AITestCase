#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成适合Audacity后期处理的VAD测试样本
使用Azure TTS的自然停顿，然后使用Audacity自动化添加呼吸声
"""

from azure_config import SPEECH_KEY, SPEECH_REGION, VOICE_NAME
from azure.cognitiveservices.speech import SpeechConfig, SpeechSynthesizer, AudioConfig
from azure.cognitiveservices.speech import ResultReason, SpeechSynthesisOutputFormat
import os

# 输出目录
OUTPUT_DIR = "../vad_samples"

# 创建输出目录
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

def generate_natural_pause_ssml(text, style=None, pause_position="句中"):
    """
    生成带有自然停顿的SSML，适合后续用Audacity添加呼吸声
    :param text: 待合成的文本
    :param style: 语气风格
    :param pause_position: 停顿位置
    :return: 生成的SSML文本
    """
    ssml_parts = [
        "<speak version='1.0' xmlns='http://www.w3.org/2001/10/synthesis' xml:lang='zh-CN' xmlns:mstts='http://www.w3.org/2001/mstts'>",
        f"<voice name='{VOICE_NAME}'>"
    ]
    
    # 添加语气风格
    if style and style != "normal":
        ssml_parts.append(f"<mstts:express-as style='{style}'>")
    
    # 处理自然停顿
    if pause_position == "句中":
        # 在句中添加自然停顿
        if len(text) > 4:
            # 在词语边界添加停顿
            ssml_parts.append(text[:3])
            ssml_parts.append("<break time='500ms'/>")
            ssml_parts.append(text[3:])
        else:
            ssml_parts.append(text)
    elif pause_position == "句首":
        # 在句首添加停顿
        ssml_parts.append("<break time='300ms'/>")
        ssml_parts.append(text)
    else:  # 句尾
        # 在句尾添加停顿
        ssml_parts.append(text)
        ssml_parts.append("<break time='300ms'/>")
    
    # 关闭语气风格标签
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
        
        # 创建音频配置
        output_path = os.path.join(OUTPUT_DIR, output_filename)
        audio_config = AudioConfig(filename=output_path)
        
        # 创建语音合成器
        synthesizer = SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
        
        # 生成语音
        print(f"正在生成语音：{output_filename}")
        result = synthesizer.speak_ssml_async(ssml).get()
        
        if result.reason == ResultReason.SynthesizingAudioCompleted:
            print(f"语音生成成功：{output_path}")
            return True
        else:
            print(f"语音生成失败：{result.reason}")
            return False
    except Exception as e:
        print(f"语音生成异常：{str(e)}")
        return False

def generate_audacity_ready_samples():
    """
    生成适合Audacity后期处理的样本
    """
    # 测试用例
    test_cases = [
        ("自然对话", "我觉得这个方案挺好的", "gentle", "句中"),
        ("开心交流", "今天天气真好", "cheerful", "句中"),
        ("严肃讨论", "这个问题需要仔细考虑", "serious", "句中")
    ]
    
    for i, (scenario_name, text, style, pause_position) in enumerate(test_cases):
        print(f"\n=== 生成样本 {i+1}/{len(test_cases)} ===")
        
        # 生成SSML
        ssml = generate_natural_pause_ssml(text, style, pause_position)
        
        # 生成输出文件名
        output_filename = f"SC_AUDACITY_{i+1:02d}_{scenario_name}.wav"
        
        # 生成语音
        synthesize_speech(ssml, output_filename)
    
    # 生成Audacity自动化脚本
    generate_audacity_script()

def generate_audacity_script():
    """
    生成Audacity自动化脚本，用于添加呼吸声
    """
    audacity_script = '''
;; Audacity自动化脚本 - 添加呼吸声
;; 此脚本需要在Audacity中执行

;; 步骤1：打开生成的音频文件
;; 你需要手动打开一个音频文件，然后运行此脚本

;; 步骤2：选择音频中的自然停顿位置
;; 这里假设你已经选择了要添加呼吸声的区域

;; 步骤3：生成并添加呼吸声
NewMonoTrack: TrackName="Breath" Type="wave"
SelectTracks: Track=0 Mode="Set"
SelectTime: Start=0 End=1
GenerateTone: Frequency=100 Waveform="Sine" Amplitude=0.1
SelectTime: Start=0 End=0.5
Effect: Name="Fade In"
SelectTime: Start=0.5 End=1
Effect: Name="Fade Out"
SelectTime: Start=0 End=1
Copy
SelectTracks: Track=1 Mode="Set"
Paste

;; 步骤4：调整呼吸声音量
SelectTracks: Track=2 Mode="Set"
Effect: Name="Amplify" dB=-10

;; 步骤5：混合音频轨道
MixAndRender: CreateTracks=0

;; 步骤6：导出音频
Export2: Filename="your_output_file.wav" NumChannels=1
    '''
    
    script_path = os.path.join(OUTPUT_DIR, "audacity_breath_script.txt")
    with open(script_path, "w", encoding="utf-8") as f:
        f.write(audacity_script)
    
    print(f"\n=== Audacity自动化脚本生成成功 ===")
    print(f"脚本路径：{script_path}")
    print("\n使用说明：")
    print("1. 打开Audacity")
    print("2. 打开生成的音频文件")
    print("3. 选择你想要添加呼吸声的停顿区域")
    print("4. 在Audacity中打开此脚本（文件 -> 导入 -> 导入脚本...）")
    print("5. 运行脚本（工具 -> 脚本 -> 运行...）")
    print("6. 调整呼吸声参数以获得最佳效果")

if __name__ == "__main__":
    print("=== 生成适合Audacity后期处理的VAD测试样本 ===")
    generate_audacity_ready_samples()
    print("\n=== 生成完成 ===")
    print(f"输出目录：{OUTPUT_DIR}")

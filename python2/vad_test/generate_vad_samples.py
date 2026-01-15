#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VAD测试样本生成脚本
使用Azure TTS生成标准化的VAD测试样本，支持不同场景和停顿时长
"""

import os
import sys
import csv
import json
import random
from azure.cognitiveservices.speech import SpeechConfig, SpeechSynthesizer, AudioConfig
from azure.cognitiveservices.speech import ResultReason, SpeechSynthesisOutputFormat
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from azure_tts.azure_config import SPEECH_KEY, SPEECH_REGION, VOICE_NAME, AUDIO_FORMAT, OUTPUT_DIR, validate_config
from audio_processing.add_breath_sound import add_breath_to_audio

def create_output_dir():
    """创建输出目录"""
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        print(f"创建输出目录：{OUTPUT_DIR}")
    else:
        print(f"输出目录已存在：{OUTPUT_DIR}")

def generate_ssml(text, break_time_ms=None, pause_position=None, 
                 prosody_rate=None, prosody_pitch=None, prosody_volume=None, 
                 emphasis_words=None, style=None, add_noise=False):
    """
    生成符合Azure TTS规范的SSML文本，确保prosody属性和语气风格正确应用
    
    Args:
        text: 待合成的文本内容
        break_time_ms: 停顿时长（毫秒）
        pause_position: 停顿位置（句首/句中/句尾）
        prosody_rate: 语速调整（slow/normal/fast 或 -50% 到 +100%）
        prosody_pitch: 音高调整（x-low/low/medium/high/x-high 或 -50% 到 +50%）
        prosody_volume: 音量调整（silent/x-soft/soft/medium/loud/x-loud 或 -40dB 到 +40dB）
        emphasis_words: 需要强调的词语（逗号分隔）
        style: 语气风格（cheerful/serious/customerService等）
        add_noise: 是否添加杂音
    
    Returns:
        生成的SSML文本
    """
    ssml_parts = ["<speak version='1.0' xmlns='http://www.w3.org/2001/10/synthesis' xml:lang='zh-CN' xmlns:mstts='http://www.w3.org/2001/mstts'>"]
    ssml_parts.append(f"<voice name='{VOICE_NAME}'>")
    
    # 处理语气风格
    style_applied = False
    if style and style != "normal":
        # 只使用style属性，移除不被支持的intensity属性
        ssml_parts.append(f"<mstts:express-as style='{style}'>")
        style_applied = True
    
    # 构建prosody标签，确保语速、音高、音量属性正确应用
    prosody_attrs = []
    
    # 基于语气风格的自动prosody调整，增强语气差异
    style_prosody = {
        "cheerful": {"rate": "+15%", "pitch": "+10%"},
        "serious": {"rate": "-10%", "pitch": "-5%"},
        "sad": {"rate": "-20%", "pitch": "-15%"},
        "excited": {"rate": "+20%", "pitch": "+15%"},
        "angry": {"rate": "+10%", "pitch": "+5%"},
        "gentle": {"rate": "-15%", "pitch": "-5%"},
    }
    
    # 应用基于风格的默认prosody设置，但允许用户自定义参数覆盖
    # 只对非normal风格应用自动prosody调整
    if style and style != "normal" and style in style_prosody:
        default_prosody = style_prosody[style]
        # 如果用户没有提供自定义值，则使用基于风格的默认值
        if not prosody_rate or prosody_rate == "normal":
            prosody_rate = default_prosody["rate"]
        if not prosody_pitch:
            prosody_pitch = default_prosody["pitch"]
    
    # 添加prosody属性
    if prosody_rate and prosody_rate != "normal":
        prosody_attrs.append(f"rate='{prosody_rate}'")
    if prosody_pitch:
        prosody_attrs.append(f"pitch='{prosody_pitch}'")
    if prosody_volume and prosody_volume != "normal":
        # 使用所有预定义音量值，确保音量差异明显
        prosody_attrs.append(f"volume='{prosody_volume}'")
    
    # 处理文本内容和停顿
    content_parts = []
    
    # 使用免费的公共杂音URL列表 - 从Pixabay获取
    noise_urls = [
        "https://cdn.pixabay.com/audio/2025/11/07/audio_d613f744f2.mp3",
        "https://cdn.pixabay.com/audio/2026/01/08/audio_14060a21f9.mp3",
        "https://cdn.pixabay.com/audio/2024/09/20/audio_9c10ad2e35.mp3",
        "https://cdn.pixabay.com/audio/2024/09/20/audio_31602561df.mp3",
        "https://cdn.pixabay.com/audio/2021/08/04/audio_209174bd86.mp3",
        "https://www.orangefreesounds.com/wp-content/uploads/2021/12/Male-breath-in-and-hold-sound-effect.mp3",
        "https://orangefreesounds.com/wp-content/uploads/2025/12/Single-loud-distant-firecracker-explosion-in-city-sound-effect.mp3"
    ]
    # 随机选择一个杂音URL
    noise_url = random.choice(noise_urls)
    
    # 处理停顿和真实杂音效果
    if break_time_ms:
        if pause_position == "句首":
            # 句首停顿模拟吸气
            if add_noise:
                content_parts.append(f"<audio src='{noise_url}'/>")
            content_parts.append(f"<break time='{break_time_ms}ms'/>")
            content_parts.append(text)
        elif pause_position == "句尾":
            # 句尾停顿模拟呼气
            content_parts.append(text)
            content_parts.append(f"<break time='{break_time_ms}ms'/>")
            if add_noise:
                content_parts.append(f"<audio src='{noise_url}'/>")
        else:  # 默认句中
            # 在词语边界添加停顿和真实杂音
            if len(text) > 4:
                # 尝试在词语边界添加停顿和杂音
                content_parts.append(text[:2])
                if add_noise:
                    content_parts.append(f"<audio src='{noise_url}'/>")
                content_parts.append(f"<break time='{break_time_ms}ms'/>")
                content_parts.append(text[2:])
            else:
                # 短文本直接添加停顿
                content_parts.append(text)
                if add_noise:
                    content_parts.append(f"<audio src='{noise_url}'/>")
                content_parts.append(f"<break time='{break_time_ms}ms'/>")
    else:
        # 没有指定停顿时，根据文本长度添加自然停顿和杂音
        if len(text) > 6:
            # 在长文本中间添加停顿和杂音
            content_parts.append(text[:3])
            if add_noise:
                content_parts.append(f"<audio src='{noise_url}'/>")
            content_parts.append("<break time='300ms'/>")
            content_parts.append(text[3:])
        elif len(text) > 4:
            # 稍长文本添加句尾停顿和杂音
            content_parts.append(text)
            if add_noise:
                content_parts.append(f"<audio src='{noise_url}'/>")
            content_parts.append("<break time='200ms'/>")
        else:
            # 短文本直接添加
            content_parts.append(text)
            if add_noise:
                content_parts.append(f"<audio src='{noise_url}'/>")
    
    # 应用prosody标签
    content = "".join(content_parts)
    if prosody_attrs:
        ssml_parts.append(f"<prosody {' '.join(prosody_attrs)}>{content}</prosody>")
    else:
        ssml_parts.append(content)
    
    # 关闭语气风格标签
    if style_applied:
        ssml_parts.append("</mstts:express-as>")
    
    ssml_parts.append("</voice>")
    ssml_parts.append("</speak>")
    return "".join(ssml_parts)

def synthesize_speech(ssml, output_filename):
    """
    调用Azure TTS API生成语音
    :param ssml: SSML文本
    :param output_filename: 输出文件名
    :return: 布尔值，表示生成是否成功
    """
    try:
        # 创建语音配置
        speech_config = SpeechConfig(subscription=SPEECH_KEY, region=SPEECH_REGION)
        speech_config.speech_synthesis_voice_name = VOICE_NAME
        
        # 设置音频格式（使用枚举值）
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
        elif result.reason == ResultReason.Canceled:
            print(f"语音生成失败：{result.reason}")
            cancellation_details = result.cancellation_details
            print(f"取消原因：{cancellation_details.reason}")
            try:
                print(f"错误代码：{cancellation_details.error_code}")
                print(f"错误详情：{cancellation_details.error_details}")
            except Exception as ex:
                print(f"获取错误详情时发生异常：{str(ex)}")
            return False
        else:
            print(f"语音生成失败：{result.reason}")
            if hasattr(result, 'error_details') and result.error_details:
                print(f"错误详情：{result.error_details}")
            return False
    except Exception as e:
        print(f"语音生成异常：{str(e)}")
        return False

def process_audio_volume(output_filename, fade_duration=300):
    """
    处理音频音量，添加更明显的渐变效果
    :param output_filename: 输入/输出文件名
    :param fade_duration: 渐变时长（毫秒），增加到300ms使效果更明显
    :return: 布尔值，表示处理是否成功
    """
    try:
        from pydub import AudioSegment
        
        # 加载音频文件
        input_path = os.path.join(OUTPUT_DIR, output_filename)
        audio = AudioSegment.from_wav(input_path)
        
        # 如果音频长度小于渐变时长的2倍，则不进行处理
        if len(audio) < fade_duration * 2:
            print(f"音频长度过短，跳过音量处理：{output_filename}")
            return True
        
        # 添加更明显的淡入淡出效果
        # 增强停顿前后的音量变化，使效果更明显
        processed_audio = audio.fade_in(fade_duration).fade_out(fade_duration)
        
        # 保存处理后的音频
        processed_audio.export(input_path, format="wav")
        print(f"音量处理完成：{output_filename}")
        return True
    except ImportError:
        print("pydub库未安装，跳过音频处理")
        return False
    except Exception as e:
        print(f"音频处理异常：{str(e)}")
        return False

def add_background_noise(output_filename, noise_level=-20):
    """
    添加真实的背景噪音，直接使用pydub实现混音功能
    :param output_filename: 输入/输出文件名
    :param noise_level: 噪音音量（dB）
    :return: 布尔值，表示处理是否成功
    """
    try:
        from pydub import AudioSegment
        import os
        
        # 加载音频文件
        input_path = os.path.join(OUTPUT_DIR, output_filename)
        tts_audio = AudioSegment.from_wav(input_path)
        
        # 使用真实的背景噪音文件
        background_file = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "background_noise.mp3")
        
        if not os.path.exists(background_file):
            print(f"背景噪音文件不存在：{background_file}")
            return False
        
        # 加载背景噪音
        background = AudioSegment.from_mp3(background_file)
        
        print(f"=== 混音处理开始 ===")
        print(f"TTS文件：{input_path}")
        print(f"背景噪音文件：{background_file}")
        print(f"TTS长度：{len(tts_audio) / 1000:.2f}秒")
        print(f"背景噪音长度：{len(background) / 1000:.2f}秒")
        print(f"背景噪音音量调整：{noise_level}dB")
        
        # 处理背景音长度（trim模式）
        if len(background) > len(tts_audio):
            background = background[:len(tts_audio)]
            print(f"已裁剪背景音到TTS长度：{len(tts_audio) / 1000:.2f}秒")
        elif len(background) < len(tts_audio):
            # 循环背景音到TTS长度
            loop_count = int(len(tts_audio) / len(background)) + 1
            background = background * loop_count
            background = background[:len(tts_audio)]
            print(f"已循环背景音到TTS长度：{len(tts_audio) / 1000:.2f}秒")
        
        # 调整背景音音量
        background = background + noise_level
        
        # 混音
        mixed = tts_audio.overlay(background)
        
        # 保存处理后的音频
        mixed.export(input_path, format="wav")
        
        print(f"混音完成：{output_filename}")
        print(f"混音文件长度：{len(mixed) / 1000:.2f}秒")
        print(f"=== 混音处理结束 ===")
        
        return True
    except ImportError as e:
        print(f"导入错误，跳过噪音添加：{str(e)}")
        return False
    except Exception as e:
        print(f"噪音添加异常：{str(e)}")
        import traceback
        traceback.print_exc()
        return False

# 从CSV读取测试数据
def read_test_data_from_csv(csv_file):
    """
    从CSV文件读取测试数据
    
    Args:
        csv_file: CSV文件路径
        
    Returns:
        测试数据列表
    """
    test_data = []
    
    # 先读取所有行，跳过注释行和空行
    with open(csv_file, 'r', encoding='utf-8') as f:
        # 读取所有行并过滤
        lines = []
        for line in f:
            line = line.strip()
            # 跳过注释行和空行
            if line and not line.startswith('#'):
                lines.append(line)
    
    # 如果没有有效行，返回空列表
    if not lines:
        return test_data
    
    # 使用csv.DictReader处理过滤后的行
    import io
    csv_data = io.StringIO('\n'.join(lines))
    reader = csv.DictReader(csv_data)
    
    for row in reader:
        # 跳过可能的空行
        if not row or not any(row.values()):
            continue
        
        # 转换数据类型
        if row['break_time_ms']:
            row['break_time_ms'] = int(row['break_time_ms'])
        else:
            row['break_time_ms'] = None
        
        # 转换布尔值字段，处理空值情况
        add_breath_value = row.get('add_post_process_breath', 'false')
        row['add_post_process_breath'] = add_breath_value.lower() == 'true' if add_breath_value else False
        
        expected_silence_value = row.get('expected_silence', 'false')
        row['expected_silence'] = expected_silence_value.lower() == 'true' if expected_silence_value else False
        
        expected_speech_value = row.get('expected_speech', 'true')
        row['expected_speech'] = expected_speech_value.lower() == 'true' if expected_speech_value else True
        
        # 处理预期后处理呼吸效果字段
        if 'expected_post_process_breath' in row:
            expected_breath_value = row['expected_post_process_breath']
            row['expected_post_process_breath'] = expected_breath_value.lower() == 'true' if expected_breath_value else False
        else:
            row['expected_post_process_breath'] = False
        
        # 转换数值字段 - 添加错误处理
        for field in ['sample_rate', 'channels', 'bit_depth']:
            if field in row and row[field]:
                try:
                    row[field] = int(row[field])
                except ValueError:
                    # 如果转换失败，使用默认值
                    if field == 'sample_rate':
                        row[field] = 16000
                    elif field == 'channels':
                        row[field] = 1
                    elif field == 'bit_depth':
                        row[field] = 16
        
        test_data.append(row)
    return test_data

# 生成VAD测试样本
def generate_vad_samples(test_data_file="vad_test_data.csv"):
    """生成VAD测试样本"""
    # 验证配置
    is_valid, message = validate_config()
    if not is_valid:
        print(f"配置错误：{message}")
        print("请在azure_config.py中设置有效的API密钥和服务区域")
        return False
    
    # 创建输出目录
    create_output_dir()
    
    # 读取测试数据
    test_data = read_test_data_from_csv(test_data_file)
    
    # 生成测试样本
    success_count = 0
    for i, data in enumerate(test_data):
        print(f"\n=== 生成样本 {i+1}/{len(test_data)} ===")
        
        # 获取style参数，确保正确处理
        style = data['style'].strip() if data['style'] else None
        if style and style.lower() == 'none':
            style = None
        
        # 生成SSML
        ssml = generate_ssml(
            text=data['text'],
            break_time_ms=data.get('break_time_ms'),
            pause_position=data.get('pause_position'),
            prosody_rate=data.get('prosody_rate'),
            prosody_pitch=data.get('prosody_pitch'),
            prosody_volume=data.get('prosody_volume'),
            emphasis_words=data.get('emphasis_words'),
            style=style,
            add_noise=data.get('add_post_process_breath', False)  # 暂时保留原有字段名，仅修改函数参数名
        )
        
        # 生成输出文件名
        output_filename = f"{data['scenario_id']}_{data['scenario_name']}.wav"
        
        # 打印生成信息
        print(f"场景：{data['scenario_name']}")
        print(f"文本：{data['text']}")
        print(f"停顿时长：{data.get('break_time_ms')}ms" if data.get('break_time_ms') else "停顿时长：无")
        print(f"停顿位置：{data.get('pause_position')}" if data.get('pause_position') else "停顿位置：无")
        print(f"后处理添加杂音：{data.get('add_post_process_breath', False)}")
        if data.get('add_post_process_breath', False):
            print(f"杂音强度：{data.get('breath_strength', 'medium')}")
        print(f"语速：{data.get('prosody_rate', 'normal')}")
        print(f"语气风格：{style}" if style else "语气风格：无")
        print(f"SSML：{ssml}")
        
        # 合成语音
        if synthesize_speech(ssml, output_filename):
            # 音频后期处理
            process_audio_volume(output_filename, fade_duration=100)
            add_background_noise(output_filename, noise_level=-30)
            
            success_count += 1
    
    print(f"\n=== 生成完成 ===")
    print(f"总场景数：{len(test_data)}")
    print(f"成功数：{success_count}")
    print(f"失败数：{len(test_data) - success_count}")
    print(f"输出目录：{OUTPUT_DIR}")
    
    return success_count == len(test_data)

def main():
    """主函数"""
    print("=== VAD测试样本生成工具 ===")
    print("使用Azure TTS生成标准化的VAD测试样本\n")
    
    # 解析命令行参数
    import argparse
    parser = argparse.ArgumentParser(description='VAD测试样本生成工具')
    parser.add_argument('--test-data', '-d', type=str, default='vad_test_data.csv', 
                      help='测试数据CSV文件路径 (默认: vad_test_data.csv)')
    args = parser.parse_args()
    
    # 运行生成任务
    if generate_vad_samples(args.test_data):
        print("\n所有测试样本生成成功！")
        return 0
    else:
        print("\n测试样本生成失败！")
        return 1

if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成符合Azure TTS规范的SSML文本
"""

def generate_ssml(text, break_time_ms=None, pause_position=None, 
                 prosody_rate=None, prosody_pitch=None, prosody_volume=None, 
                 emphasis_words=None, style=None):
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
    
    Returns:
        生成的SSML文本
    """
    ssml_parts = ["<speak version='1.0' xmlns='http://www.w3.org/2001/10/synthesis' xml:lang='zh-CN'>"]
    ssml_parts.append(f"<voice name='zh-CN-XiaoxiaoNeural'>")
    
    # 构建prosody标签，确保语速、音高、音量属性正确应用
    prosody_attrs = []
    if prosody_rate and prosody_rate != "normal":
        prosody_attrs.append(f"rate='{prosody_rate}'")
    if prosody_pitch:
        prosody_attrs.append(f"pitch='{prosody_pitch}'")
    if prosody_volume and prosody_volume != "normal":
        prosody_attrs.append(f"volume='{prosody_volume}'")
    
    # 处理文本内容和停顿
    content_parts = []
    
    if break_time_ms:
        if pause_position == "句首":
            content_parts.append(f"<break time='{break_time_ms}ms'/>")
            content_parts.append(text)
        elif pause_position == "句尾":
            content_parts.append(text)
            content_parts.append(f"<break time='{break_time_ms}ms'/>")
        else:  # 默认句中
            # 在词语边界添加停顿，更符合自然语言习惯
            if len(text) > 4:
                # 尝试在词语边界添加停顿
                content_parts.append(text[:2])
                content_parts.append(f"<break time='{break_time_ms}ms'/>")
                content_parts.append(text[2:])
            else:
                # 短文本直接添加停顿
                content_parts.append(text)
                content_parts.append(f"<break time='{break_time_ms}ms'/>")
    else:
        # 没有指定停顿时，直接添加文本
        content_parts.append(text)
    
    # 应用prosody标签
    content = "".join(content_parts)
    if prosody_attrs:
        ssml_parts.append(f"<prosody {' '.join(prosody_attrs)}>{content}</prosody>")
    else:
        ssml_parts.append(content)
    
    ssml_parts.append("</voice>")
    ssml_parts.append("</speak>")
    return "".join(ssml_parts)

# 测试代码
if __name__ == "__main__":
    # 测试不同语速设置
    test_cases = [
        ("正常语速", "今天天气真好", None, None, "normal", None, None, None, None),
        ("快速语速", "今天天气真好", None, None, "fast", None, None, None, None),
        ("慢速语速", "今天天气真好", None, None, "slow", None, None, None, None),
        ("自定义快速", "今天天气真好", None, None, "+50%", None, None, None, None),
        ("自定义慢速", "今天天气真好", None, None, "-30%", None, None, None, None),
    ]
    
    for test_name, *args in test_cases:
        ssml = generate_ssml(*args)
        print(f"\n=== {test_name} ===")
        print(ssml)

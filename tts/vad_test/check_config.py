#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
检查Azure TTS配置
"""

import os
import sys

# 添加路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from azure_tts.azure_config import SPEECH_KEY, SPEECH_REGION, VOICE_NAME, validate_config

def main():
    """检查配置"""
    print("="*50)
    print("Azure TTS 配置检查")
    print("="*50)
    print(f"语音密钥: {SPEECH_KEY[:20]}...{SPEECH_KEY[-10:] if SPEECH_KEY else 'None'}")
    print(f"服务区域: {SPEECH_REGION}")
    print(f"语音名称: {VOICE_NAME}")
    print("="*50)
    
    is_valid, message = validate_config()
    print(f"配置验证: {message}")
    print("="*50)

if __name__ == "__main__":
    main()

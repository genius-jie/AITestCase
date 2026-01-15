# Azure TTS配置文件
# 请根据实际情况填写以下配置，或通过环境变量设置

import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# Azure TTS API密钥
# 环境变量名：AZURE_SPEECH_KEY
SPEECH_KEY = os.environ.get("AZURE_SPEECH_KEY", "YOUR_AZURE_SPEECH_KEY")

# Azure TTS服务区域
# 环境变量名：AZURE_SPEECH_REGION
# 常见区域：eastasia, southeastasia, centralus, eastus等
SPEECH_REGION = os.environ.get("AZURE_SPEECH_REGION", "eastus")

# 语音配置
VOICE_NAME = "zh-CN-XiaoxiaoNeural"  # 晓晓音色
# 其他可选音色：zh-CN-YunxiNeural（云希）, zh-CN-YunyangNeural（云扬）等

# 音频格式
AUDIO_FORMAT = "riff-24khz-16bit-mono-pcm"  # WAV格式，适合VAD测试

# 输出目录
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "vad_samples")  # 测试样本输出目录（绝对路径）

# 验证配置是否完整
def validate_config():
    """验证配置是否完整，返回布尔值和错误信息"""
    if not SPEECH_KEY or SPEECH_KEY == "your_speech_key_here":
        return False, "请设置有效的AZURE_SPEECH_KEY"
    if not SPEECH_REGION or SPEECH_REGION == "your_speech_region_here":
        return False, "请设置有效的AZURE_SPEECH_REGION"
    return True, "配置验证通过"

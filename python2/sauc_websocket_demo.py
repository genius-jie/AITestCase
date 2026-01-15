#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SAUC ASR WebSocket 客户端
功能：通过 WebSocket 协议实时访问字节跳动大模型流式语音识别服务（ASR）

主要特性：
- 支持实时流式语音识别
- 支持音频文件批量识别
- 自动音频格式转换（使用 FFmpeg）
- 支持 ITN（智能文本转换）、标点符号、数字格式化
- 支持多种 API 端点（流式、异步、非流式）

依赖库：
- asyncio: 异步 I/O
- aiohttp: 异步 HTTP 客户端
- ffmpeg: 音频格式转换（需要系统安装）
"""

import asyncio
import aiohttp
import json
import struct
import gzip
import uuid
import logging
import os
import subprocess
from typing import Optional, List, Dict, Any, Tuple, AsyncGenerator
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('run.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# 常量定义
DEFAULT_SAMPLE_RATE = 16000  # 默认音频采样率（Hz）

class ProtocolVersion:
    """协议版本号定义"""
    V1 = 0b0001  # 协议版本 1

class MessageType:
    """消息类型定义"""
    CLIENT_FULL_REQUEST = 0b0001  # 客户端完整请求（包含配置信息）
    CLIENT_AUDIO_ONLY_REQUEST = 0b0010  # 客户端纯音频数据请求
    SERVER_FULL_RESPONSE = 0b1001  # 服务端完整响应
    SERVER_ERROR_RESPONSE = 0b1111  # 服务端错误响应

class MessageTypeSpecificFlags:
    """消息类型特定标志位"""
    NO_SEQUENCE = 0b0000  # 无序列号
    POS_SEQUENCE = 0b0001  # 正序列号
    NEG_SEQUENCE = 0b0010  # 负序列号
    NEG_WITH_SEQUENCE = 0b0011  # 负序列号（用于最后一个包）

class SerializationType:
    """序列化类型定义"""
    NO_SERIALIZATION = 0b0000  # 无序列化
    JSON = 0b0001  # JSON 序列化

class CompressionType:
    """压缩类型定义"""
    GZIP = 0b0001  # GZIP 压缩


class Config:
    """配置类：从环境变量加载 SAUC API 密钥"""
    
    def __init__(self):
        # 填入控制台获取的app id和access token
        # 环境变量名：SAUC_APP_KEY
        # 环境变量名：SAUC_ACCESS_KEY
        self.auth = {
            "app_key": os.environ.get("SAUC_APP_KEY", "YOUR_SAUC_APP_KEY"),
            "access_key": os.environ.get("SAUC_ACCESS_KEY", "YOUR_SAUC_ACCESS_KEY")
        }

    @property
    def app_key(self) -> str:
        """获取应用密钥"""
        return self.auth["app_key"]

    @property
    def access_key(self) -> str:
        """获取访问密钥"""
        return self.auth["access_key"]

config = Config()

class CommonUtils:
    """通用工具类：提供压缩、音频处理等工具方法"""
    
    @staticmethod
    def gzip_compress(data: bytes) -> bytes:
        """使用 GZIP 压缩数据"""
        return gzip.compress(data)

    @staticmethod
    def gzip_decompress(data: bytes) -> bytes:
        """解压 GZIP 数据"""
        return gzip.decompress(data)

    @staticmethod
    def judge_wav(data: bytes) -> bool:
        """判断是否为有效的 WAV 文件格式"""
        if len(data) < 44:
            return False
        return data[:4] == b'RIFF' and data[8:12] == b'WAVE'

    @staticmethod
    def convert_wav_with_path(audio_path: str, sample_rate: int = DEFAULT_SAMPLE_RATE) -> bytes:
        """
        使用 FFmpeg 将音频文件转换为标准 WAV 格式
        
        参数：
            audio_path: 音频文件路径
            sample_rate: 目标采样率（默认 16000 Hz）
            
        返回：
            转换后的 WAV 音频数据（字节）
        """
        try:
            cmd = [
                "ffmpeg", "-v", "quiet", "-y", "-i", audio_path,
                "-acodec", "pcm_s16le", "-ac", "1", "-ar", str(sample_rate),
                "-f", "wav", "-"
            ]
            result = subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            # 尝试删除原始文件
            try:
                os.remove(audio_path)
            except OSError as e:
                logger.warning(f"Failed to remove original file: {e}")
                
            return result.stdout
        except subprocess.CalledProcessError as e:
            logger.error(f"FFmpeg conversion failed: {e.stderr.decode()}")
            raise RuntimeError(f"Audio conversion failed: {e.stderr.decode()}")

    @staticmethod
    def read_wav_info(data: bytes) -> Tuple[int, int, int, int, bytes]:
        """
        解析 WAV 文件头信息
        
        参数：
            data: WAV 文件数据（字节）
            
        返回：
            元组包含：(声道数, 采样宽度, 采样率, 采样数, 音频数据)
            
        异常：
            ValueError: 当 WAV 文件格式无效时抛出
        """
        if len(data) < 44:
            raise ValueError("Invalid WAV file: too short")
            
        # 解析WAV头
        chunk_id = data[:4]
        if chunk_id != b'RIFF':
            raise ValueError("Invalid WAV file: not RIFF format")
            
        format_ = data[8:12]
        if format_ != b'WAVE':
            raise ValueError("Invalid WAV file: not WAVE format")
            
        # 解析fmt子块
        audio_format = struct.unpack('<H', data[20:22])[0]
        num_channels = struct.unpack('<H', data[22:24])[0]
        sample_rate = struct.unpack('<I', data[24:28])[0]
        bits_per_sample = struct.unpack('<H', data[34:36])[0]
        
        # 查找data子块
        pos = 36
        while pos < len(data) - 8:
            subchunk_id = data[pos:pos+4]
            subchunk_size = struct.unpack('<I', data[pos+4:pos+8])[0]
            if subchunk_id == b'data':
                wave_data = data[pos+8:pos+8+subchunk_size]
                return (
                    num_channels,
                    bits_per_sample // 8,
                    sample_rate,
                    subchunk_size // (num_channels * (bits_per_sample // 8)),
                    wave_data
                )
            pos += 8 + subchunk_size
            
        raise ValueError("Invalid WAV file: no data subchunk found")

class AsrRequestHeader:
    """ASR 请求头类：构建 WebSocket 请求的头部信息"""
    
    def __init__(self):
        self.message_type = MessageType.CLIENT_FULL_REQUEST
        self.message_type_specific_flags = MessageTypeSpecificFlags.POS_SEQUENCE
        self.serialization_type = SerializationType.JSON
        self.compression_type = CompressionType.GZIP
        self.reserved_data = bytes([0x00])

    def with_message_type(self, message_type: int) -> 'AsrRequestHeader':
        """设置消息类型"""
        self.message_type = message_type
        return self

    def with_message_type_specific_flags(self, flags: int) -> 'AsrRequestHeader':
        """设置消息类型特定标志"""
        self.message_type_specific_flags = flags
        return self

    def with_serialization_type(self, serialization_type: int) -> 'AsrRequestHeader':
        """设置序列化类型"""
        self.serialization_type = serialization_type
        return self

    def with_compression_type(self, compression_type: int) -> 'AsrRequestHeader':
        """设置压缩类型"""
        self.compression_type = compression_type
        return self

    def with_reserved_data(self, reserved_data: bytes) -> 'AsrRequestHeader':
        """设置保留数据"""
        self.reserved_data = reserved_data
        return self

    def to_bytes(self) -> bytes:
        """将请求头转换为字节数组"""
        header = bytearray()
        header.append((ProtocolVersion.V1 << 4) | 1)
        header.append((self.message_type << 4) | self.message_type_specific_flags)
        header.append((self.serialization_type << 4) | self.compression_type)
        header.extend(self.reserved_data)
        return bytes(header)

    @staticmethod
    def default_header() -> 'AsrRequestHeader':
        """创建默认请求头"""
        return AsrRequestHeader()

class RequestBuilder:
    """请求构建器类：构建各种类型的 ASR 请求"""
    
    @staticmethod
    def new_auth_headers() -> Dict[str, str]:
        """
        创建 WebSocket 认证请求头
        
        返回：
            包含认证信息的字典
        """
        reqid = str(uuid.uuid4())
        return {
            "X-Api-Resource-Id": "volc.bigasr.sauc.duration",
            "X-Api-Request-Id": reqid,
            "X-Api-Access-Key": config.access_key,
            "X-Api-App-Key": config.app_key
        }

    @staticmethod
    def new_full_client_request(seq: int) -> bytes:
        """
        创建完整的客户端请求（包含配置信息）
        
        参数：
            seq: 序列号
            
        返回：
            完整的请求数据（字节）
        """
        header = AsrRequestHeader.default_header() \
            .with_message_type_specific_flags(MessageTypeSpecificFlags.POS_SEQUENCE)
        
        # 构建请求负载
        payload = {
            "user": {
                "uid": "demo_uid"
            },
            "audio": {
                "format": "wav",
                "codec": "raw",
                "rate": 16000,
                "bits": 16,
                "channel": 1
            },
            "request": {
                "model_name": "bigmodel",
                "enable_itn": True,  # 启用智能文本转换（ITN）
                "enable_punc": True,  # 启用标点符号
                "enable_ddc": True,  # 启用数字格式化（DDC）
                "show_utterances": True,  # 显示语音片段
                "enable_nonstream": False  # 非流式模式
            }
        }
        
        payload_bytes = json.dumps(payload).encode('utf-8')
        compressed_payload = CommonUtils.gzip_compress(payload_bytes)
        payload_size = len(compressed_payload)
        
        request = bytearray()
        request.extend(header.to_bytes())
        request.extend(struct.pack('>i', seq))
        request.extend(struct.pack('>I', payload_size))
        request.extend(compressed_payload)
        
        return bytes(request)

    @staticmethod
    def new_audio_only_request(seq: int, segment: bytes, is_last: bool = False) -> bytes:
        """
        创建纯音频数据请求
        
        参数：
            seq: 序列号
            segment: 音频数据片段
            is_last: 是否为最后一个片段
            
        返回：
            音频请求数据（字节）
        """
        header = AsrRequestHeader.default_header()
        if is_last:  # 最后一个包特殊处理
            header.with_message_type_specific_flags(MessageTypeSpecificFlags.NEG_WITH_SEQUENCE)
            seq = -seq  # 设为负值
        else:
            header.with_message_type_specific_flags(MessageTypeSpecificFlags.POS_SEQUENCE)
        header.with_message_type(MessageType.CLIENT_AUDIO_ONLY_REQUEST)
        
        request = bytearray()
        request.extend(header.to_bytes())
        request.extend(struct.pack('>i', seq))
        
        compressed_segment = CommonUtils.gzip_compress(segment)
        request.extend(struct.pack('>I', len(compressed_segment)))
        request.extend(compressed_segment)
        
        return bytes(request)

class AsrResponse:
    """ASR 响应类：封装服务端返回的响应数据"""
    
    def __init__(self):
        self.code = 0  # 响应码（0 表示成功）
        self.event = 0  # 事件类型
        self.is_last_package = False  # 是否为最后一个包
        self.payload_sequence = 0  # 负载序列号
        self.payload_size = 0  # 负载大小
        self.payload_msg = None  # 负载消息内容

    def to_dict(self) -> Dict[str, Any]:
        """将响应转换为字典格式"""
        return {
            "code": self.code,
            "event": self.event,
            "is_last_package": self.is_last_package,
            "payload_sequence": self.payload_sequence,
            "payload_size": self.payload_size,
            "payload_msg": self.payload_msg
        }

class ResponseParser:
    """响应解析器类：解析服务端返回的响应数据"""
    
    @staticmethod
    def parse_response(msg: bytes) -> AsrResponse:
        """
        解析服务端响应消息
        
        参数：
            msg: 服务端返回的原始消息（字节）
            
        返回：
            解析后的 AsrResponse 对象
        """
        response = AsrResponse()
        
        # 解析消息头
        header_size = msg[0] & 0x0f
        message_type = msg[1] >> 4
        message_type_specific_flags = msg[1] & 0x0f
        serialization_method = msg[2] >> 4
        message_compression = msg[2] & 0x0f
        
        payload = msg[header_size*4:]
        
        # 解析message_type_specific_flags
        if message_type_specific_flags & 0x01:
            response.payload_sequence = struct.unpack('>i', payload[:4])[0]
            payload = payload[4:]
        if message_type_specific_flags & 0x02:
            response.is_last_package = True
        if message_type_specific_flags & 0x04:
            response.event = struct.unpack('>i', payload[:4])[0]
            payload = payload[4:]
            
        # 解析message_type
        if message_type == MessageType.SERVER_FULL_RESPONSE:
            response.payload_size = struct.unpack('>I', payload[:4])[0]
            payload = payload[4:]
        elif message_type == MessageType.SERVER_ERROR_RESPONSE:
            response.code = struct.unpack('>i', payload[:4])[0]
            response.payload_size = struct.unpack('>I', payload[4:8])[0]
            payload = payload[8:]
            
        if not payload:
            return response
            
        # 解压缩
        if message_compression == CompressionType.GZIP:
            try:
                payload = CommonUtils.gzip_decompress(payload)
            except Exception as e:
                logger.error(f"Failed to decompress payload: {e}")
                return response
                
        # 解析payload
        try:
            if serialization_method == SerializationType.JSON:
                response.payload_msg = json.loads(payload.decode('utf-8'))
        except Exception as e:
            logger.error(f"Failed to parse payload: {e}")
            
        return response

class AsrWsClient:
    """ASR WebSocket 客户端类：实现与服务端的 WebSocket 通信"""
    
    def __init__(self, url: str, segment_duration: int = 200):
        """
        初始化 ASR WebSocket 客户端
        
        参数：
            url: WebSocket 服务地址
            segment_duration: 音频分段时长（毫秒），默认 200ms
        """
        self.seq = 1  # 序列号计数器
        self.url = url  # WebSocket 服务地址
        self.segment_duration = segment_duration  # 音频分段时长
        self.conn = None  # WebSocket 连接对象
        self.session = None  # HTTP 会话对象

    async def __aenter__(self):
        """异步上下文管理器入口：创建 HTTP 会话"""
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc, tb):
        """异步上下文管理器退出：关闭连接和会话"""
        if self.conn and not self.conn.closed:
            await self.conn.close()
        if self.session and not self.session.closed:
            await self.session.close()
        
    async def read_audio_data(self, file_path: str) -> bytes:
        """
        读取音频文件数据
        
        参数：
            file_path: 音频文件路径
            
        返回：
            音频数据（字节）
        """
        try:
            with open(file_path, 'rb') as f:
                content = f.read()
                
            # 如果不是 WAV 格式，使用 FFmpeg 转换
            if not CommonUtils.judge_wav(content):
                logger.info("Converting audio to WAV format...")
                content = CommonUtils.convert_wav_with_path(file_path, DEFAULT_SAMPLE_RATE)
                
            return content
        except Exception as e:
            logger.error(f"Failed to read audio data: {e}")
            raise
            
    def get_segment_size(self, content: bytes) -> int:
        """
        计算音频分段大小
        
        参数：
            content: 音频数据（字节）
            
        返回：
            每个分段的大小（字节）
        """
        try:
            channel_num, samp_width, frame_rate, _, _ = CommonUtils.read_wav_info(content)[:5]
            size_per_sec = channel_num * samp_width * frame_rate
            segment_size = size_per_sec * self.segment_duration // 1000
            return segment_size
        except Exception as e:
            logger.error(f"Failed to calculate segment size: {e}")
            raise
            
    async def create_connection(self) -> None:
        """创建 WebSocket 连接"""
        headers = RequestBuilder.new_auth_headers()
        try:
            self.conn = await self.session.ws_connect(
                self.url,
                headers=headers
            )
            logger.info(f"Connected to {self.url}")
        except Exception as e:
            logger.error(f"Failed to connect to WebSocket: {e}")
            raise
            
    async def send_full_client_request(self) -> None:
        """发送完整的客户端请求（包含配置信息）"""
        request = RequestBuilder.new_full_client_request(self.seq)
        self.seq += 1  # 发送后递增序列号
        try:
            await self.conn.send_bytes(request)
            logger.info(f"Sent full client request with seq: {self.seq-1}")
            
            # 接收服务端响应
            msg = await self.conn.receive()
            if msg.type == aiohttp.WSMsgType.BINARY:
                response = ResponseParser.parse_response(msg.data)
                logger.info(f"Received response: {response.to_dict()}")
            else:
                logger.error(f"Unexpected message type: {msg.type}")
        except Exception as e:
            logger.error(f"Failed to send full client request: {e}")
            raise
            
    async def send_messages(self, segment_size: int, content: bytes) -> AsyncGenerator[None, None]:
        """
        发送音频数据消息（流式发送）
        
        参数：
            segment_size: 每个分段的大小
            content: 音频数据
            
        异步生成器：
            每发送一个分段后 yield 一次
        """
        audio_segments = self.split_audio(content, segment_size)
        total_segments = len(audio_segments)
        
        for i, segment in enumerate(audio_segments):
            is_last = (i == total_segments - 1)
            request = RequestBuilder.new_audio_only_request(
                self.seq, 
                segment,
                is_last=is_last
            )
            await self.conn.send_bytes(request)
            logger.info(f"Sent audio segment with seq: {self.seq} (last: {is_last})")
            
            if not is_last:
                self.seq += 1
                
            # 逐个发送，间隔时间模拟实时流
            await asyncio.sleep(self.segment_duration / 1000)
            # 让出控制权，允许接收消息
            yield
            
    async def recv_messages(self) -> AsyncGenerator[AsrResponse, None]:
        """
        接收服务端响应消息
        
        异步生成器：
            每接收到一个响应后 yield 一次
        """
        try:
            async for msg in self.conn:
                if msg.type == aiohttp.WSMsgType.BINARY:
                    response = ResponseParser.parse_response(msg.data)
                    yield response
                    
                    # 如果是最后一个包或出现错误，停止接收
                    if response.is_last_package or response.code != 0:
                        break
                elif msg.type == aiohttp.WSMsgType.ERROR:
                    logger.error(f"WebSocket error: {msg.data}")
                    break
                elif msg.type == aiohttp.WSMsgType.CLOSED:
                    logger.info("WebSocket connection closed")
                    break
        except Exception as e:
            logger.error(f"Error receiving messages: {e}")
            raise
            
    async def start_audio_stream(self, segment_size: int, content: bytes) -> AsyncGenerator[AsrResponse, None]:
        """
        启动音频流处理（同时发送和接收）
        
        参数：
            segment_size: 每个分段的大小
            content: 音频数据
            
        异步生成器：
            每接收到一个识别结果后 yield 一次
        """
        async def sender():
            """发送任务：发送音频数据"""
            async for _ in self.send_messages(segment_size, content):
                pass
                
        # 启动发送和接收任务
        sender_task = asyncio.create_task(sender())
        
        try:
            # 接收识别结果
            async for response in self.recv_messages():
                yield response
        finally:
            # 取消发送任务
            sender_task.cancel()
            try:
                await sender_task
            except asyncio.CancelledError:
                pass
                
    @staticmethod
    def split_audio(data: bytes, segment_size: int) -> List[bytes]:
        """
        将音频数据分段
        
        参数：
            data: 音频数据（字节）
            segment_size: 每个分段的大小
            
        返回：
            分段后的音频数据列表
        """
        if segment_size <= 0:
            return []
            
        segments = []
        for i in range(0, len(data), segment_size):
            end = i + segment_size
            if end > len(data):
                end = len(data)
            segments.append(data[i:end])
        return segments
        
    async def execute(self, file_path: str) -> AsyncGenerator[AsrResponse, None]:
        """
        执行完整的 ASR 识别流程
        
        参数：
            file_path: 音频文件路径
            
        异步生成器：
            每接收到一个识别结果后 yield 一次
            
        异常：
            ValueError: 当文件路径或 URL 为空时抛出
        """
        if not file_path:
            raise ValueError("File path is empty")
            
        if not self.url:
            raise ValueError("URL is empty")
            
        self.seq = 1  # 重置序列号
        
        try:
            # 1. 读取音频文件
            content = await self.read_audio_data(file_path)
            
            # 2. 计算分段大小
            segment_size = self.get_segment_size(content)
            
            # 3. 创建WebSocket连接
            await self.create_connection()
            
            # 4. 发送完整客户端请求
            await self.send_full_client_request()
            
            # 5. 启动音频流处理
            async for response in self.start_audio_stream(segment_size, content):
                yield response
                
        except Exception as e:
            logger.error(f"Error in ASR execution: {e}")
            raise
        finally:
            # 关闭连接
            if self.conn:
                await self.conn.close()

async def main():
    """主函数：命令行入口"""
    import argparse
    
    parser = argparse.ArgumentParser(description="ASR WebSocket Client")
    parser.add_argument("--file", type=str, required=True, help="Audio file path")

    # 支持的 API 端点：
    # wss://openspeech.bytedance.com/api/v3/sauc/bigmodel - 实时流式识别
    # wss://openspeech.bytedance.com/api/v3/sauc/bigmodel_async - 异步识别
    # wss://openspeech.bytedance.com/api/v3/sauc/bigmodel_nostream - 非流式识别（默认）
    parser.add_argument("--url", type=str, default="wss://openspeech.bytedance.com/api/v3/sauc/bigmodel_nostream", 
                       help="WebSocket URL")
    parser.add_argument("--seg-duration", type=int, default=200, 
                       help="Audio duration(ms) per packet, default:200")
    
    args = parser.parse_args()
    
    # 使用异步上下文管理器创建客户端
    async with AsrWsClient(args.url, args.seg_duration) as client:
        try:
            # 执行 ASR 识别并打印结果
            async for response in client.execute(args.file):
                logger.info(f"Received response: {json.dumps(response.to_dict(), indent=2, ensure_ascii=False)}")
        except Exception as e:
            logger.error(f"ASR processing failed: {e}")

if __name__ == "__main__":
    asyncio.run(main())

# 使用示例：
# 1. 基本用法（使用默认参数）：
#    python sauc_websocket_demo.py --file /path/to/audio.wav
#
# 2. 指定 API 端点：
#    python sauc_websocket_demo.py --file /path/to/audio.wav --url wss://openspeech.bytedance.com/api/v3/sauc/bigmodel
#
# 3. 自定义音频分段时长：
#    python sauc_websocket_demo.py --file /path/to/audio.wav --seg-duration 100
#
# 4. 完整参数示例：
#    python sauc_websocket_demo.py --file /path/to/audio.wav --url wss://openspeech.bytedance.com/api/v3/sauc/bigmodel --seg-duration 200
#
# 注意事项：
# - 需要先安装 FFmpeg 并确保其在系统 PATH 中
# - 需要在 .env 文件中配置 SAUC_APP_KEY 和 SAUC_ACCESS_KEY
# - 支持的音频格式：WAV、MP3、FLAC 等（会自动转换为 WAV）
# - 默认音频格式：16kHz、单声道、16-bit PCM

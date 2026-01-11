湃启WebSocket 通信协议文档1.0
1. 连接地址
1.1 WebSocket URL 格式
设备端连接服务器时，需要使用以下 URL 格式：

| Plain Text
ws://<host>:<port>/?device_id=<device_id>&user_id=<user_id> |
| --- |

示例：

| Plain Text
ws://118.196.28.154:8460/?device_id=设备唯一标识&user_id=用户唯一标识 |
| --- |

URL 参数说明：

点击图片可查看完整电子表格

| [!TIP]
在 URL 中提前传递 device_id和user_id 可以让服务器在 WebSocket 握手阶段就开始预热设备专属配置，显著降低首次对话的响应延迟。 |
| --- |


2. 通用请求头
建立 WebSocket 连接时需设置以下请求头：

点击图片可查看完整电子表格

3. 消息格式
WebSocket 传输两种类型的数据：

点击图片可查看完整电子表格
3.1 JSON 消息通用结构
所有 JSON 消息都包含以下基础字段：

| JSON
{
  "type": "消息类型",
  "session_id": "会话标识",
  "user_id": "用户标识",
  "trace_id": "追踪标识"
} |
| --- |


4. 设备端 → 服务器消息
4.1 hello - 握手消息
连接成功后设备端发送的第一条消息，用于交换参数和建立会话。

| JSON
{
  "type": "hello",
  "version": 1,
  "features": {
    "mcp": true
  },
  "transport": "websocket",
  "audio_params": {
    "format": "opus",
    "sample_rate": 16000,
    "channels": 1,
    "frame_duration": 60
  },
  "device_id": "设备唯一标识",
  "device_name": "设备名称",
  "user_id": "用户唯一标识",
  "trace_id": "日志追踪ID",
  "device_mac": "设备MAC地址",
  "client_id": "客户端ID",
  "client_ip": "客户端IP地址",
  "client_info": {
    "os_type": "Android",
    "os_version": "14",
    "app_version": "1.2.3",
    "network_type": "wifi",
    "network_provider": "CMCC",
    "timezone": "Asia/Shanghai",
    "country_code": "CN",
    "battery_level": 76,
    "is_charging": true
  }
} |
| --- |


点击图片可查看完整电子表格
client_info 字段说明：

点击图片可查看完整电子表格

4.2 listen - 语音监听控制
控制语音识别的开始、停止和检测状态。
开始监听

| JSON
{
  "session_id": "xxx",
  "type": "listen",
  "state": "start",
  "mode": "auto"
} |
| --- |

停止监听

| JSON
{
  "session_id": "xxx",
  "type": "listen",
  "state": "stop"
} |
| --- |

检测到语音/文本

| JSON
{
  "session_id": "xxx",
  "type": "listen",
  "state": "detect",
  "text": "用户说的话或唤醒词"
} |
| --- |


点击图片可查看完整电子表格

4.3 interrupt - 打断当前播放

| [!IMPORTANT]
这是客户端主动打断服务器 TTS 播放的推荐方式。服务器会停止当前 TTS 播放，但保持 ASR 继续识别。 |
| --- |



| JSON
{
  "session_id": "xxx",
  "type": "interrupt"
} |
| --- |

服务器处理后会返回 interrupt_complete 消息确认打断完成。

5. 服务器 → 设备端消息
5.1 hello - 握手响应
服务器对设备端 hello 消息的响应。

| JSON
{
  "type": "hello",
  "version": 1,
  "transport": "websocket",
  "session_id": "会话标识",
  "user_id": "用户标识",
  "trace_id": "追踪标识",
  "audio_params": {
    "format": "opus",
    "sample_rate": 24000,
    "channels": 1,
    "frame_duration": 60
  }
} |
| --- |



| [!NOTE]
服务器下行音频采样率可能为 24000Hz，以获得更好的音质。设备端需注意处理采样率差异。 |
| --- |


5.2 stt - 语音识别结果
服务器返回的语音识别结果。

| JSON
{
  "session_id": "xxx",
  "type": "stt",
  "text": "识别到的文本",
  "user_id": "xxx",
  "trace_id": "xxx",
  "emotion_fusion_analysis": "情绪分析结果",
  "emotion_code": 1,
  "label": "情绪标签"
} |
| --- |


点击图片可查看完整电子表格

5.3 tts - TTS 状态消息
控制 TTS 音频播放的生命周期。
开始播放

| JSON
{
  "session_id": "xxx",
  "type": "tts",
  "state": "start",
  "reason": "init",
  "tts_type": "text",
  "audio_codec": "opus"
} |
| --- |

句子开始

| JSON
{
  "session_id": "xxx",
  "type": "tts",
  "state": "sentence_start",
  "text": "要播放的文本内容",
  "index": 1,
  "tts_type": "text",
  "emotion_tag": "情绪标签"
} |
| --- |

句子结束

| JSON
{
  "session_id": "xxx",
  "type": "tts",
  "state": "sentence_end",
  "text": "播放完成的文本",
  "index": 1,
  "tts_type": "text"
} |
| --- |

停止播放

| JSON
{
  "session_id": "xxx",
  "type": "tts",
  "state": "stop",
  "index": 1,
  "reason": "complete",
  "tts_type": "text"
} |
| --- |


点击图片可查看完整电子表格
state 状态值：

点击图片可查看完整电子表格
reason 原因值：

点击图片可查看完整电子表格
tts_type 类型值：

点击图片可查看完整电子表格


5.4 interrupt_complete - 打断完成
服务器确认打断处理完成。

| JSON
{
  "session_id": "xxx",
  "type": "interrupt_complete",
  "user_id": "xxx",
  "trace_id": "xxx",
  "reason": "client_interrupt_processed"
} |
| --- |


5.5 goodbye - 告别消息
服务器发送的连接关闭消息。

| JSON
{
  "session_id": "xxx",
  "type": "goodbye",
  "version": 1,
  "transport": "websocket",
  "talk_rounds": 5,
  "reason": "connection_closed"
} |
| --- |


5.6 emoji - 表情消息
发送表情/动作指令，用于控制设备表情显示。

| JSON
{
  "session_id": "xxx",
  "type": "emoji",
  "version": 1,
  "transport": "websocket",
  "talk_rounds": 1,
  "emoji_map": "3"
} |
| --- |


点击图片可查看完整电子表格
表情编码映射表：

点击图片可查看完整电子表格

5.7 error - 错误消息
服务器返回的错误信息。

| JSON
{
  "session_id": "xxx",
  "type": "error",
  "message": "错误描述"
} |
| --- |


5.8 mcp - MCP 工具调用
服务器下发的 MCP 工具调用请求。

| JSON
{
  "type": "mcp",
  "session_id": "<会话ID>",
  "payload": {
    "jsonrpc": "2.0",
    "method": "<方法名>",
    "params": {
      "<参数名>": "<参数值>"
    }
  }
} |
| --- |


点击图片可查看完整电子表格

服务器下发 MCP 控制消息示例
以下为服务器向设备端下发的常用 MCP 控制指令示例及参数说明：
exit - 退出对话
服务器指示设备端结束当前对话会话。

| JSON
{
  "type": "mcp",
  "session_id": "2cc0a361-af5a-42d2-9d78-f83e7aa32ea9",
  "payload": {
    "jsonrpc": "2.0",
    "method": "exit",
    "params": {
      "say_goodbye": "回帕奇星系啦～"
    }
  }
} |
| --- |


点击图片可查看完整电子表格

play_music - 播放音乐
服务器指示设备端播放本地音乐。

| JSON
{
  "type": "mcp",
  "session_id": "2cc0a361-af5a-42d2-9d78-f83e7aa32ea9",
  "payload": {
    "jsonrpc": "2.0",
    "method": "play_music",
    "params": {
      "song_name": "两只老虎"
    }
  }
} |
| --- |


点击图片可查看完整电子表格
song_name 示例值：

点击图片可查看完整电子表格

play_white_noise - 播放白噪声
服务器指示设备端播放助眠/放松类白噪声。

| JSON
{
  "type": "mcp",
  "session_id": "2cc0a361-af5a-42d2-9d78-f83e7aa32ea9",
  "payload": {
    "jsonrpc": "2.0",
    "method": "play_white_noise",
    "params": {
      "noise_name": "雨声"
    }
  }
} |
| --- |


点击图片可查看完整电子表格
noise_name 示例值：

点击图片可查看完整电子表格

set_volume - 设置绝对音量
服务器指示设备端将音量设置为指定的绝对值。

| JSON
{
  "type": "mcp",
  "session_id": "2cc0a361-af5a-42d2-9d78-f83e7aa32ea9",
  "payload": {
    "jsonrpc": "2.0",
    "method": "set_volume",
    "params": {
      "volume": 50
    }
  }
} |
| --- |


点击图片可查看完整电子表格
volume 常用值：

点击图片可查看完整电子表格

| [!TIP]
当用户明确指定具体音量数值时（如"音量调到80%"、"静音"），使用 set_volume。 |
| --- |


adjust_volume - 相对调节音量
服务器指示设备端相对当前音量进行增减调节。

| JSON
{
  "type": "mcp",
  "session_id": "2cc0a361-af5a-42d2-9d78-f83e7aa32ea9",
  "payload": {
    "jsonrpc": "2.0",
    "method": "adjust_volume",
    "params": {
      "adjustment": 20
    }
  }
} |
| --- |


点击图片可查看完整电子表格
adjustment 示例值：

点击图片可查看完整电子表格

| [!TIP]
当用户表达音量不合适但没有指定具体值时（如"声音大一点"、"太吵了"），使用 adjust_volume。 |
| --- |



set_brightness - 设置绝对亮度
服务器指示设备端将屏幕亮度设置为指定的绝对值。

| JSON
{
  "type": "mcp",
  "session_id": "2cc0a361-af5a-42d2-9d78-f83e7aa32ea9",
  "payload": {
    "jsonrpc": "2.0",
    "method": "set_brightness",
    "params": {
      "brightness": 50
    }
  }
} |
| --- |


点击图片可查看完整电子表格
brightness 常用值：

点击图片可查看完整电子表格

| [!TIP]
当用户明确指定具体亮度级别时（如"亮度调到50%"、"调到最亮"），使用 set_brightness。 |
| --- |


adjust_brightness - 相对调节亮度
服务器指示设备端相对当前亮度进行增减调节。

| JSON
{
  "type": "mcp",
  "session_id": "2cc0a361-af5a-42d2-9d78-f83e7aa32ea9",
  "payload": {
    "jsonrpc": "2.0",
    "method": "adjust_brightness",
    "params": {
      "adjustment": 20
    }
  }
} |
| --- |


点击图片可查看完整电子表格
adjustment 示例值：

点击图片可查看完整电子表格

| [!TIP]
当用户表达亮度不合适但没有指定具体值时（如"太暗了"、"太刺眼"），使用 adjust_brightness。 |
| --- |


MCP 控制消息通用结构

点击图片可查看完整电子表格
set_* 与 adjust_* 使用场景对比

点击图片可查看完整电子表格


6. 二进制音频协议
6.1 音频格式

点击图片可查看完整电子表格
6.2 协议版本
通过 version 字段配置二进制协议版本：
版本 1（默认）
直接发送 Opus 音频数据，无额外元数据。
版本 2
带时间戳的二进制协议，适用于服务器端 AEC（回声消除）：

| C
struct BinaryProtocol2 {
    uint16_t version;        // 协议版本
    uint16_t type;           // 消息类型 (0: OPUS, 1: JSON)
    uint32_t reserved;       // 保留字段
    uint32_t timestamp;      // 时间戳（毫秒）
    uint32_t payload_size;   // 负载大小（字节）
    uint8_t payload[];       // 负载数据
} __attribute__((packed)); |
| --- |

版本 3
简化的二进制协议：

| C
struct BinaryProtocol3 {
    uint8_t type;            // 消息类型
    uint8_t reserved;        // 保留字段
    uint16_t payload_size;   // 负载大小
    uint8_t payload[];       // 负载数据
} __attribute__((packed)); |
| --- |


7. 典型交互流程
7.1 完整对话示例

| JSON
// 1. 设备端→服务器：握手
{
  "type": "hello",
  "version": 1,
  "transport": "websocket",
  "audio_params": {
    "format": "opus",
    "sample_rate": 16000,
    "channels": 1,
    "frame_duration": 60
  },
  "device_id": "device_001",
  "user_id": "user_001"
}

// 2. 服务器→设备端：握手响应
{
  "type": "hello",
  "transport": "websocket",
  "session_id": "sess_abc123",
  "audio_params": {
    "format": "opus",
    "sample_rate": 24000
  }
}

// 3. 设备端→服务器：开始监听
{
  "session_id": "sess_abc123",
  "type": "listen",
  "state": "start",
  "mode": "auto"
}

// 4. 设备端→服务器：发送二进制音频数据...

// 5. 服务器→设备端：语音识别结果
{
  "session_id": "sess_abc123",
  "type": "stt",
  "text": "今天天气怎么样"
}

// 6. 服务器→设备端：TTS 开始
{
  "session_id": "sess_abc123",
  "type": "tts",
  "state": "start"
}

// 7. 服务器→设备端：句子开始
{
  "session_id": "sess_abc123",
  "type": "tts",
  "state": "sentence_start",
  "text": "今天北京晴，气温15到25度",
  "index": 1
}

// 8. 服务器→设备端：发送二进制音频数据...

// 9. 服务器→设备端：句子结束
{
  "session_id": "sess_abc123",
  "type": "tts",
  "state": "sentence_end",
  "text": "今天北京晴，气温15到25度",
  "index": 1
}

// 10. 服务器→设备端：TTS 结束
{
  "session_id": "sess_abc123",
  "type": "tts",
  "state": "stop",
  "reason": "complete"
} |
| --- |

7.2 打断流程示例

| JSON
// 1. 设备端→服务器：打断请求
{
  "session_id": "sess_abc123",
  "type": "interrupt"
}

// 2. 服务器→设备端：TTS 停止
{
  "session_id": "sess_abc123",
  "type": "tts",
  "state": "stop",
  "reason": "interrupt"
}

// 3. 服务器→设备端：打断完成
{
  "session_id": "sess_abc123",
  "type": "interrupt_complete",
  "reason": "client_interrupt_processed"
} |
| --- |


8. 错误处理
8.1 连接错误
握手超时：设备端在 10 秒内未收到服务器 hello 响应，应断开重连
服务器断开：触发 OnDisconnected 回调，设备回到空闲状态
8.2 消息错误
格式错误：服务器返回 type: "error" 消息
缺少必要字段：服务器记录错误日志，不执行业务逻辑

9. 附录
9.1 消息类型速查表
设备端 → 服务器

点击图片可查看完整电子表格
服务器 → 设备端

点击图片可查看完整电子表格
9.2 表情编码速查表

点击图片可查看完整电子表格

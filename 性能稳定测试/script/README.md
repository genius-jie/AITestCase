# WebSocket JMeter 测试脚本使用说明

## 脚本概述

本脚本实现了完整的WebSocket对话流程测试，包含以下12个步骤：

1. 建立WebSocket连接
2. 发送hello握手消息
3. 接收hello响应
4. 发送listen start消息
5. 发送二进制音频数据
6. 接收stt识别结果
7. 接收TTS start消息
8. 接收TTS sentence_start消息
9. 接收TTS音频数据
10. 接收TTS sentence_end消息
11. 接收TTS stop消息
12. 关闭WebSocket连接

## 测试流程说明

### 步骤1：建立WebSocket连接

- **组件**：OpenWebSocketSampler
- **配置**：
  - 服务器地址：`${SERVER_HOST}`（默认：118.196.28.154）
  - 端口：`${SERVER_PORT}`（默认：8460）
  - URL路径：`/?device_id=${DEVICE_ID}&user_id=${USER_ID}`
  - 连接超时：20秒
  - 读取超时：30秒

### 步骤2：发送hello握手消息

- **组件**：WebSocketSingleWriteSampler
- **内容**：完整的hello握手JSON消息
- **包含字段**：
  - type: "hello"
  - version: 1
  - features: {mcp: true}
  - transport: "websocket"
  - audio_params: {format: "opus", sample_rate: 16000, channels: 1, frame_duration: 60}
  - device_id, device_name, user_id, trace_id
  - device_mac, client_id, client_ip
  - client_info: 设备详细信息
- **响应时间断言**：≤ 5秒

### 步骤3：接收hello响应

- **组件**：WebSocketSingleReadSampler
- **验证**：
  - 验证响应类型为"hello"
  - 验证session_id存在
  - 提取session_id到变量`${SESSION_ID}`供后续使用

### 步骤4：发送listen start消息

- **组件**：WebSocketSingleWriteSampler
- **内容**：
  ```json
  {
    "session_id": "${SESSION_ID}",
    "type": "listen",
    "state": "start",
    "mode": "auto"
  }
  ```
- **响应时间断言**：≤ 2秒

### 步骤5：发送二进制音频数据

- **组件**：WebSocketSingleWriteSampler
- **注意**：当前使用占位符`BINARY_AUDIO_DATA_PLACEHOLDER`
- **重要**：需要替换为实际的Opus编码音频数据
- **音频参数**：
  - 格式：Opus
  - 采样率：16000Hz
  - 声道：单声道
  - 帧时长：60ms
- **响应时间断言**：≤ 30秒

### 步骤6：接收stt识别结果

- **组件**：WebSocketSingleReadSampler
- **验证**：
  - 验证消息类型为"stt"
  - 验证识别文本存在
- **读取超时**：30秒

### 步骤7：接收TTS start消息

- **组件**：WebSocketSingleReadSampler
- **验证**：
  - 验证消息类型为"tts"
  - 验证状态为"start"
- **读取超时**：10秒

### 步骤8：接收TTS sentence_start消息

- **组件**：WebSocketSingleReadSampler
- **验证**：
  - 验证状态为"sentence_start"
- **读取超时**：5秒

### 步骤9：接收TTS音频数据

- **组件**：WebSocketSingleReadSampler
- **说明**：接收服务器返回的TTS音频数据
- **读取超时**：30秒

### 步骤10：接收TTS sentence_end消息

- **组件**：WebSocketSingleReadSampler
- **验证**：
  - 验证状态为"sentence_end"
- **读取超时**：5秒

### 步骤11：接收TTS stop消息

- **组件**：WebSocketSingleReadSampler
- **验证**：
  - 验证状态为"stop"
  - 验证原因为"complete"
- **读取超时**：5秒

### 步骤12：关闭WebSocket连接

- **组件**：CloseWebSocketSampler
- **说明**：优雅关闭WebSocket连接

## 用户自定义变量

脚本中定义了以下变量，可在Test Plan中修改：

| 变量名 | 默认值 | 说明 |
|--------|--------|------|
| DEVICE_ID | 00:11:22:33:44:55 | 设备唯一标识 |
| USER_ID | 00:11:22:33:44:55 | 用户唯一标识 |
| SERVER_HOST | 118.196.28.154 | 服务器地址 |
| SERVER_PORT | 8460 | 服务器端口 |

## 重要注意事项

### 1. 二进制音频数据

**当前问题**：步骤5中的音频数据使用占位符`BINARY_AUDIO_DATA_PLACEHOLDER`

**解决方案**：

#### 方案1：使用文件读取（推荐）

1. 准备Opus编码的音频文件
2. 在JMeter中添加`CSV Data Set Config`或`BeanShell Sampler`读取音频文件
3. 将读取的二进制数据发送到WebSocket

#### 方案2：使用JSR223 Sampler

```groovy
// 读取音频文件
import java.nio.file.Files
import java.nio.file.Paths

def audioPath = "path/to/your/audio.opus"
def audioBytes = Files.readAllBytes(Paths.get(audioPath))

// 将字节数组转换为Base64或直接发送
def sampler = ctx.getCurrentSampler()
sampler.setBinaryData(audioBytes)
```

#### 方案3：使用Pre-Processor

在"发送二进制音频数据"采样器上添加`JSR223 Pre-Processor`：

```groovy
// 生成测试音频数据（示例）
import java.nio.ByteBuffer

def frameSize = 960 // 60ms at 16kHz
def numFrames = 100 // 6秒音频
def audioData = ByteBuffer.allocate(frameSize * numFrames)

// 填充测试数据（实际应使用真实Opus编码数据）
for (int i = 0; i < audioData.capacity(); i++) {
    audioData.put((byte)0)
}

sampler.setBinaryData(audioData.array())
```

### 2. 线程组配置

- **线程数**：1（单线程测试）
- **Ramp-Up时间**：1秒
- **循环次数**：1（执行一次完整对话）

如需进行性能测试，可以：
- 增加线程数（模拟多个并发用户）
- 增加循环次数（模拟多次对话）
- 调整Ramp-Up时间（控制并发启动速度）

### 3. 超时设置

各步骤的超时设置根据实际业务场景调整：

| 步骤 | 超时时间 | 说明 |
|------|----------|------|
| 连接 | 20秒 | 建立连接超时 |
| hello发送 | 10秒 | 握手消息发送超时 |
| hello接收 | 10秒 | 握手响应接收超时 |
| listen start | 5秒 | 监听开始消息超时 |
| 音频发送 | 60秒 | 音频数据发送超时 |
| stt接收 | 30秒 | 语音识别超时 |
| TTS start | 10秒 | TTS开始消息超时 |
| TTS音频 | 30秒 | TTS音频接收超时 |
| TTS结束 | 5秒 | TTS结束消息超时 |
| 关闭连接 | 5秒 | 连接关闭超时 |

### 4. 断言配置

脚本中包含以下断言：

- **响应时间断言**：验证关键步骤的响应时间
- **JSONPath断言**：验证JSON响应的字段和值
- **字段存在性断言**：验证关键字段是否存在

### 5. 结果收集

脚本配置了`View Results Tree`监听器，可以查看：
- 请求和响应数据
- 响应时间
- 断言结果
- 成功/失败状态

## 运行脚本

### 前置条件

1. 安装JMeter 5.6.3或更高版本
2. 安装WebSocket插件（JMeter WebSocket Sampler）
3. 准备测试用的音频数据（Opus格式）

### 运行步骤

1. 打开JMeter GUI
2. 打开脚本文件：`websocket.jmx`
3. 根据需要修改用户自定义变量
4. 替换音频数据占位符为真实数据
5. 点击"运行"按钮执行测试
6. 查看"查看结果树"监听器中的测试结果

### 命令行运行

```bash
jmeter -n -t websocket.jmx -l results.jtl -e -o report/
```

参数说明：
- `-n`：非GUI模式
- `-t`：指定测试脚本
- `-l`：指定结果文件
- `-e`：生成测试报告
- `-o`：报告输出目录

## 扩展场景

### 1. 并发测试

修改线程组配置：
- 线程数：10（或更多）
- Ramp-Up时间：10秒
- 循环次数：5（或更多）

### 2. 压力测试

- 增加线程数到100+
- 延长测试时间
- 监控服务器性能指标

### 3. 稳定性测试

- 设置长时间运行（如1小时）
- 持续发送对话请求
- 监控内存泄漏和连接稳定性

### 4. 打断测试

在TTS播放过程中添加interrupt消息：

```xml
<eu.luminis.jmeter.wssampler.WebSocketSingleWriteSampler testname="发送interrupt消息">
  <stringProp name="payload">{
    "session_id": "${SESSION_ID}",
    "type": "interrupt"
  }</stringProp>
</eu.luminis.jmeter.wssampler.WebSocketSingleWriteSampler>
```

### 5. 错误场景测试

- 发送无效的JSON格式
- 发送错误的session_id
- 发送空音频数据
- 测试网络中断恢复

## 故障排查

### 常见问题

1. **连接失败**
   - 检查服务器地址和端口是否正确
   - 检查网络连接
   - 检查防火墙设置

2. **握手失败**
   - 检查hello消息格式是否正确
   - 检查必需字段是否完整
   - 查看服务器返回的错误信息

3. **音频识别失败**
   - 检查音频格式是否为Opus
   - 检查采样率是否为16000Hz
   - 检查音频数据是否有效

4. **TTS无响应**
   - 检查stt识别结果是否正确
   - 检查服务器TTS服务是否正常
   - 增加读取超时时间

### 调试技巧

1. 启用JMeter日志
2. 使用Debug Sampler查看变量值
3. 使用View Results Tree查看详细请求响应
4. 添加Response Assertion验证响应内容

## 性能指标

建议监控以下性能指标：

- 连接建立时间
- 握手响应时间
- 语音识别时间（stt）
- TTS响应时间
- 完整对话时间
- 成功率
- 错误率

## 附录

### WebSocket插件安装

1. 下载JMeter WebSocket插件：https://github.com/maciejzaleski/JMeter-WebSocket-Plugin
2. 将jar文件复制到JMeter的`lib/ext`目录
3. 重启JMeter

### Opus音频准备

使用以下工具准备Opus音频：

- FFmpeg：`ffmpeg -i input.wav -c:a libopus -ar 16000 -ac 1 -frame_duration 60 output.opus`
- Opus工具：`opusenc input.wav output.opus`

---

**文档版本**：v1.0
**最后更新**：2026-01-06

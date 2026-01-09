# WebSocket脚本编写参考文档

## 1. 文件基本信息与用途说明

### 1.1 文件概述

**文件名称**：WebSocket完整对话流程测试.jmx
**文件位置**：e:\AI测试用例\性能稳定测试\script\WebSocket完整对话流程测试.jmx
**JMeter版本**：5.6.3
**插件依赖**：eu.luminis.jmeter.wssampler（WebSocket Sampler插件）

### 1.2 主要用途

该脚本用于测试WebSocket完整对话流程，包括连接建立、握手、语音交互、TTS响应等核心功能。主要应用场景：

- WebSocket协议兼容性测试
- 语音识别（STT）功能测试
- 语音合成（TTS）功能测试
- 并发用户性能测试
- 端到端对话流程验证

### 1.3 技术栈与组件

| 技术/组件 | 版本/类型 | 用途 |
|-----------|-----------|------|
| JMeter | 5.6.3 | 测试框架 |
| WebSocket插件 | eu.luminis.jmeter.wssampler | WebSocket通信 |
| Groovy | 内置 | 脚本处理 |
| FFmpeg | 外部依赖 | 音频格式转换 |
| Opus编解码器 | concentus-1.0.2.jar | 音频压缩编码 |

## 2. 关键配置参数详解及使用规范

### 2.1 用户定义变量

| 参数名称 | 默认值 | 用途 | 使用规范 |
|----------|--------|------|----------|
| CONCURRENT_USERS | 1 | 并发用户数 | 根据测试需求调整，建议从1开始逐步增加 |
| SERVER_HOST | 118.196.28.154 | WebSocket服务器地址 | 替换为实际测试服务器地址 |
| SERVER_PORT | 8460 | WebSocket服务器端口 | 替换为实际测试服务器端口 |
| AUDIO_FILE_PATH | 你好啊.mp3 | 测试音频文件路径 | 确保文件存在，支持MP3格式 |

### 2.2 线程组配置

| 线程组 | 类型 | 线程数 | 循环次数 | 用途 |
|--------|------|--------|----------|------|
| 音频预处理 | SetupThreadGroup | 1 | 1 | 全局执行一次音频转换 |
| WebSocket对话线程组 | ThreadGroup | ${CONCURRENT_USERS} | 10 | 模拟并发用户进行WebSocket对话 |

### 2.3 WebSocket连接参数

| 参数名称 | 默认值 | 用途 | 使用规范 |
|----------|--------|------|----------|
| TLS | false | 是否使用TLS加密 | 根据服务器配置调整 |
| connectTimeout | 20000 | 连接超时时间（毫秒） | 建议设置为10-30秒 |
| readTimeout | 30000 | 读取超时时间（毫秒） | 根据业务场景调整，语音场景建议30-60秒 |
| binaryPayload | false/true | 是否发送二进制数据 | 文本消息设为false，音频数据设为true |
| createNewConnection | false | 是否创建新连接 | 后续请求必须设为false，复用已建立的连接 |

### 2.4 音频处理参数

| 参数名称 | 默认值 | 用途 | 使用规范 |
|----------|--------|------|----------|
| 采样率 | 16000 | 音频采样率 | 固定为16000Hz |
| 声道数 | 1 | 音频声道数 | 固定为单声道 |
| 帧大小 | 1920字节 | 音频帧大小 | 对应60ms音频数据 |
| Opus编码模式 | OPUS_APPLICATION_VOIP | 编码优化模式 | 语音场景固定为VOIP模式 |
| Opus比特率 | 32000 | 编码比特率 | 可根据网络情况调整 |
| 帧间隔 | 60ms | 音频帧发送间隔 | 固定为60ms，与帧大小对应 |

## 3. 测试流程步骤分解与逻辑说明

### 3.1 整体测试流程

```
测试计划设置
    ↓
音频预处理（全局执行一次）
    ↓
WebSocket对话线程组（并发执行）
    ↓
    声明变量
    ↓
    HTTP Header Manager配置
    ↓
    建立WebSocket连接
    ↓
    发送hello握手消息
    ↓
    接收初始化消息
    ↓
    接收hello响应
    ↓
    发送listen start消息
    ↓
    发送音频帧循环
    ↓
    发送listen stop消息
    ↓
    接收stt识别结果
    ↓
    接收TTS响应（可选）
    ↓
    关闭WebSocket连接
    ↓
结果收集与分析
```

### 3.2 详细步骤说明

#### 3.2.1 测试计划设置

- 定义全局变量：CONCURRENT_USERS、SERVER_HOST、SERVER_PORT、AUDIO_FILE_PATH
- 配置类路径：添加D:\apache-jmeter-5.6.3\lib\concentus-1.0.2.jar用于Opus编码

#### 3.2.2 音频预处理

使用SetupThreadGroup全局执行一次，完成以下操作：

1. 检查音频文件是否存在
2. 使用FFmpeg将MP3转换为PCM格式（16kHz，单声道，16位）
3. 计算音频分块数量
4. 将预处理结果存储到全局变量中

#### 3.2.3 WebSocket对话线程组

每个线程执行完整的WebSocket对话流程：

1. **声明变量**：生成唯一的DEVICE_ID和USER_ID
2. **HTTP Header Manager配置**：设置Protocol-Version、Device-Id、Client-Id等头部
3. **建立WebSocket连接**：使用OpenWebSocketSampler连接到服务器
4. **发送hello握手消息**：初始化WebSocket会话
5. **接收初始化消息**：处理服务器的初始化响应
6. **接收hello响应**：验证握手结果，提取session_id
7. **发送listen start消息**：通知服务器开始监听语音
8. **发送音频帧循环**：循环发送Opus编码的音频帧
9. **发送listen stop消息**：通知服务器停止监听语音
10. **接收stt识别结果**：获取语音识别结果
11. **接收TTS响应**：处理文本转语音响应（可选）
12. **关闭WebSocket连接**：正常关闭连接

## 4. 请求/响应数据格式标准

### 4.1 WebSocket连接请求

**URL格式**：ws://${SERVER_HOST}:${SERVER_PORT}/?device_id=${DEVICE_ID}&user_id=${USER_ID}

**请求方法**：GET

**头部信息**：
- Protocol-Version: 1
- Device-Id: ${DEVICE_ID}
- Client-Id: ${USER_ID}

### 4.2 消息类型与格式

#### 4.2.1 Hello握手消息

**发送格式**：

```json
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
  "device_id": "${DEVICE_ID}",
  "device_name": "JMeter测试设备",
  "user_id": "${USER_ID}",
  "trace_id": "jmeter_test_${__time(,)}",
  "device_mac": "${DEVICE_ID}",
  "client_id": "${DEVICE_ID}",
  "client_ip": "127.0.0.1",
  "client_info": {
    "os_type": "Android",
    "os_version": "14",
    "app_version": "1.0.0",
    "network_type": "wifi",
    "network_provider": "TEST",
    "timezone": "Asia/Shanghai",
    "country_code": "CN",
    "battery_level": 100,
    "is_charging": true
  }
}
```

**接收格式**：

```json
{
  "type": "hello",
  "session_id": "unique-session-id",
  "version": 1
}
```

#### 4.2.2 Listen消息

**Start格式**：

```json
{
  "session_id": "${SESSION_ID}",
  "type": "listen",
  "state": "start",
  "mode": "auto"
}
```

**Stop格式**：

```json
{
  "type": "listen",
  "state": "stop",
  "session_id": "${SESSION_ID}"
}
```

**Detect格式**（手动模式）：

```json
{
  "type": "listen",
  "state": "detect",
  "mode": "manual",
  "text": "测试文本",
  "session_id": "${SESSION_ID}"
}
```

#### 4.2.3 STT响应格式

```json
{
  "type": "stt",
  "text": "识别到的文本",
  "session_id": "${SESSION_ID}",
  "timestamp": 1234567890
}
```

#### 4.2.4 TTS消息

**Start格式**：

```json
{
  "type": "tts",
  "state": "start",
  "session_id": "${SESSION_ID}"
}
```

**Stop格式**：

```json
{
  "type": "tts",
  "state": "stop",
  "session_id": "${SESSION_ID}"
}
```

### 4.3 响应处理机制

| 处理方式 | 组件 | 用途 |
|----------|------|------|
| 响应读取 | SingleReadWebSocketSampler | 读取WebSocket响应 |
| 内容验证 | JSONPathAssertion | 验证响应JSON结构和内容 |
| 数据提取 | JSONPostProcessor | 提取关键数据（如session_id） |
| 复杂逻辑处理 | JSR223PostProcessor | 处理条件判断、状态管理等 |
| 响应时间验证 | DurationAssertion | 验证响应时间是否符合要求 |

## 5. 常见场景处理方案

### 5.1 连接管理

#### 5.1.1 正常连接建立

- 使用OpenWebSocketSampler建立连接
- 设置合理的连接超时（建议20秒）
- 验证连接成功后再进行后续操作

#### 5.1.2 连接异常处理

- 添加DurationAssertion验证连接时间
- 设置线程组的on_sample_error为continue，确保单个连接失败不影响其他测试
- 在JSR223Sampler中添加异常捕获逻辑

### 5.2 音频处理

#### 5.2.1 音频格式转换

- 使用FFmpeg将MP3转换为PCM格式
- 确保转换后的PCM参数正确（16kHz，单声道，16位）
- 处理文件不存在的异常情况

#### 5.2.2 音频帧发送

- 使用LoopController控制发送次数
- 固定60ms的帧间隔
- 到达文件末尾时发送静音帧
- 使用props存储线程级偏移量，确保状态保持

### 5.3 响应处理

#### 5.3.1 异步响应处理

- 使用SingleReadWebSocketSampler读取响应
- 设置合理的读取超时（根据业务场景调整）
- 对于可选响应，设置optional=true

#### 5.3.2 TTS响应循环处理

- 使用WhileController循环接收TTS响应
- 设置TTS_STOP_RECEIVED标志，收到stop消息后退出循环
- 处理二进制音频数据和文本消息的区分

## 6. 性能优化建议

### 6.1 脚本设计优化

1. **使用SetupThreadGroup**：将音频预处理等全局操作放在SetupThreadGroup中，只执行一次
2. **脚本缓存**：在JSR223Sampler中设置cacheKey=true，提高脚本执行效率
3. **编码器单例模式**：每个线程只创建一个OpusEncoder实例，避免重复创建
4. **线程状态管理**：使用props存储线程级状态，避免线程间干扰

### 6.2 资源优化

1. **音频文件处理**：
   - 预先转换音频文件，避免运行时转换
   - 使用合适大小的测试音频（建议5-10秒）
   - 清理临时文件

2. **连接管理**：
   - 复用WebSocket连接，避免频繁创建和关闭
   - 设置合理的连接超时和读取超时
   - 关闭不必要的连接

### 6.3 性能测试参数优化

1. **并发用户数**：
   - 从1开始逐步增加，找到系统瓶颈
   - 根据服务器配置和网络情况调整

2. **线程组配置**：
   - 合理设置ramp_time（建议1-5秒）
   - 调整循环次数，平衡测试时长和结果可靠性

3. **超时设置**：
   - 连接超时：建议10-30秒
   - 读取超时：根据业务场景调整，语音场景建议30-60秒
   - 响应时间断言：根据性能要求设置合理阈值

### 6.4 结果收集优化

1. **ResultCollector配置**：
   - 只保存必要的结果字段
   - 关闭responseData和samplerData的保存，减少磁盘IO
   - 合理设置断言结果保存

2. **报告生成**：
   - 使用命令行生成报告，避免GUI模式的性能开销
   - 定期清理报告文件，避免磁盘空间不足

## 7. 脚本编写规范

### 7.1 命名规范

- 采样器名称：使用数字前缀+描述，如"1. 建立WebSocket连接"
- 变量名称：使用大写字母+下划线，如DEVICE_ID、SESSION_ID
- 文件名称：使用清晰的描述性名称，如"WebSocket_连接管理测试.jmx"

### 7.2 结构规范

- 每个功能模块使用TransactionController分组
- 使用HeaderManager统一管理HTTP头部
- 关键步骤添加断言和响应时间验证
- 使用注释说明复杂逻辑

### 7.3 错误处理规范

- 每个关键步骤添加适当的断言
- 设置合理的超时时间
- 添加异常捕获和日志记录
- 使用ResultCollector便于调试

## 8. 脚本维护与更新

### 8.1 版本控制

- 使用Git等版本控制工具管理脚本
- 每次修改添加清晰的提交信息
- 定期备份脚本文件

### 8.2 更新流程

1. 分析需求变化
2. 修改脚本相关部分
3. 执行测试验证修改
4. 更新文档
5. 提交版本控制

### 8.3 常见问题排查

| 问题 | 可能原因 | 解决方案 |
|------|----------|----------|
| WebSocket连接失败 | 服务器地址/端口错误 | 检查SERVER_HOST和SERVER_PORT配置 |
| 音频转换失败 | FFmpeg未安装或路径错误 | 确保FFmpeg已正确安装并添加到环境变量 |
| 响应时间过长 | 服务器性能问题或网络延迟 | 检查服务器负载和网络状况，调整超时设置 |
| 线程间状态混乱 | 变量作用域设置错误 | 使用props存储线程级状态，避免线程间干扰 |
| 断言失败 | 响应格式变化或预期结果错误 | 更新断言规则，确保与服务器响应匹配 |

## 9. 附录

### 9.1 插件安装

1. 下载WebSocket Sampler插件：https://github.com/peterdoornbosch/jmeter-websocket-samplers
2. 将jar文件复制到JMeter的lib/ext目录
3. 重启JMeter

### 9.2 依赖配置

- FFmpeg：https://ffmpeg.org/download.html
- Opus编解码器：concentus-1.0.2.jar

### 9.3 常用命令

1. 执行脚本：
   ```
   jmeter -n -t WebSocket完整对话流程测试.jmx -l result.jtl
   ```

2. 生成报告：
   ```
   jmeter -g result.jtl -o report
   ```

3. 清理旧报告：
   ```powershell
   Remove-Item -Path "e:\AI测试用例\性能稳定测试\script\report" -Recurse -Force -ErrorAction SilentlyContinue
   Remove-Item -Path "e:\AI测试用例\性能稳定测试\script\result.jtl" -Force -ErrorAction SilentlyContinue
   ```

### 9.4 相关文档

- JMeter官方文档：https://jmeter.apache.org/usermanual/index.html
- WebSocket Sampler插件文档：https://github.com/peterdoornbosch/jmeter-websocket-samplers/wiki
- Opus编码规范：https://opus-codec.org/docs/

---

**文档创建时间**：2026-01-09
**文档版本**：1.0
**更新记录**：
- 2026-01-09：初始版本创建，基于WebSocket完整对话流程测试.jmx文件分析
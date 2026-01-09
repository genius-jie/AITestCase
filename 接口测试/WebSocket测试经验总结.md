# WebSocket测试经验总结

## 1. 核心概念与技术栈

### 1.1 WebSocket基础
- **定义**：WebSocket是一种全双工通信协议，允许客户端与服务器之间建立持久连接，实现双向实时数据传输
- **优势**：低延迟、减少HTTP握手开销、支持二进制数据传输
- **应用场景**：实时通信、音视频流、实时数据推送

### 1.2 WebSocket ASR测试特有概念
- **ASR**：自动语音识别（Automatic Speech Recognition）
- **音频帧**：将音频数据分割成固定时长的片段进行传输
- **Opus编码**：一种高效的音频编码格式，适用于实时通信
- **PCM**：脉冲编码调制，原始音频数据格式

### 1.3 测试工具栈
- **JMeter**：用于性能测试和自动化测试
- **WebSocket插件**：eu.luminis.jmeter.wssampler（功能更完善，支持连接复用）
- **FFmpeg**：用于音频格式转换
- **Concentus库**：用于Opus音频编码解码

## 2. 测试流程设计

### 2.1 最小可用测试流程
```
WebSocket连接 → 发送hello消息 → 发送listen start → 发送音频帧 → 接收stt结果 → 接收TTS消息 → 关闭连接
```

### 2.2 关键测试点设计
1. **连接建立**：验证WebSocket连接的建立和认证
2. **消息交互**：验证各种消息类型的正确处理
3. **音频传输**：验证音频数据的正确编码、传输和解码
4. **实时性**：验证端到端延迟是否符合要求
5. **稳定性**：验证长时间运行时的稳定性
6. **异常处理**：验证各种异常情况下的系统行为

### 2.3 音频参数设计
| 参数 | 推荐值 | 说明 |
|------|--------|------|
| 格式 | PCM/Opus | PCM更易于调试，Opus性能更好 |
| 采样率 | 16000Hz | 语音识别的标准采样率 |
| 通道数 | 1 | 单声道，减少数据量 |
| 帧时长 | 60ms | 平衡实时性和传输效率 |
| 帧大小 | 1920字节 | 16kHz/16bit/mono 60ms的PCM数据大小 |

## 3. JMeter WebSocket测试实践

### 3.1 脚本结构设计

#### 3.1.1 线程组设计
- **SetupThreadGroup**：用于音频预处理，全局执行一次
- **普通ThreadGroup**：用于模拟并发用户的WebSocket对话

#### 3.1.2 核心组件
```xml
<!-- 建立WebSocket连接 -->
<eu.luminis.jmeter.wssampler.OpenWebSocketSampler>
  <!-- 配置服务器地址、端口、路径等 -->
</eu.luminis.jmeter.wssampler.OpenWebSocketSampler>

<!-- 发送文本消息 -->
<eu.luminis.jmeter.wssampler.SingleWriteWebSocketSampler>
  <!-- 配置消息内容、是否二进制等 -->
</eu.luminis.jmeter.wssampler.SingleWriteWebSocketSampler>

<!-- 接收消息 -->
<eu.luminis.jmeter.wssampler.SingleReadWebSocketSampler>
  <!-- 配置超时时间、是否可选等 -->
</eu.luminis.jmeter.wssampler.SingleReadWebSocketSampler>
```

### 3.2 音频处理实现

#### 3.2.1 音频预处理（Groovy脚本）
```groovy
// 将MP3转换为PCM格式
String audioPath = vars.get("AUDIO_FILE_PATH")
File tempPcmFile = File.createTempFile("temp_pcm_", ".raw")

def pb = new ProcessBuilder("ffmpeg", "-y", "-i", audioPath,
        "-f", "s16le", "-ar", "16000", "-ac", "1",
        tempPcmFile.getAbsolutePath())
// 执行转换并验证结果
```

#### 3.2.2 音频帧发送
```groovy
// 读取PCM文件并转换为Opus帧
RandomAccessFile raf = new RandomAccessFile(path, "r")
byte[] pcmBuffer = new byte[frameSize]
raf.readFully(pcmBuffer)

// PCM转Opus编码
OpusEncoder encoder = vars.getObject("OPUS_ENCODER")
byte[] opusBuffer = new byte[1275] // Max payload size
int len = encoder.encode(shortBuffer, 0, 960, opusBuffer, 0, opusBuffer.length)

// 转换为十六进制字符串发送
StringBuilder hex = new StringBuilder()
for (byte b : finalOpus) {
    hex.append(String.format("%02x", b))
}
vars.put("FRAME_HEX", hex.toString())
```

### 3.3 并行处理设计

#### 3.3.1 正确的并行控制器配置
```xml
<com.blazemeter.jmeter.controller.ParallelSampler guiclass="com.blazemeter.jmeter.controller.ParallelControllerGui" testclass="com.blazemeter.jmeter.controller.ParallelSampler" testname="bzm - Parallel Controller">
  <intProp name="MAX_THREAD_NUMBER">6</intProp>
  <boolProp name="PARENT_SAMPLE">false</boolProp>
  <boolProp name="LIMIT_MAX_THREAD_NUMBER">false</boolProp>
</com.blazemeter.jmeter.controller.ParallelSampler>
```

#### 3.3.2 连接共享问题解决
- 问题：并行线程无法访问父线程的WebSocket连接
- 解决方案：确保所有采样器使用同一个连接（`createNewConnection=false`）
- 注意：避免在并行控制器中创建新连接

## 4. 常见问题及解决方案

### 4.1 连接相关问题
| 问题 | 原因 | 解决方案 |
|------|------|----------|
| CannotResolveClassException | 插件版本不兼容 | 使用正确的插件类名，如`eu.luminis.jmeter.wssampler`替代旧版`kg.apc` |
| 连接超时 | 网络问题或服务器未响应 | 检查网络连接，增加超时时间，验证服务器状态 |
| 并行线程无法获取连接 | 连接未正确共享 | 确保所有采样器设置`createNewConnection=false` |

### 4.2 音频相关问题
| 问题 | 原因 | 解决方案 |
|------|------|----------|
| 无STT返回 | 未发送listen start或音频格式错误 | 检查消息顺序，验证音频参数配置 |
| 识别乱码 | 音频格式不匹配 | 确保PCM是16kHz/16bit/mono，Opus是裸帧 |
| 服务端报Opus解码失败 | 发送了Ogg/WebM封装的Opus | 确保发送裸Opus帧，无容器封装 |
| 识别很慢或丢字 | 推流速度过快或帧大小错误 | 按60ms间隔推流，确保帧大小正确（1920字节） |

### 4.3 脚本设计问题
| 问题 | 原因 | 解决方案 |
|------|------|----------|
| 脚本无法打开 | JMX格式错误 | 验证XML格式，使用正确的插件类名 |
| 音频文件未找到 | 路径配置错误 | 使用绝对路径，验证文件存在性 |
| 线程状态丢失 | 变量作用域问题 | 使用props存储跨线程组变量，vars存储线程内变量 |

## 5. 测试技巧与最佳实践

### 5.1 测试设计技巧
- **分层测试**：从单用户功能测试开始，逐步扩展到多用户性能测试
- **参数化**：使用变量配置服务器地址、音频文件等，提高脚本可维护性
- **断言设计**：添加响应时间断言、内容断言，确保测试结果准确性
- **日志记录**：适当添加日志，便于调试和分析问题

### 5.2 性能测试注意事项
- **线程数设计**：根据服务器承载能力设计合理的并发线程数
- **Ramp-up时间**：逐渐增加线程数，避免瞬间压力过大
- **持续时间**：长时间运行测试，验证系统稳定性
- **资源监控**：同时监控服务器CPU、内存、网络等资源使用情况

### 5.3 调试技巧
- **查看结果树**：使用JMeter的查看结果树组件查看详细的请求和响应
- **日志级别调整**：调整JMeter日志级别，获取更详细的调试信息
- **分步调试**：逐步执行测试步骤，定位问题所在
- **使用Wireshark**：捕获WebSocket流量，分析数据传输情况

## 6. 常见问题及回答要点

### 6.1 基础概念
**问题**：WebSocket和HTTP有什么区别？
**回答要点**：
- HTTP是单向通信，WebSocket是全双工通信
- HTTP需要每次请求建立连接，WebSocket建立持久连接
- HTTP有头部开销，WebSocket头部开销小
- HTTP适用于请求-响应模式，WebSocket适用于实时通信

### 6.2 测试设计
**问题**：如何设计WebSocket ASR测试用例？
**回答要点**：
- 覆盖基本流程：连接→hello→listen→音频→stt→关闭
- 测试不同音频格式和参数
- 测试异常情况：断网、超时、格式错误
- 测试性能：并发用户数、延迟、稳定性

### 6.3 技术实现
**问题**：在JMeter中如何实现WebSocket并行处理？
**回答要点**：
- 使用bzm - Parallel Controller组件
- 确保连接共享（`createNewConnection=false`）
- 设计合理的线程组结构
- 注意变量作用域和状态管理

### 6.4 问题排查
**问题**：WebSocket测试中没有收到预期的STT结果，如何排查？
**回答要点**：
- 检查是否发送了listen start消息
- 验证音频格式和参数是否正确
- 检查WebSocket连接是否正常
- 查看服务器日志，确认是否收到音频数据
- 检查音频推流速度是否符合要求

## 7. 测试能力提升建议

### 7.1 技术栈扩展
- 学习WebSocket协议规范（RFC 6455）
- 掌握音频编码解码原理
- 学习使用其他测试工具，如Postman、WebSocket King等
- 了解性能测试的基本原理和方法

### 7.2 实践建议
- 参与实际项目的WebSocket测试
- 搭建本地测试环境，进行各种场景测试
- 分析开源项目的WebSocket实现
- 编写测试脚本模板，提高测试效率

### 7.3 持续学习
- 关注WebSocket技术发展动态
- 学习实时通信领域的新技术
- 参与测试社区交流，分享经验
- 阅读相关书籍和博客，提升理论水平

## 8. 总结

WebSocket测试是一项综合性的技术工作，需要掌握WebSocket协议、音频处理、测试工具使用等多方面知识。通过系统化的测试流程设计、合理的脚本结构、有效的问题排查方法，可以提高WebSocket测试的效率和质量。

这份经验总结涵盖了WebSocket测试的核心概念、测试流程设计、JMeter实践、常见问题解决方案，希望能帮助测试人员提升WebSocket测试能力

## 9. 参考资料

- [PatchX AI Server - Java WebSocket ASR 测试流程](e:\AI测试用例\性能稳定测试\PatchX AI Server - Java WebSocket ASR 测试流程 (1).md)
- [WebSocket完整对话流程测试.jmx](e:\AI测试用例\性能稳定测试\script\WebSocket完整对话流程测试.jmx)
- [JMeter WebSocket Sampler插件文档](https://github.com/PeterDoornbosch/jmeter-websocket-samplers)
- [WebSocket协议规范（RFC 6455）](https://datatracker.ietf.org/doc/html/rfc6455)

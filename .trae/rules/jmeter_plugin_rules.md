# JMeter 脚本与插件规范

## 1. 插件兼容性原则

### 1.1 插件识别与匹配
在编写或修改 JMX 脚本时，必须首先确认目标环境安装的插件版本。
- **Maciej Zaleski 插件** (`kg.apc.jmeter.samplers`): 早期常用，功能基础。
- **Peter Doornbosch 插件** (`eu.luminis.jmeter.wssampler`): 功能更完善，支持复用连接、读写分离等。

**规则**：
- 严禁混用不同插件家族的组件，除非经过严格验证。
- 必须根据用户环境（如报错信息 `CannotResolveClassException`）切换正确的插件实现。

### 1.2 WebSocket 插件映射表

| 功能 | Maciej Zaleski (`kg.apc`) | Peter Doornbosch (`eu.luminis`) |
| :--- | :--- | :--- |
| **建立连接** | `WebSocketOpenSampler` | `OpenWebSocketSampler` |
| **发送消息** | `WebSocketSampler` (带 Payload) | `SingleWriteWebSocketSampler` |
| **接收消息** | `WebSocketSampler` (无 Payload) | `SingleReadWebSocketSampler` |
| **关闭连接** | `WebSocketCloseSampler` | `CloseWebSocketSampler` |
| **Ping/Pong** | `WebSocketPingSampler` | `PingPongSampler` |

## 2. JMX 脚本生成规范

### 2.1 连接管理
- **复用连接**：在 Peter Doornbosch 插件中，后续读写操作必须设置 `createNewConnection=false`，确保使用由 `OpenWebSocketSampler` 建立的会话。
- **超时设置**：明确区分 `connectTimeout` (连接超时) 和 `readTimeout` (读取超时)，与其业务场景匹配。

### 2.2 数据读写
- **二进制 vs 文本**：明确区分 `binaryPayload` 属性。
    - JSON/Text 消息：`binaryPayload=false`
    - 音频/二进制流：`binaryPayload=true`
- **读写分离**：不要试图在一个 Sampler 中同时完成复杂的"发-收"逻辑，建议拆分为 "Single Write" + "Single Read" 以便更好控制断言和调试。

### 2.3 异常处理
- 必须包含 `ResultCollector` 以便调试。
- 关键步骤应添加 `DurationAssertion` (响应时间断言) 和 `JSONPathAssertion` (内容断言)。

### 2.4 清理规则  
每次执行 JMeter 脚本前，必须清理上一次生成的报告和结果文件，避免旧数据干扰统计。  
- 使用 PowerShell 命令：Remove-Item -Path "e:\AI测试用例\性能稳定测试\script\report" -Recurse -Force -ErrorAction SilentlyContinue; Remove-Item -Path "e:\AI测试用例\性能稳定测试\script\result.jtl" -Force -ErrorAction SilentlyContinue; Write-Host "清理完成"

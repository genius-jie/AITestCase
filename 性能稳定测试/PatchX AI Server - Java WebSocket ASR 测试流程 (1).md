PatchX AI Server - Java WebSocket ASR 测试流程
本文档给出一个完整可跑通的 Java 测试流程：从握手连接 → hello → listen → 发送二进制音频 → 收到 stt。
重要结论（和服务端实现一致）：
设备上行二进制音频 只能发送裸 Opus 帧或裸 PCM 数据。
不要发送带自定义二进制头的协议包（Binary Protocol v2/v3）或 Ogg/WebM 容器。
推荐使用 PCM 16kHz / 16-bit / 单声道 / 60ms 帧，最容易验证。

1. 最小可用流程（概览）
WebSocket 连接（URL 建议带 device_id 参数）
发送 hello（带 audio_params）
发送 listen start（mode=auto）
以二进制消息发送音频帧（每 60ms 一帧）
（可选）发送 listen stop
接收服务端下发的 stt JSON 消息

2. 音频参数与帧大小
推荐参数：
format: pcm
sample_rate: 16000
channels: 1
frame_duration: 60
PCM 帧大小计算：

| Plain Text
16000 samples/s * 2 bytes * 0.06 s = 1920 bytes |
| --- |

所以每帧 1920 字节。
如果你使用 WAV 文件作为输入：
要求 WAV 本身是 16kHz / 16-bit / mono
发送前需跳过 44 字节 WAV 头（仅发送数据区）

3. Java 测试示例（PCM 方案）
3.1 示例代码（Java 11+）

| Java
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.WebSocket;
import java.nio.ByteBuffer;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.time.Duration;
import java.util.UUID;
import java.util.concurrent.CompletableFuture;

public class PatchxWsAsrTest {
    public static void main(String[] args) throws Exception {
        String host = "ws://127.0.0.1:8460"; // 替换为你的服务地址
        String deviceId = "test-device-001";
        String userId = "test-user-001";
        String traceId = UUID.randomUUID().toString();
        String wsUrl = host + "/?device_id=" + deviceId;

        HttpClient client = HttpClient.newHttpClient();
        WebSocket ws = client.newWebSocketBuilder()
                .connectTimeout(Duration.ofSeconds(10))
                // 协议头（可选但建议）
                .header("Protocol-Version", "1")
                .header("Device-Id", deviceId)
                .header("Client-Id", UUID.randomUUID().toString())
                .buildAsync(URI.create(wsUrl), new SimpleListener())
                .join();

        // 1) hello
        String hello = "{\n" +
                "  \"type\": \"hello\",\n" +
                "  \"version\": 1,\n" +
                "  \"transport\": \"websocket\",\n" +
                "  \"audio_params\": {\n" +
                "    \"format\": \"pcm\",\n" +
                "    \"sample_rate\": 16000,\n" +
                "    \"channels\": 1,\n" +
                "    \"frame_duration\": 60\n" +
                "  },\n" +
                "  \"device_id\": \"" + deviceId + "\",\n" +
                "  \"user_id\": \"" + userId + "\",\n" +
                "  \"trace_id\": \"" + traceId + "\"\n" +
                "}";
        ws.sendText(hello, true).join();

        // 2) listen start
        String listenStart = "{\n" +
                "  \"type\": \"listen\",\n" +
                "  \"state\": \"start\",\n" +
                "  \"mode\": \"auto\",\n" +
                "  \"session_id\": \"" + traceId + "\"\n" +
                "}";
        ws.sendText(listenStart, true).join();

        // 3) 发送 PCM 音频帧（示例：从 16kHz/16bit/mono WAV 读取）
        Path wavFile = Path.of("/path/to/your-16k-mono.wav");
        byte[] wavBytes = Files.readAllBytes(wavFile);

        int wavHeader = 44; // WAV 标准头长度
        int frameSize = 1920; // 60ms * 16kHz * 2 bytes
        int offset = wavHeader;
        while (offset < wavBytes.length) {
            int end = Math.min(offset + frameSize, wavBytes.length);
            byte[] frame = new byte[end - offset];
            System.arraycopy(wavBytes, offset, frame, 0, frame.length);
            ws.sendBinary(ByteBuffer.wrap(frame), true).join();
            offset = end;
            Thread.sleep(60); // 模拟实时 60ms/帧
        }

        // 4) listen stop（manual 模式必需，auto 模式可选）
        String listenStop = "{\n" +
                "  \"type\": \"listen\",\n" +
                "  \"state\": \"stop\",\n" +
                "  \"session_id\": \"" + traceId + "\"\n" +
                "}";
        ws.sendText(listenStop, true).join();

        // 等待一会儿接收 stt
        Thread.sleep(3000);
        ws.sendClose(WebSocket.NORMAL_CLOSURE, "done").join();
    }

    // 简单接收器：打印所有服务端文本消息（包括 stt）
    static class SimpleListener implements WebSocket.Listener {
        @Override
        public void onOpen(WebSocket webSocket) {
            System.out.println("[WS] open");
            webSocket.request(1);
        }

        @Override
        public CompletionStage<?> onText(WebSocket webSocket, CharSequence data, boolean last) {
            System.out.println("[WS] text: " + data);
            webSocket.request(1);
            return CompletableFuture.completedFuture(null);
        }

        @Override
        public CompletionStage<?> onBinary(WebSocket webSocket, ByteBuffer data, boolean last) {
            System.out.println("[WS] binary len=" + data.remaining());
            webSocket.request(1);
            return CompletableFuture.completedFuture(null);
        }

        @Override
        public void onError(WebSocket webSocket, Throwable error) {
            System.err.println("[WS] error: " + error.getMessage());
        }
    }
} |
| --- |

3.2 运行说明
先把 /path/to/your-16k-mono.wav 换成真实文件路径。
WAV 必须是 16kHz / 16bit / mono。
控制台会打印服务端返回的 stt JSON，例如：

| JSON
{"type":"stt","text":"你好"} |
| --- |


4. 文本消息测试（不走音频）
本地页面 dev/test_page_split.html 的“文本消息”按钮，实际是发送 listen 消息：

| JSON
{
  "type": "listen",
  "mode": "manual",
  "state": "detect",
  "text": "用户输入的文本"
} |
| --- |

服务端会把 state=detect 的 text 当作用户发言，直接进入对话流程（等价于 ASR 结果）。
4.1 Java 发送文本示例

| Java
String textMessage = "{\n" +
        "  \\\"type\\\": \\\"listen\\\",\\n" +
        "  \\\"state\\\": \\\"detect\\\",\\n" +
        "  \\\"mode\\\": \\\"manual\\\",\\n" +
        "  \\\"text\\\": \\\"你好\\\",\\n" +
        "  \\\"session_id\\\": \\\"" + traceId + "\\\"\\n" +
        "}";
ws.sendText(textMessage, true).join(); |
| --- |

说明：session_id 在协议中推荐携带；本地页面代码里未强制填写也能工作。
如果开启“聆听模式”，同样是 listen 消息，但服务端会先累积文本，停止时再统一处理。

5. Opus 方案（可选）
如果你已经有 裸 Opus 帧（不是 Ogg/WebM），可以在 hello 中设置：

| JSON
"audio_params": {"format": "opus", "sample_rate": 16000, "channels": 1, "frame_duration": 60} |
| --- |

然后按帧发送二进制消息。注意：不要发送 Ogg/WebM 容器。

6. 常见问题排查
没有 stt 返回
是否发送了 listen start？
是否发送了音频？
manual 模式是否发送了 listen stop？
是否在 hello 返回之前就开始推流？（建议等 hello 响应后再推）
是否过早关闭 WebSocket，导致 STT 还没回就断开？
识别乱码或无结果
PCM 是否 16kHz / 16bit / mono？
WAV 是否跳过了 44 字节头？
Opus 是否是裸帧而非容器？
audio_params.format 是否与实际发送数据一致（pcm/opus）？
服务端报 Opus 解码失败
可能是发送了 Ogg/WebM 封装。
或 Opus 编码参数与 16kHz 不一致。
服务端完全不进 ASR
是否把 PCM 转成了 hex/base64 文本发送？（必须发 Binary）
WebSocket 客户端是否只支持文本消息？（需要 Binary 支持）
是否误发了 BinaryProtocol v2/v3 带头的数据？（服务端当前只认“裸帧”）
识别很慢或丢字
是否在很短时间内“突发推完”，没有按 60ms 节奏推流？
帧大小是否不对（16kHz/16bit/mono 60ms = 1920 bytes）？
文本模式与音频混用异常
文本测试应使用 listen state=detect（不需要音频）
音频测试应使用 listen state=start + 二进制音频（必要时 stop）

7. 重要注意事项（音频必看）
必须发送二进制帧（opcode=2）
不要把 PCM 转成 hex 或 base64。
直接发送原始 byte[] / ByteBuffer。
audio_params.format 必须与实际数据一致
发 PCM 就设 format=pcm
发 Opus 就设 format=opus
流式发送：按 60ms 帧持续推送
1920 字节/帧（16kHz/16bit/mono）
建议 sleep 60ms 模拟实时
手动模式必须发送 stop
mode=manual 仅 detect 文本也要 stop
mode=auto 可不发 stop
不要发送 BinaryProtocol v2/v3 头
服务端当前只识别“裸帧”

8. JMeter / Groovy PCM 推流示例
以下示例适用于 JMeter 的 WebSocket 发送场景（Groovy 伪代码）。
关键点：不要 hex，直接发送二进制帧。
8.1 预处理（MP3 → PCM）

| Groovy
import java.nio.file.Files
import java.nio.file.Paths
import java.io.File

String audioPath = vars.get("AUDIO_FILE_PATH")
File audioFile = new File(audioPath)
if (!audioFile.exists()) {
    SampleResult.setSuccessful(false)
    SampleResult.setResponseMessage("未找到音频文件: " + audioPath)
    SampleResult.setStopThread(true)
    return
}

File tempPcmFile = File.createTempFile("temp_pcm_", ".raw")
tempPcmFile.deleteOnExit()
String ffmpegPath = "ffmpeg"

def pb = new ProcessBuilder(ffmpegPath, "-y", "-i", audioPath,
        "-f", "s16le", "-ar", "16000", "-ac", "1",
        tempPcmFile.getAbsolutePath())
pb.redirectErrorStream(true)
def process = pb.start()
process.waitFor()

if (process.exitValue() != 0) {
    SampleResult.setSuccessful(false)
    SampleResult.setResponseMessage("FFmpeg转换失败")
    return
}

long fileSize = tempPcmFile.length()
int frameSize = 1920
int chunks = (int) Math.ceil((double) fileSize / frameSize)

vars.put("PCM_FILE_PATH", tempPcmFile.getAbsolutePath())
vars.put("CHUNK_COUNT", String.valueOf(chunks))
vars.put("CURRENT_OFFSET", "0")
log.info("已准备好PCM音频。大小：" + fileSize + "，块数：" + chunks) |
| --- |

8.2 每帧发送（必须是二进制）

| Groovy
import java.io.RandomAccessFile

String path = vars.get("PCM_FILE_PATH")
long offset = Long.parseLong(vars.get("CURRENT_OFFSET"))
int frameSize = 1920

RandomAccessFile raf = new RandomAccessFile(path, "r")
if (offset < raf.length()) {
    raf.seek(offset)
    int bytesToRead = (int) Math.min(frameSize, raf.length() - offset)
    byte[] buffer = new byte[bytesToRead]
    raf.readFully(buffer)

    // 关键：这里必须发送二进制 buffer，不要转 hex/base64
    // 具体发送方法取决于你使用的 WebSocket 插件/采样器
    // 例：websocketClient.sendBinary(buffer)

    vars.put("CURRENT_OFFSET", String.valueOf(offset + bytesToRead))
}
raf.close() |
| --- |

如果你当前 WebSocket 采样器只支持“文本消息”，请换支持 Binary 的插件或客户端。
发送 hex 字符串会被服务端当作普通文本，ASR 不会处理。

9. 推荐测试顺序
用 PCM 方案跑通（最稳定）
再切到 Opus 方案（性能更好）

如需我帮你把这段 Java 示例改成你现在脚本的实际结构（比如已有 ws 框架 / 已有 Opus 编码器），把你当前脚本结构贴一下即可。
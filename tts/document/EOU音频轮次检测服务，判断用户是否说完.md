# Smart Turn API 接口文档

## 服务信息

- **服务名称**: Smart Turn Detection API
- **版本**: 1.0.0
- **端口**: 8006
- **基础URL**: `http://localhost:8006`
- **API 文档**: 
  - Swagger UI: `http://localhost:8006/docs`
  - ReDoc: `http://localhost:8006/redoc`

## 关于 UploadFile

`UploadFile` 是 FastAPI 的文件上传类型，使用 **multipart/form-data** 格式提交。

### 请求格式

- **Content-Type**: `multipart/form-data`
- **字段名**: `audio_file`（在代码中定义）
- **支持格式**: wav, mp3, flac, ogg 等常见音频格式

### 使用方式

#### 1. 使用 curl 命令

```bash
curl -X POST "http://localhost:8006/detect" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "audio_file=@/path/to/your/audio.wav"
```

#### 2. 使用 Python requests

```python
import requests

url = "http://localhost:8006/detect"

# 方式1: 直接传文件路径
with open("audio.wav", "rb") as f:
    files = {"audio_file": ("audio.wav", f, "audio/wav")}
    response = requests.post(url, files=files)
    print(response.json())

# 方式2: 传文件对象
files = {"audio_file": open("audio.wav", "rb")}
response = requests.post(url, files=files)
print(response.json())
```

#### 3. 使用 JavaScript/TypeScript (FormData)

```javascript
const formData = new FormData();
const fileInput = document.querySelector('input[type="file"]');
formData.append('audio_file', fileInput.files[0]);

fetch('http://localhost:8006/detect', {
  method: 'POST',
  body: formData
})
.then(response => response.json())
.then(data => console.log(data));
```

#### 4. 使用 Postman/Apifox

1. 选择请求方法: `POST`
2. URL: `http://localhost:8006/detect`
3. Body 标签页 → 选择 `form-data`
4. Key: `audio_file`，类型选择 `File`
5. Value: 点击选择文件，选择你的音频文件
6. 点击 Send

## API 接口列表

### 1. 根路径

**GET** `/`

获取服务基本信息

**响应示例**:
```json
{
  "service": "Smart Turn Detection API",
  "version": "1.0.0",
  "status": "running",
  "description": "音频轮次检测服务，判断用户是否说完"
}
```

---

### 2. 健康检查

**GET** `/health`

检查服务健康状态
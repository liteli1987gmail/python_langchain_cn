# Embaas
[embaas](https://embaas.io)是一个全面管理的NLP API服务，提供嵌入生成、文档文本提取、文档到嵌入等功能。您可以选择[各种预训练模型](https://embaas.io/docs/models/embeddings)。

### 先决条件
在[https://embaas.io/register](https://embaas.io/register)上创建一个免费的embaas帐户并生成一个[API密钥](https://embaas.io/dashboard/api-keys)。

### 文档文本提取API
文档文本提取API允许您从给定的文档中提取文本。该API支持各种文档格式，包括PDF、mp3、mp4等。有关支持的格式的完整列表，请查看API文档（下方链接）。
```python
# 设置API密钥
embaas_api_key = "YOUR_API_KEY"
# 或者设置环境变量
os.environ["EMBAAS_API_KEY"] = "YOUR_API_KEY"
```

#### 使用blob（字节）
```python
from langchain.document_loaders.embaas import EmbaasBlobLoader
from langchain.document_loaders.blob_loaders import Blob
```

```python
blob_loader = EmbaasBlobLoader()
blob = Blob.from_path("example.pdf")
documents = blob_loader.load(blob)
```

```python
# 您还可以直接创建嵌入
blob_loader = EmbaasBlobLoader(params={"model": "e5-large-v2", "should_embed": True})
blob = Blob.from_path("example.pdf")
documents = blob_loader.load(blob)

print(documents[0]["metadata"]["embedding"])
```

#### 使用文件
```python
from langchain.document_loaders.embaas import EmbaasLoader
```

```python
file_loader = EmbaasLoader(file_path="example.pdf")
documents = file_loader.load()
```

```python
# 禁用自动文本拆分
file_loader = EmbaasLoader(file_path="example.mp3", params={"should_chunk": False})
documents = file_loader.load()
```

有关embaas文档文本提取API的更详细信息，请参阅[官方embaas API文档](https://embaas.io/api-reference)。

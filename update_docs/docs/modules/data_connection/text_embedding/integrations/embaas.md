# Embaas

[embaas](https://embaas.io)是一个完全托管的NLP API服务，提供嵌入生成、文档文本提取、文档到嵌入等功能。您可以选择[各种预训练模型](https://embaas.io/docs/models/embeddings)。

在本教程中，我们将向您展示如何使用embaas嵌入API为给定的文本生成嵌入。

### 先决条件
在[https://embaas.io/register](https://embaas.io/register)上创建您的免费embaas帐户，并生成一个[API密钥](https://embaas.io/dashboard/api-keys)。

```python
# 设置API密钥
embaas_api_key = "YOUR_API_KEY"
# 或设置环境变量
os.environ["EMBAAS_API_KEY"] = "YOUR_API_KEY"
```

......

```python
# 为单个文档创建嵌入
    doc_text = "This is a test document."
    doc_text_embedding = embeddings.embed_query(doc_text)
```

......

For more detailed information about the embaas Embeddings API, please refer to [the official embaas API documentation](https://embaas.io/api-reference).
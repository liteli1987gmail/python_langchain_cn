# AwaDB

> [AwaDB](https://github.com/awa-ai/awadb) 是一个用于 LLM 应用程序中搜索和存储嵌入向量的 AI 本地数据库。

## 安装和设置

```bash
pip install awadb
```


## VectorStore

存在一个围绕 AwaDB 向量数据库的包装器，可以将其用作向量存储，
无论是用于语义搜索还是示例选择。

```python
from langchain.vectorstores import AwaDB
```

有关 AwaDB 包装器的更详细说明，请参阅 [此笔记本](../modules/indexes/vectorstores/examples/awadb.ipynb)

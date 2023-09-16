# DeepInfra

[DeepInfra](https://deepinfra.com/?utm_source=langchain)是一种无服务器的推理服务，提供对[各种LLM模型](https://deepinfra.com/models?utm_source=langchain)和[嵌入模型](https://deepinfra.com/models?type=embeddings&utm_source=langchain)的访问。本笔记本介绍了如何在LangChain中使用DeepInfra进行文本嵌入。

```python
# 注册帐户：https://deepinfra.com/login?utm_source=langchain
from getpass import getpass

DEEPINFRA_API_TOKEN = getpass()
```

......

## Cosine similarity between "Dog is not a cat" and query: 0.7489097144129355

Cosine similarity between "Beta is the second letter of Greek alphabet" and query: 0.9519380640702013


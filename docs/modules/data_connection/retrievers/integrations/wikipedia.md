# Wikipedia

[Wikipedia](https://wikipedia.org/) 是一个多语言的免费在线百科全书，由一群志愿者社区（称为维基人）通过开放协作和使用基于维基的编辑系统MediaWiki进行撰写和维护。`Wikipedia`是历史上最大且阅读量最高的参考作品。

本笔记本演示了如何从 `wikipedia.org` 检索维基页面并将其转换为下游使用的文档格式。

## 安装

首先，您需要安装 `wikipedia` Python包。

```python
#!pip install wikipedia
```

`WikipediaRetriever` 有以下参数：

- 可选的 `lang`：默认值为"en"。用于在特定语言的维基百科中进行搜索。
- 可选的 `load_max_docs`：默认值为100。用于限制下载的文档数量。下载所有100个文档需要时间，因此对于实验，请使用较小的数量。目前限制为最多300个。
- 可选的 `load_all_available_meta`：默认值为False。默认只下载最重要的字段：`Published`（文档发布/最后更新日期）、`title`、`Summary`。如果为True，则还会下载其他字段。

`get_relevant_documents()` 有一个参数 `query`：用于在维基百科中查找文档的自由文本。

## 示例

### 运行检索器

```python
from langchain.retrievers import WikipediaRetriever
```

```python
retriever = WikipediaRetriever()
```

```python
docs = retriever.get_relevant_documents(query="HUNTER X HUNTER")
```

```python
docs[0].metadata  # 文档的元数据
```

```python
docs[0].page_content[:400]  # 文档的内容
```

### 事实问答

```python
# 获取一个令牌：https://platform.openai.com/account/api-keys
from getpass import getpass

OPENAI_API_KEY = getpass()
```

```python
import os

os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
```

```python
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain

model = ChatOpenAI(model_name="gpt-3.5-turbo")  # 切换到 'gpt-4'
qa = ConversationalRetrievalChain.from_llm(model, retriever=retriever)
```

```python
questions = [
    "什么是 Apify？",
    "1830年革命烈士纪念碑是什么时候创建的？",
    "什么是阿布哈耶伽里寺庙？",
    # "Wikipédia en français有多大？",
]
chat_history = []

for question in questions:
    result = qa({"question": question, "chat_history": chat_history})
    chat_history.append((question, result["answer"]))
    print(f"-> **问题**：{question} \n")
    print(f"**答案**：{result['answer']} \n")
```

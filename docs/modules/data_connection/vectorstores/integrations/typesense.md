# Typesense

> [Typesense](https://typesense.org) 是一个开源的内存搜索引擎，您可以[自行托管](https://typesense.org/docs/guide/install-typesense.html#option-2-local-machine-self-hosting)或在[Typesense云](https://cloud.typesense.org)上运行。

> Typesense专注于性能，通过将整个索引存储在RAM中（备份在磁盘上），并通过简化可用选项和设置良好的默认值来提供开箱即用的开发者体验。

> 它还允许您将基于属性的过滤与向量查询结合在一起，以检索最相关的文档。

本笔记本向您展示如何将Typesense用作您的VectorStore。

让我们首先安装依赖项：

```python
!pip install typesense openapi-schema-pydantic openai tiktoken
```

我们想要使用`OpenAIEmbeddings`，因此我们必须获取OpenAI API密钥。

```python
import os
import getpass

os.environ["OPENAI_API_KEY"] = getpass.getpass("OpenAI API Key：")
```


```python
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Typesense
from langchain.document_loaders import TextLoader
```

让我们导入我们的测试数据集：

```python
loader = TextLoader("../../../state_of_the_union.txt")
documents = loader.load()
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
docs = text_splitter.split_documents(documents)

embeddings = OpenAIEmbeddings()
```


```python
docsearch = Typesense.from_documents(
    docs,
    embeddings,
    typesense_client_params={
        "host": "localhost",  # Use xxx.a1.typesense.net for Typesense Cloud
        "port": "8108",  # Use 443 for Typesense Cloud
        "protocol": "http",  # Use https for Typesense Cloud
        "typesense_api_key": "xyz",
        "typesense_collection_name": "lang-chain",
    },
)
```

## 相似性搜索


```python
query = "What did the president say about Ketanji Brown Jackson"
found_docs = docsearch.similarity_search(query)
```


```python
print(found_docs[0].page_content)
```


## Typesense作为检索器

Typesense和其他向量存储一样，是LangChain的检索器，使用余弦相似性。


```python
retriever = docsearch.as_retriever()
retriever
```


```python
query = "What did the president say about Ketanji Brown Jackson"
retriever.get_relevant_documents(query)[0]
```

# Vectara

>[Vectara](https://vectara.com/) 是一个用于构建 LLM 引擎应用程序的 API 平台。它提供了一个简单易用的 API，用于由 Vectara 管理的文档索引和查询，优化了性能和准确性。

本笔记本展示了如何使用与 `Vectara` 向量数据库相关的功能。

有关如何使用 API 的更多信息，请参阅 [Vectara API 文档](https://docs.vectara.com/docs/)。

我们想要使用 `OpenAIEmbeddings`，所以我们需要获取 OpenAI API 密钥。

```python
import os
import getpass

os.environ["OPENAI_API_KEY"] = getpass.getpass("OpenAI API 密钥：")
```

    OpenAI API 密钥：········
    

```python
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Vectara
from langchain.document_loaders import TextLoader
```

```python
loader = TextLoader("../../../state_of_the_union.txt")
documents = loader.load()
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
docs = text_splitter.split_documents(documents)

embeddings = OpenAIEmbeddings()
```

## 从 LangChain 连接到 Vectara

Vectara API 提供了用于索引和查询的简单 API 端点。

```python
vectara = Vectara.from_documents(docs, embedding=None)
```

## 相似性搜索

使用 Vectara 的最简单场景是执行相似性搜索。

```python
query = "总统对 Ketanji Brown Jackson 说了什么"
found_docs = vectara.similarity_search(query, n_sentence_context=0)
```

```python
print(found_docs[0].page_content)
```

    Tonight. I call on the Senate to: Pass the Freedom to Vote Act. Pass the John Lewis Voting Rights Act. And while you’re at it, pass the Disclose Act so Americans can know who is funding our elections. 
    
    Tonight, I’d like to honor someone who has dedicated his life to serve this country: Justice Stephen Breyer—an Army veteran, Constitutional scholar, and retiring Justice of the United States Supreme Court. Justice Breyer, thank you for your service. 
    
    One of the most serious constitutional responsibilities a President has is nominating someone to serve on the United States Supreme Court. 
    
    And I did that 4 days ago, when I nominated Circuit Court of Appeals Judge Ketanji Brown Jackson. One of our nation’s top legal minds, who will continue Justice Breyer’s legacy of excellence.
    

## 带分数的相似性搜索

有时候我们可能希望执行搜索，同时获得相关性分数，以了解特定结果的好坏程度。

```python
query = "总统对 Ketanji Brown Jackson 说了什么"
found_docs = vectara.similarity_search_with_score(query)
```

```python
document, score = found_docs[0]
print(document.page_content)
print(f"\n分数：{score}")
```

    Tonight. I call on the Senate to: Pass the Freedom to Vote Act. Pass the John Lewis Voting Rights Act. And while you’re at it, pass the Disclose Act so Americans can know who is funding our elections. 
    
    Tonight, I’d like to honor someone who has dedicated his life to serve this country: Justice Stephen Breyer—an Army veteran, Constitutional scholar, and retiring Justice of the United States Supreme Court. Justice Breyer, thank you for your service. 
    
    One of the most serious constitutional responsibilities a President has is nominating someone to serve on the United States Supreme Court. 
    
    And I did that 4 days ago, when I nominated Circuit Court of Appeals Judge Ketanji Brown Jackson. One of our nation’s top legal minds, who will continue Justice Breyer’s legacy of excellence.
    
    分数：0.7129974
    

## Vectara 作为检索器

Vectara 和其他向量存储一样，是 LangChain 的检索器，使用余弦相似度。

```python
retriever = vectara.as_retriever()
retriever
```


    VectaraRetriever(vectorstore=<langchain.vectorstores.vectara.Vectara object at 0x122db2830>, search_type='similarity', search_kwargs={'lambda_val': 0.025, 'k': 5, 'filter': '', 'n_sentence_context': '0'})


```python
query = "总统对 Ketanji Brown Jackson 说了什么"
retriever.get_relevant_documents(query)[0]
```


    Document(page_content='Tonight. I call on the Senate to: Pass the Freedom to Vote Act. Pass the John Lewis Voting Rights Act. And while you’re at it, pass the Disclose Act so Americans can know who is funding our elections. \n\nTonight, I’d like to honor someone who has dedicated his life to serve this country: Justice Stephen Breyer—an Army veteran, Constitutional scholar, and retiring Justice of the United States Supreme Court. Justice Breyer, thank you for your service. \n\nOne of the most serious constitutional responsibilities a President has is nominating someone to serve on the United States Supreme Court. \n\nAnd I did that 4 days ago, when I nominated Circuit Court of Appeals Judge Ketanji Brown Jackson. One of our nation’s top legal minds, who will continue Justice Breyer’s legacy of excellence.', metadata={'source': '../../../state_of_the_union.txt'})






```python

```
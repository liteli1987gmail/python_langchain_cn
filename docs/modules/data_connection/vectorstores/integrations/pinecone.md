# Pinecone

[Pinecone](https://docs.pinecone.io/docs/overview) 是一个具有广泛功能的向量数据库。

本笔记本展示了如何使用与 `Pinecone` 向量数据库相关的功能。

要使用 Pinecone，您必须拥有一个 API 密钥。[安装说明](https://docs.pinecone.io/docs/quickstart)在这里。

```python
!pip install pinecone-client openai tiktoken
```


```python
import os
import getpass

PINECONE_API_KEY = getpass.getpass("Pinecone API Key:")
```


```python
PINECONE_ENV = getpass.getpass("Pinecone Environment:")
```

我们想要使用 `OpenAIEmbeddings`，因此我们必须获取 OpenAI API 密钥。

```python
os.environ["OPENAI_API_KEY"] = getpass.getpass("OpenAI API Key:")
```


```python
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Pinecone
from langchain.document_loaders import TextLoader
```


```python
from langchain.document_loaders import TextLoader

loader = TextLoader("../../../state_of_the_union.txt")
documents = loader.load()
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
docs = text_splitter.split_documents(documents)

embeddings = OpenAIEmbeddings()
```


```python
import pinecone

# initialize pinecone
pinecone.init(
    api_key=PINECONE_API_KEY,  # find at app.pinecone.io
    environment=PINECONE_ENV,  # next to api key in console
)

index_name = "langchain-demo"

docsearch = Pinecone.from_documents(docs, embeddings, index_name=index_name)

# if you already have an index, you can load it like this
# docsearch = Pinecone.from_existing_index(index_name, embeddings)

query = "What did the president say about Ketanji Brown Jackson"
docs = docsearch.similarity_search(query)
```


```python
print(docs[0].page_content)
```

### Maximal Marginal Relevance Searches

除了在检索器对象中使用相似性搜索之外，您还可以使用 `mmr` 作为检索器。

```python
retriever = docsearch.as_retriever(search_type="mmr")
matched_docs = retriever.get_relevant_documents(query)
for i, d in enumerate(matched_docs):
    print(f"\n## Document {i}\n")
    print(d.page_content)
```

或者直接使用 `max_marginal_relevance_search`

```python
found_docs = docsearch.max_marginal_relevance_search(query, k=2, fetch_k=10)
for i, doc in enumerate(found_docs):
    print(f"{i + 1}.", doc.page_content, "\n")
```

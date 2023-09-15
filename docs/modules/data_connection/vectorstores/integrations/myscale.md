# MyScale

>[MyScale](https://docs.myscale.com/en/overview/) is a cloud-based database optimized for AI applications and solutions, built on the open-source [ClickHouse](https://github.com/ClickHouse/ClickHouse). 

This notebook shows how to use functionality related to the `MyScale` vector database.

## Setting up envrionments


```python
!pip install clickhouse-connect
```

We want to use OpenAIEmbeddings so we have to get the OpenAI API Key.


```python
import os
import getpass

os.environ["OPENAI_API_KEY"] = getpass.getpass("OpenAI API Key:")
```

There are two ways to set up parameters for myscale index.

1. Environment Variables

    Before you run the app, please set the environment variable with `export`:
    `export MYSCALE_HOST='<your-endpoints-url>' MYSCALE_PORT=<your-endpoints-port> MYSCALE_USERNAME=<your-username> MYSCALE_PASSWORD=<your-password> ...`

    You can easily find your account, password and other info on our SaaS. For details please refer to [this document](https://docs.myscale.com/en/cluster-management/)

    Every attributes under `MyScaleSettings` can be set with prefix `MYSCALE_` and is case insensitive.

2. Create `MyScaleSettings` object with parameters


    ```python
    from langchain.vectorstores import MyScale, MyScaleSettings
    config = MyScaleSetting(host="<your-backend-url>", port=8443, ...)
    index = MyScale(embedding_function, config)
    index.add_documents(...)
    ```


```python
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import MyScale
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
for d in docs:
    d.metadata = {"some": "metadata"}
docsearch = MyScale.from_documents(docs, embeddings)

query = "What did the president say about Ketanji Brown Jackson"
docs = docsearch.similarity_search(query)
```


```python
print(docs[0].page_content)
```

## Get connection info and data schema


```python
print(str(docsearch))
```

## Filtering

You can have direct access to myscale SQL where statement. You can write `WHERE` clause following standard SQL.

**NOTE**: Please be aware of SQL injection, this interface must not be directly called by end-user.

If you custimized your `column_map` under your setting, you search with filter like this:


```python
from langchain.vectorstores import MyScale, MyScaleSettings
from langchain.document_loaders import TextLoader

loader = TextLoader("../../../state_of_the_union.txt")
documents = loader.load()
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
docs = text_splitter.split_documents(documents)

embeddings = OpenAIEmbeddings()

for i, d in enumerate(docs):
    d.metadata = {"doc_id": i}

docsearch = MyScale.from_documents(docs, embeddings)
```

### Similarity search with score

The returned distance score is cosine distance. Therefore, a lower score is better.


```python
meta = docsearch.metadata_column
output = docsearch.similarity_search_with_relevance_scores(
    "What did the president say about Ketanji Brown Jackson?",
    k=4,
    where_str=f"{meta}.doc_id<10",
)
for d, dist in output:
    print(dist, d.metadata, d.page_content[:20] + "...")
```

## Deleting your data


```python
docsearch.drop()
```


```python

```

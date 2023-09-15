# Typesense

> [Typesense](https://typesense.org) is an open source, in-memory search engine, that you can either [self-host](https://typesense.org/docs/guide/install-typesense.html#option-2-local-machine-self-hosting) or run on [Typesense Cloud](https://cloud.typesense.org/).
>
> Typesense focuses on performance by storing the entire index in RAM (with a backup on disk) and also focuses on providing an out-of-the-box developer experience by simplifying available options and setting good defaults.
>
> It also lets you combine attribute-based filtering together with vector queries, to fetch the most relevant documents.

This notebook shows you how to use Typesense as your VectorStore.

Let's first install our dependencies:


```python
!pip install typesense openapi-schema-pydantic openai tiktoken
```

We want to use `OpenAIEmbeddings` so we have to get the OpenAI API Key.


```python
import os
import getpass

os.environ["OPENAI_API_KEY"] = getpass.getpass("OpenAI API Key:")
```


```python
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Typesense
from langchain.document_loaders import TextLoader
```

Let's import our test dataset:


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

## Similarity Search


```python
query = "What did the president say about Ketanji Brown Jackson"
found_docs = docsearch.similarity_search(query)
```


```python
print(found_docs[0].page_content)
```

## Typesense as a Retriever

Typesense, as all the other vector stores, is a LangChain Retriever, by using cosine similarity.


```python
retriever = docsearch.as_retriever()
retriever
```


```python
query = "What did the president say about Ketanji Brown Jackson"
retriever.get_relevant_documents(query)[0]
```

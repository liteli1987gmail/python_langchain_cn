# OpenAI

Let's load the OpenAI Embedding class.


```python
from langchain.embeddings import OpenAIEmbeddings
```


```python
embeddings = OpenAIEmbeddings()
```


```python
text = "This is a test document."
```


```python
query_result = embeddings.embed_query(text)
```


```python
doc_result = embeddings.embed_documents([text])
```

Let's load the OpenAI Embedding class with first generation models (e.g. text-search-ada-doc-001/text-search-ada-query-001). Note: These are not recommended models - see [here](https://platform.openai.com/docs/guides/embeddings/what-are-embeddings)


```python
from langchain.embeddings.openai import OpenAIEmbeddings
```


```python
embeddings = OpenAIEmbeddings()
```


```python
text = "This is a test document."
```


```python
query_result = embeddings.embed_query(text)
```


```python
doc_result = embeddings.embed_documents([text])
```


```python
# if you are behind an explicit proxy, you can use the OPENAI_PROXY environment variable to pass through
os.environ["OPENAI_PROXY"] = "http://proxy.yourcompany.com:8080"
```

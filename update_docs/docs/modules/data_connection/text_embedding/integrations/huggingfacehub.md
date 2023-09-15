# Hugging Face Hub
Let's load the Hugging Face Embedding class.


```python
from langchain.embeddings import HuggingFaceEmbeddings
```


```python
embeddings = HuggingFaceEmbeddings()
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

```

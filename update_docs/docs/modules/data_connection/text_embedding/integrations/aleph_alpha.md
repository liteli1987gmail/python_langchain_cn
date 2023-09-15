# Aleph Alpha

There are two possible ways to use Aleph Alpha's semantic embeddings. If you have texts with a dissimilar structure (e.g. a Document and a Query) you would want to use asymmetric embeddings. Conversely, for texts with comparable structures, symmetric embeddings are the suggested approach.

## Asymmetric


```python
from langchain.embeddings import AlephAlphaAsymmetricSemanticEmbedding
```


```python
document = "This is a content of the document"
query = "What is the contnt of the document?"
```


```python
embeddings = AlephAlphaAsymmetricSemanticEmbedding()
```


```python
doc_result = embeddings.embed_documents([document])
```


```python
query_result = embeddings.embed_query(query)
```

## Symmetric


```python
from langchain.embeddings import AlephAlphaSymmetricSemanticEmbedding
```


```python
text = "This is a test text"
```


```python
embeddings = AlephAlphaSymmetricSemanticEmbedding()
```


```python
doc_result = embeddings.embed_documents([text])
```


```python
query_result = embeddings.embed_query(text)
```


```python

```

# Aleph Alpha
有两种可能的使用 Aleph Alpha 的语义嵌入方式。如果您有不同结构的文本（例如文档和查询），您将希望使用不对称嵌入。相反，对于结构相似的文本，建议使用对称嵌入。

## 不对称

```python
from langchain.embeddings import AlephAlphaAsymmetricSemanticEmbedding
```


```python
document = "这是文档的内容"
query = "文档的内容是什么？"
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

## 对称


```python
from langchain.embeddings import AlephAlphaSymmetricSemanticEmbedding
```


```python
text = "这是一个测试文本"
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
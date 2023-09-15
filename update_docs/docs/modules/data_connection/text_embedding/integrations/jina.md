# Jina

Let's load the Jina Embedding class.


```python
from langchain.embeddings import JinaEmbeddings
```


```python
embeddings = JinaEmbeddings(
    jina_auth_token=jina_auth_token, model_name="ViT-B-32::openai"
)
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

In the above example, `ViT-B-32::openai`, OpenAI's pretrained `ViT-B-32` model is used. For a full list of models, see [here](https://cloud.jina.ai/user/inference/model/63dca9df5a0da83009d519cd).


```python

```

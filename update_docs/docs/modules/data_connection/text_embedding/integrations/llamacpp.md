# Llama-cpp

This notebook goes over how to use Llama-cpp embeddings within LangChain


```python
!pip install llama-cpp-python
```


```python
from langchain.embeddings import LlamaCppEmbeddings
```


```python
llama = LlamaCppEmbeddings(model_path="/path/to/model/ggml-model-q4_0.bin")
```


```python
text = "This is a test document."
```


```python
query_result = llama.embed_query(text)
```


```python
doc_result = llama.embed_documents([text])
```

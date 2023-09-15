# InstructEmbeddings
Let's load the HuggingFace instruct Embeddings class.


```python
from langchain.embeddings import HuggingFaceInstructEmbeddings
```


```python
embeddings = HuggingFaceInstructEmbeddings(
    query_instruction="Represent the query for retrieval: "
)
```

    load INSTRUCTOR_Transformer
    max_seq_length  512
    


```python
text = "This is a test document."
```


```python
query_result = embeddings.embed_query(text)
```


```python

```

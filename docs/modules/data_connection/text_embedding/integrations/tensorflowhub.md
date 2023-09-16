# TensorflowHub
让我们加载TensorflowHub嵌入类。


```python
from langchain.embeddings import TensorflowHubEmbeddings
```


```python
embeddings = TensorflowHubEmbeddings()
```

    2023-01-30 23:53:01.652176: I tensorflow/core/platform/cpu_feature_guard.cc:193] 此TensorFlow二进制文件使用oneAPI Deep Neural Network Library (oneDNN)进行了优化，以在性能关键操作中使用以下CPU指令:  AVX2 FMA
    要在其他操作中启用它们，请使用适当的编译器标志重新构建TensorFlow。
    2023-01-30 23:53:34.362802: I tensorflow/core/platform/cpu_feature_guard.cc:193] 此TensorFlow二进制文件使用oneAPI Deep Neural Network Library (oneDNN)进行了优化，以在性能关键操作中使用以下CPU指令:  AVX2 FMA
    要在其他操作中启用它们，请使用适当的编译器标志重新构建TensorFlow。
    


```python
text = "这是一个测试文档。"
```


```python
query_result = embeddings.embed_query(text)
```


```python
doc_results = embeddings.embed_documents(["foo"])
```


```python
doc_results
```


```python

```

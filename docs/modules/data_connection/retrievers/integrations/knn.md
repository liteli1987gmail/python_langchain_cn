# kNN
>In statistics, the [k-nearest neighbors algorithm (k-NN)](https://en.wikipedia.org/wiki/K-nearest_neighbors_algorithm)是一种非参数的监督学习方法，最早由Evelyn Fix和Joseph Hodges于1951年开发，后来由Thomas Cover扩展。它用于分类和回归。
>本笔记本介绍了如何使用底层使用kNN的检索器。
>基本上基于https://github.com/karpathy/randomfun/blob/master/knn_vs_svm.html

```python
from langchain.retrievers import KNNRetriever
from langchain.embeddings import OpenAIEmbeddings
```

## 使用文本创建新的检索器

```python
retriever = KNNRetriever.from_texts(
    ["foo", "bar", "world", "hello", "foo bar"], OpenAIEmbeddings()
)
```

## 使用检索器

现在我们可以使用检索器了！


```python
result = retriever.get_relevant_documents("foo")
```


```python
result
```
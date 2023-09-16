# TF-IDF

>[TF-IDF](https://scikit-learn.org/stable/modules/feature_extraction.html#tfidf-term-weighting)表示词频乘以逆文档频率。

这个笔记本介绍了如何使用一个底层使用[TF-IDF](https://en.wikipedia.org/wiki/Tf%E2%80%93idf)的检索器，使用`scikit-learn`包。

有关TF-IDF详细信息，请参阅[此博文](https://medium.com/data-science-bootcamp/tf-idf-basics-of-information-retrieval-48de122b2a4c)。

```python
# !pip install scikit-learn
```

```python
from langchain.retrievers import TFIDFRetriever
```

## 使用文本创建新的检索器

```python
retriever = TFIDFRetriever.from_texts(["foo", "bar", "world", "hello", "foo bar"])
```

## 使用文档创建新的检索器

现在，您可以使用您创建的文档来创建一个新的检索器。

```python
from langchain.schema import Document

retriever = TFIDFRetriever.from_documents(
    [
        Document(page_content="foo"),
        Document(page_content="bar"),
        Document(page_content="world"),
        Document(page_content="hello"),
        Document(page_content="foo bar"),
    ]
)
```

## 使用检索器

我们现在可以使用检索器！

```python
result = retriever.get_relevant_documents("foo")
```

```python
result
```




    [Document(page_content='foo', metadata={}),
     Document(page_content='foo bar', metadata={}),
     Document(page_content='hello', metadata={}),
     Document(page_content='world', metadata={})]

# ElasticSearch BM25
>[Elasticsearch](https://www.elastic.co/elasticsearch/)是一个分布式的、RESTful的搜索和分析引擎。它提供了一个分布式、支持多租户的全文搜索引擎，具有HTTP Web接口和无模式的JSON文档。
>在信息检索中，[Okapi BM25](https://en.wikipedia.org/wiki/Okapi_BM25)（BM是最佳匹配的缩写）是搜索引擎用于估计文档与给定搜索查询相关性的排名函数。它基于上世纪70年代和80年代由Stephen E. Robertson、Karen Spärck Jones等人开发的概率检索框架。
>实际的排名函数名称是BM25。更完整的名称Okapi BM25包括了第一个使用它的系统的名称，该系统是在20世纪80年代和90年代在伦敦的城市大学实施的Okapi信息检索系统。BM25及其更新的变体，如BM25F（可以考虑文档结构和锚文本的BM25版本），代表文档检索中使用的类似TF-IDF的检索函数。
>本笔记本展示了如何使用使用`ElasticSearch`和`BM25`的检索器。
>有关BM25的详细信息，请参阅[此博客文章](https://www.elastic.co/blog/practical-bm25-part-2-the-bm25-algorithm-and-its-variables)。

```python
#!pip install elasticsearch
```

```python
from langchain.retrievers import ElasticSearchBM25Retriever
```

## 创建新的检索器

```python
elasticsearch_url = "http://localhost:9200"
retriever = ElasticSearchBM25Retriever.create(elasticsearch_url, "langchain-index-4")
```

```python
# 或者，您可以加载现有的索引
# import elasticsearch
# elasticsearch_url="http://localhost:9200"
# retriever = ElasticSearchBM25Retriever(elasticsearch.Elasticsearch(elasticsearch_url), "langchain-index")
```

## 添加文本（如果需要）

我们可以选择将文本添加到检索器中（如果它们尚未存在）

```python
retriever.add_texts(["foo", "bar", "world", "hello", "foo bar"])
```



    ['cbd4cb47-8d9f-4f34-b80e-ea871bc49856',
     'f3bd2e24-76d1-4f9b-826b-ec4c0e8c7365',
     '8631bfc8-7c12-48ee-ab56-8ad5f373676e',
     '8be8374c-3253-4d87-928d-d73550a2ecf0',
     'd79f457b-2842-4eab-ae10-77aa420b53d7']


## 使用检索器

现在我们可以使用检索器了！


```python
result = retriever.get_relevant_documents("foo")
```


```python
result
```
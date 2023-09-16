# Vespa

[Vespa](https://vespa.ai/) 是一个功能齐全的搜索引擎和向量数据库。它支持向量搜索 (ANN)、词法搜索和结构化数据搜索，所有这些都可以在同一个查询中进行。

这个笔记本展示了如何使用 `Vespa.ai` 作为 LangChain 的检索器。

为了创建一个检索器，我们使用 [pyvespa](https://pyvespa.readthedocs.io/en/latest/index.html) 来创建与 `Vespa` 服务的连接。

```python
#!pip install pyvespa
```

```python
from vespa.application import Vespa

vespa_app = Vespa(url="https://doc-search.vespa.oath.cloud")
```

这将创建一个与 `Vespa` 服务的连接，这里是 Vespa 文档搜索服务。
使用 `pyvespa` 包，你还可以连接到一个 [Vespa 云实例](https://pyvespa.readthedocs.io/en/latest/deploy-vespa-cloud.html) 或一个本地 [Docker 实例](https://pyvespa.readthedocs.io/en/latest/deploy-docker.html)。

连接到服务后，你可以设置检索器：

```python
from langchain.retrievers.vespa_retriever import VespaRetriever

vespa_query_body = {
    "yql": "select content from paragraph where userQuery()",
    "hits": 5,
    "ranking": "documentation",
    "locale": "en-us",
}
vespa_content_field = "content"
retriever = VespaRetriever(vespa_app, vespa_query_body, vespa_content_field)
```

这将设置一个从 Vespa 应用程序中获取文档的 LangChain 检索器。
在这里，从 `paragraph` 文档类型的 `content` 字段中最多检索 5 个结果，使用 `documentation` 作为排序方法。`userQuery()` 被实际查询从 LangChain 传递过来所替代。

更多信息请参考 [pyvespa 文档](https://pyvespa.readthedocs.io/en/latest/getting-started-pyvespa.html#Query)。

现在你可以返回结果并继续在 LangChain 中使用这些结果。

```python
retriever.get_relevant_documents("what is vespa?")
```
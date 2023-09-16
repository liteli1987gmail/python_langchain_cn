# Azure Cognitive Search

>[Azure Cognitive Search](https://learn.microsoft.com/en-us/azure/search/search-what-is-azure-search) (以前称为 `Azure Search`) 是一个云搜索服务，为开发人员提供了在 web、移动和企业应用程序中构建丰富搜索体验所需的基础设施、API 和工具。搜索是向用户展示文本的任何应用程序的基础，常见的场景包括目录或文档搜索、在线零售应用程序或专有内容的数据探索。创建搜索服务时，您将使用以下功能：
>- 用于对包含用户拥有的内容的搜索索引进行全文搜索的搜索引擎
>- 丰富的索引，包括词法分析和可选的人工智能增强，用于内容提取和转换
>- 用于文本搜索、模糊搜索、自动完成、地理搜索等的丰富查询语法
>- 通过 Azure SDK 中的 REST API 和客户端库进行编程
>- 在数据层、机器学习层和人工智能 (认知服务) 层进行 Azure 集成

这个笔记本展示了如何在 LangChain 中使用 Azure Cognitive Search (ACS)。

## 设置 Azure Cognitive Search

要设置 ACS，请按照此处的说明进行操作（https://learn.microsoft.com/en-us/azure/search/search-create-service-portal）。

请注意
1. 您的 ACS 服务名称，
2. 您的 ACS 索引名称，
3. 您的 API 密钥。

您的 API 密钥可以是管理密钥或查询密钥，但由于我们只读取数据，建议使用查询密钥。

## 使用 Azure Cognitive Search 检索器


```python
import os

from langchain.retrievers import AzureCognitiveSearchRetriever
```

将服务名称、索引名称和 API 密钥设置为环境变量（或者，您可以将它们作为参数传递给 `AzureCognitiveSearchRetriever`）。


```python
os.environ["AZURE_COGNITIVE_SEARCH_SERVICE_NAME"] = "<YOUR_ACS_SERVICE_NAME>"
os.environ["AZURE_COGNITIVE_SEARCH_INDEX_NAME"] = "<YOUR_ACS_INDEX_NAME>"
os.environ["AZURE_COGNITIVE_SEARCH_API_KEY"] = "<YOUR_API_KEY>"
```

创建检索器


```python
retriever = AzureCognitiveSearchRetriever(content_key="content")
```

现在您可以从 Azure Cognitive Search 中检索文档


```python
retriever.get_relevant_documents("what is langchain")
```

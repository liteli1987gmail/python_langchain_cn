# AWS Kendra

> AWS Kendra 是由亚马逊网络服务 (AWS) 提供的智能搜索服务。它利用先进的自然语言处理 (NLP) 和机器学习算法，在组织内的各种数据源上实现强大的搜索功能。Kendra 旨在帮助用户快速准确地找到所需的信息，提高生产力和决策能力。

> 使用 Kendra，用户可以搜索各种内容类型，包括文档、常见问题解答 (FAQ)、知识库、手册和网站。它支持多种语言，能够理解复杂的查询、同义词和上下文含义，提供高度相关的搜索结果。

## 使用 AWS Kendra 索引检索器


```python
#!pip install boto3
```


```python
import boto3
from langchain.retrievers import AwsKendraIndexRetriever
```

创建新的检索器


```python
kclient = boto3.client("kendra", region_name="us-east-1")

retriever = AwsKendraIndexRetriever(
    kclient=kclient,
    kendraindex="kendraindex",
)
```

现在您可以使用从 AWS Kendra 索引中检索的文档


```python
retriever.get_relevant_documents("what is langchain")
```

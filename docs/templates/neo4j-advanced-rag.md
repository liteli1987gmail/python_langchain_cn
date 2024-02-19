# neo4j-advanced-rag

这个模板允许您通过实施高级检索策略来平衡精确嵌入和上下文保留。

## 策略

1. **典型的RAG**：
   - 传统方法，索引的确切数据是检索的数据。
2. **父检索器**：
   - 将整个文档划分为较小的块，称为父文档和子文档，而不是索引整个文档。
   - 子文档被索引以更好地表示特定概念，而父文档则被检索以确保上下文保留。
3. **假设性问题**：
     - 处理文档以确定它们可能回答的问题。
     - 然后将这些问题索引以更好地表示特定概念，同时检索父文档以确保上下文保留。
4. **摘要**：
     - 不是索引整个文档，而是创建并索引文档的摘要。
     - 同样，父文档在RAG应用程序中被检索。

## 环境设置

您需要定义以下环境变量

```
OPENAI_API_KEY=<YOUR_OPENAI_API_KEY>
NEO4J_URI=<YOUR_NEO4J_URI>
NEO4J_USERNAME=<YOUR_NEO4J_USERNAME>
NEO4J_PASSWORD=<YOUR_NEO4J_PASSWORD>
```

## 用数据填充

如果您想用一些示例数据填充数据库，可以运行 `python ingest.py`。
该脚本将来自文件 `dune.txt` 的文本部分处理并存储到Neo4j图数据库中。
首先，将文本分成较大的块（“父块”），然后进一步细分为较小的块（“子块”），其中父块和子块都略有重叠以保持上下文。
在将这些块存储到数据库中之后，使用OpenAI的嵌入计算子节点的嵌入，并将其存储回图中以供将来检索或分析。
对于每个父节点，生成假设性问题和摘要，将其嵌入并添加到数据库中。
此外，为每个检索策略创建一个向量索引，以便对这些嵌入进行高效查询。

*请注意，由于LLM生成假设性问题和摘要的速度很快，因此摄入可能需要一两分钟。*

## 用法

要使用此包，您首先应该安装LangChain CLI：

```shell
pip install -U "langchain-cli[serve]"
```

要创建一个新的LangChain项目并将其安装为唯一的包，可以执行以下操作：

```shell
langchain app new my-app --package neo4j-advanced-rag
```

如果要将其添加到现有项目中，只需运行：

```shell
langchain app add neo4j-advanced-rag
```

并将以下代码添加到您的 `server.py` 文件中：
```python
from neo4j_advanced_rag import chain as neo4j_advanced_chain

add_routes(app, neo4j_advanced_chain, path="/neo4j-advanced-rag")
```

（可选）现在让我们配置LangSmith。
LangSmith将帮助我们跟踪、监视和调试LangChain应用程序。
LangSmith目前处于私有测试版，您可以在[此处](https://smith.langchain.com/)注册。
如果您没有访问权限，可以跳过此部分

```shell
export LANGCHAIN_TRACING_V2=true
export LANGCHAIN_API_KEY=<your-api-key>
export LANGCHAIN_PROJECT=<your-project>  # if not specified, defaults to "default"
```

如果您在此目录中，则可以直接启动LangServe实例：

```shell
langchain serve
```

这将启动FastAPI应用程序，服务器在本地运行，地址为
[http://localhost:8000](http://localhost:8000)

我们可以在[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)上查看所有模板
我们可以在[http://127.0.0.1:8000/neo4j-advanced-rag/playground](http://127.0.0.1:8000/neo4j-advanced-rag/playground)上访问playground

我们可以通过以下代码访问模板：

```python
from langserve.client import RemoteRunnable

runnable = RemoteRunnable("http://localhost:8000/neo4j-advanced-rag")
```
=======
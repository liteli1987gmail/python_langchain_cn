# neo4j-parent

这个模板允许你通过将文档分成较小的块并检索它们的原始或更大的文本信息来平衡精确嵌入和上下文保留。

使用Neo4j向量索引，该包使用向量相似性搜索查询子节点，并通过定义适当的`retrieval_query`参数检索相应的父节点文本。

## 环境设置

您需要定义以下环境变量

```
OPENAI_API_KEY=<YOUR_OPENAI_API_KEY>
NEO4J_URI=<YOUR_NEO4J_URI>
NEO4J_USERNAME=<YOUR_NEO4J_USERNAME>
NEO4J_PASSWORD=<YOUR_NEO4J_PASSWORD>
```

## 数据填充

如果您想用一些示例数据填充数据库，可以运行`python ingest.py`。
该脚本将来自文件`dune.txt`的文本部分处理并存储到Neo4j图数据库中。
首先，将文本分成较大的块（“父节点”），然后进一步细分为较小的块（“子节点”），其中父节点和子节点块都有些重叠以保持上下文。
在将这些块存储到数据库后，使用OpenAI的嵌入计算子节点的嵌入，并将其存储回图中以供将来检索或分析。
此外，还创建了一个名为`retrieval`的向量索引，用于高效查询这些嵌入。

## 使用方法

要使用此包，您首先应该安装LangChain CLI：

```shell
pip install -U langchain-cli
```

要创建一个新的LangChain项目并将其安装为唯一的包，可以执行以下操作：

```shell
langchain app new my-app --package neo4j-parent
```

如果要将其添加到现有项目中，只需运行：

```shell
langchain app add neo4j-parent
```

并将以下代码添加到您的`server.py`文件中：
```python
from neo4j_parent import chain as neo4j_parent_chain

add_routes(app, neo4j_parent_chain, path="/neo4j-parent")
```

（可选）现在让我们配置LangSmith。
LangSmith将帮助我们跟踪、监视和调试LangChain应用程序。
LangSmith目前处于私有测试版，您可以在[此处](https://smith.langchain.com/)注册。
如果您没有访问权限，可以跳过此部分

```shell
export LANGCHAIN_TRACING_V2=true
export LANGCHAIN_API_KEY=<your-api-key>
export LANGCHAIN_PROJECT=<your-project>  # 如果未指定，默认为"default"
```

如果您在此目录中，则可以直接启动LangServe实例：

```shell
langchain serve
```

这将在本地启动FastAPI应用程序，服务器正在本地运行，地址为
[http://localhost:8000](http://localhost:8000)

我们可以在[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)上看到所有模板
我们可以在[http://127.0.0.1:8000/neo4j-parent/playground](http://127.0.0.1:8000/neo4j-parent/playground)访问playground

我们可以通过以下代码访问模板：

```python
from langserve.client import RemoteRunnable

runnable = RemoteRunnable("http://localhost:8000/neo4j-parent")
```
=======
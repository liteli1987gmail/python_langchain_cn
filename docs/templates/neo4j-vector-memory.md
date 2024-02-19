# neo4j-vector-memory

这个模板允许您将LLM与基于向量的检索系统集成，使用Neo4j作为向量存储。
此外，它使用Neo4j数据库的图形功能来存储和检索特定用户会话的对话历史记录。
将对话历史记录存储为图形使得对话流程无缝，同时还可以分析用户行为和通过图形分析检索文本块。

## 环境设置

您需要定义以下环境变量

```
OPENAI_API_KEY=<YOUR_OPENAI_API_KEY>
NEO4J_URI=<YOUR_NEO4J_URI>
NEO4J_USERNAME=<YOUR_NEO4J_USERNAME>
NEO4J_PASSWORD=<YOUR_NEO4J_PASSWORD>
```

## 数据填充

如果您想要使用一些示例数据填充数据库，可以运行`python ingest.py`。
该脚本将处理并将文本文件`dune.txt`的部分内容存储到Neo4j图形数据库中。
此外，还为这些嵌入创建了一个名为`dune`的向量索引，以便进行高效的查询。

## 使用方法

要使用此包，您首先需要安装LangChain CLI：

```shell
pip install -U langchain-cli
```

要创建一个新的LangChain项目并将其安装为唯一的包，可以执行以下操作：

```shell
langchain app new my-app --package neo4j-vector-memory
```

如果要将其添加到现有项目中，只需运行：

```shell
langchain app add neo4j-vector-memory
```

并将以下代码添加到您的`server.py`文件中：
```python
from neo4j_vector_memory import chain as neo4j_vector_memory_chain

add_routes(app, neo4j_vector_memory_chain, path="/neo4j-vector-memory")
```

（可选）现在让我们配置LangSmith。
LangSmith将帮助我们跟踪、监视和调试LangChain应用程序。
LangSmith目前处于私有测试版，您可以在[此处](https://smith.langchain.com/)注册。
如果您没有访问权限，可以跳过此部分。

```shell
export LANGCHAIN_TRACING_V2=true
export LANGCHAIN_API_KEY=<your-api-key>
export LANGCHAIN_PROJECT=<your-project>  # 如果未指定，默认为"default"
```

如果您在此目录中，则可以直接启动LangServe实例：

```shell
langchain serve
```

这将在本地启动FastAPI应用程序，服务器正在运行在[http://localhost:8000](http://localhost:8000)

我们可以在[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)上查看所有模板
我们可以在[http://127.0.0.1:8000/neo4j-vector-memory/playground](http://127.0.0.1:8000/neo4j-parent/playground)访问playground

我们可以通过以下代码访问模板：

```python
from langserve.client import RemoteRunnable

runnable = RemoteRunnable("http://localhost:8000/neo4j-vector-memory")
```
=======

请确认以上翻译是否符合您的要求。
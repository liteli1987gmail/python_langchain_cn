# neo4j-semantic-ollama

这个模板旨在通过使用Mixtral作为基于JSON的代理，实现与Neo4j等图数据库交互的代理。
语义层为代理提供了一套强大的工具，使其能够根据用户的意图与图数据库进行交互。
在[相应的博客文章](https://medium.com/towards-data-science/enhancing-interaction-between-language-models-and-graph-databases-via-a-semantic-layer-0a78ad3eba49)中了解有关语义层模板的更多信息。

![图示Neo4j语义层与使用Information、Recommendation和Memory等工具与知识图连接的代理的工作流程。](https://raw.githubusercontent.com/langchain-ai/langchain/master/templates/neo4j-semantic-ollama/static/workflow.png "Neo4j语义层工作流程图")

## 工具

该代理利用多个工具有效地与Neo4j图数据库进行交互：

1. **Information工具**：
   - 检索有关电影或个人的数据，确保代理能够访问最新和最相关的信息。
2. **Recommendation工具**：
   - 根据用户的偏好和输入提供电影推荐。
3. **Memory工具**：
   - 在知识图中存储有关用户偏好的信息，实现多次交互的个性化体验。
4. **Smalltalk工具**：
   - 允许代理处理闲聊。

## 环境设置

在使用此模板之前，您需要设置Ollama和Neo4j数据库。

1. 按照[此处的说明](https://python.langchain.com/docs/integrations/chat/ollama)下载Ollama。

2. 下载您感兴趣的LLM：

    * 该软件包使用`mixtral`：`ollama pull mixtral`
    * 您可以从[这里](https://ollama.ai/library)选择多个LLM

您需要定义以下环境变量

```
OLLAMA_BASE_URL=<YOUR_OLLAMA_URL>
NEO4J_URI=<YOUR_NEO4J_URI>
NEO4J_USERNAME=<YOUR_NEO4J_USERNAME>
NEO4J_PASSWORD=<YOUR_NEO4J_PASSWORD>
```

## 数据填充

如果您想使用示例电影数据集填充数据库，可以运行`python ingest.py`。
该脚本导入有关电影及其用户评分的信息。
此外，该脚本创建了两个[全文索引](https://neo4j.com/docs/cypher-manual/current/indexes-for-full-text-search/)，用于将用户输入的信息映射到数据库。

## 使用方法

要使用此软件包，您首先需要安装LangChain CLI：

```shell
pip install -U "langchain-cli[serve]"
```

要创建一个新的LangChain项目并将其安装为唯一的软件包，可以执行以下操作：

```shell
langchain app new my-app --package neo4j-semantic-ollama
```

如果要将其添加到现有项目中，只需运行：

```shell
langchain app add neo4j-semantic-ollama
```

并将以下代码添加到您的`server.py`文件中：
```python
from neo4j_semantic_layer import agent_executor as neo4j_semantic_agent

add_routes(app, neo4j_semantic_agent, path="/neo4j-semantic-ollama")
```

（可选）现在让我们配置LangSmith。
LangSmith将帮助我们跟踪、监视和调试LangChain应用程序。
LangSmith目前处于私人测试版，您可以在[此处](https://smith.langchain.com/)注册。
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

这将在本地启动FastAPI应用程序，服务器正在[http://localhost:8000](http://localhost:8000)上运行

我们可以在[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)上查看所有模板
我们可以在[http://127.0.0.1:8000/neo4j-semantic-ollama/playground](http://127.0.0.1:8000/neo4j-semantic-ollama/playground)上访问playground

我们可以通过以下代码访问模板：

```python
from langserve.client import RemoteRunnable

runnable = RemoteRunnable("http://localhost:8000/neo4j-semantic-ollama")
```
=======
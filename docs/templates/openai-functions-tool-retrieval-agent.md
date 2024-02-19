# openai-functions-tool-retrieval-agent

这个模板引入了一个新的想法，即使用检索来选择用于回答代理查询的工具集。当您有很多工具可供选择时，这非常有用。您无法在提示中放置所有工具的描述（由于上下文长度问题），因此您可以在运行时动态选择要考虑使用的N个工具。

在这个模板中，我们将创建一个有点牵强的示例。我们将有一个合法的工具（搜索）和99个只是胡言乱语的假工具。然后，我们将在提示模板中添加一个步骤，该步骤接受用户输入并检索与查询相关的工具。

此模板基于[此代理人操作指南](https://python.langchain.com/docs/modules/agents/how_to/custom_agent_with_tool_retrieval)。

## 环境设置

需要设置以下环境变量：

将`OPENAI_API_KEY`环境变量设置为访问OpenAI模型。

将`TAVILY_API_KEY`环境变量设置为访问Tavily。

## 使用方法

要使用此软件包，您首先应该安装LangChain CLI：

```shell
pip install -U langchain-cli
```

要创建一个新的LangChain项目并将其安装为唯一的软件包，可以执行以下操作：

```shell
langchain app new my-app --package openai-functions-tool-retrieval-agent
```

如果要将其添加到现有项目中，只需运行：

```shell
langchain app add openai-functions-tool-retrieval-agent
```

并将以下代码添加到您的`server.py`文件中：
```python
from openai_functions_tool_retrieval_agent import chain as openai_functions_tool_retrieval_agent_chain

add_routes(app, openai_functions_tool_retrieval_agent_chain, path="/openai-functions-tool-retrieval-agent")
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

这将在本地启动一个运行的FastAPI应用程序，位于
[http://localhost:8000](http://localhost:8000)

我们可以在[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)上查看所有模板
我们可以在[http://127.0.0.1:8000/openai-functions-tool-retrieval-agent/playground](http://127.0.0.1:8000/openai-functions-tool-retrieval-agent/playground)访问playground

我们可以通过以下代码访问模板：

```python
from langserve.client import RemoteRunnable

runnable = RemoteRunnable("http://localhost:8000/openai-functions-tool-retrieval-agent")
```
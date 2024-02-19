# xml-agent

这个包创建了一个代理，它使用XML语法来传达其决策以采取何种行动。它使用Anthropic的Claude模型来编写XML语法，并可以选择使用DuckDuckGo在互联网上查找信息。

## 环境设置

需要设置两个环境变量：

- `ANTHROPIC_API_KEY`：使用Anthropic所需

## 使用方法

要使用这个包，首先应该安装LangChain CLI：

```shell
pip install -U langchain-cli
```

要创建一个新的LangChain项目并将其安装为唯一的包，可以执行以下操作：

```shell
langchain app new my-app --package xml-agent
```

如果要将其添加到现有项目中，只需运行：

```shell
langchain app add xml-agent
```

并将以下代码添加到您的`server.py`文件中：
```python
from xml_agent import agent_executor as xml_agent_chain

add_routes(app, xml_agent_chain, path="/xml-agent")
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

这将启动FastAPI应用程序，服务器在本地运行，地址为
[http://localhost:8000](http://localhost:8000)

我们可以在[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)上查看所有模板
我们可以在[http://127.0.0.1:8000/xml-agent/playground](http://127.0.0.1:8000/xml-agent/playground)上访问playground

我们可以通过以下代码访问代码中的模板：

```python
from langserve.client import RemoteRunnable

runnable = RemoteRunnable("http://localhost:8000/xml-agent")
```
=======
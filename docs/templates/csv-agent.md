# csv-agent

这个模板使用一个[csv代理](https://python.langchain.com/docs/integrations/toolkits/csv)，通过工具（Python REPL）和内存（vectorstore）与文本数据进行交互（问答）。

## 环境设置

设置`OPENAI_API_KEY`环境变量以访问OpenAI模型。

要设置环境，应该运行`ingest.py`脚本来处理向vectorstore中摄取。

## 使用方法

要使用这个包，首先应该安装LangChain CLI：

```shell
pip install -U langchain-cli
```

要创建一个新的LangChain项目并将其安装为唯一的包，可以执行以下操作：

```shell
langchain app new my-app --package csv-agent
```

如果要将其添加到现有项目中，只需运行：

```shell
langchain app add csv-agent
```

并将以下代码添加到你的`server.py`文件中：
```python
from csv_agent.agent import agent_executor as csv_agent_chain

add_routes(app, csv_agent_chain, path="/csv-agent")
```

（可选）现在让我们配置LangSmith。
LangSmith将帮助我们跟踪、监控和调试LangChain应用程序。
LangSmith目前处于私有测试版，你可以在[这里](https://smith.langchain.com/)注册。
如果你没有访问权限，可以跳过此部分


```shell
export LANGCHAIN_TRACING_V2=true
export LANGCHAIN_API_KEY=<your-api-key>
export LANGCHAIN_PROJECT=<your-project>  # 如果未指定，默认为"default"
```

如果你在此目录中，则可以直接启动LangServe实例：

```shell
langchain serve
```

这将启动FastAPI应用程序，服务器在本地运行，地址为
[http://localhost:8000](http://localhost:8000)

我们可以在[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)上看到所有模板
我们可以在[http://127.0.0.1:8000/csv-agent/playground](http://127.0.0.1:8000/csv-agent/playground)上访问playground

我们可以通过以下代码访问模板：

```python
from langserve.client import RemoteRunnable

runnable = RemoteRunnable("http://localhost:8000/csv-agent")
```

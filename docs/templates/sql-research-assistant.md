# sql-research-assistant

这个包对SQL数据库进行研究

## 用法

这个包依赖于多个模型，这些模型有以下依赖关系：

- OpenAI: 设置`OPENAI_API_KEY`环境变量
- Ollama: [安装和运行Ollama](https://python.langchain.com/docs/integrations/chat/ollama)
- llama2 (在Ollama上): `ollama pull llama2` (否则你将从Ollama得到404错误)

要使用这个包，你首先应该安装LangChain CLI:

```shell
pip install -U langchain-cli
```

要创建一个新的LangChain项目并将其安装为唯一的包，你可以执行以下操作:

```shell
langchain app new my-app --package sql-research-assistant
```

如果你想将其添加到现有项目中，你只需运行:

```shell
langchain app add sql-research-assistant
```

并将以下代码添加到你的`server.py`文件中:
```python
from sql_research_assistant import chain as sql_research_assistant_chain

add_routes(app, sql_research_assistant_chain, path="/sql-research-assistant")
```

(可选) 现在让我们配置LangSmith。
LangSmith将帮助我们跟踪、监视和调试LangChain应用程序。
LangSmith目前处于私有测试版，你可以在[这里](https://smith.langchain.com/)注册。
如果你没有访问权限，你可以跳过这一部分


```shell
export LANGCHAIN_TRACING_V2=true
export LANGCHAIN_API_KEY=<your-api-key>
export LANGCHAIN_PROJECT=<your-project>  # 如果未指定，默认为"default"
```

如果你在这个目录下，你可以直接启动一个LangServe实例:

```shell
langchain serve
```

这将启动一个FastAPI应用程序，服务器在本地运行，地址为
[http://localhost:8000](http://localhost:8000)

我们可以在[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)上看到所有模板
我们可以在[http://127.0.0.1:8000/sql-research-assistant/playground](http://127.0.0.1:8000/sql-research-assistant/playground)上访问playground

我们可以通过以下代码访问模板:

```python
from langserve.client import RemoteRunnable

runnable = RemoteRunnable("http://localhost:8000/sql-research-assistant")
```
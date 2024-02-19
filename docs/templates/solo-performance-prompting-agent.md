# solo-performance-prompting-agent

这个模板创建了一个代理，通过与多个人物进行多轮自我协作，将单个LLM转化为认知协同者。
认知协同者是指与多个思维合作的智能代理，结合他们各自的优势和知识，提高复杂任务中的问题解决和整体性能。通过根据任务输入动态识别和模拟不同的人物，SPP释放了LLM中认知协同的潜力。

这个模板将使用`DuckDuckGo`搜索API。

## 环境设置

这个模板将默认使用`OpenAI`。
请确保在您的环境中设置了`OPENAI_API_KEY`。

## 使用方法

要使用这个包，您首先应该安装LangChain CLI:

```shell
pip install -U langchain-cli
```

要创建一个新的LangChain项目并将其安装为唯一的包，可以执行以下操作:

```shell
langchain app new my-app --package solo-performance-prompting-agent
```

如果您想将其添加到现有项目中，只需运行:

```shell
langchain app add solo-performance-prompting-agent
```

并将以下代码添加到您的`server.py`文件中:
```python
from solo_performance_prompting_agent.agent import agent_executor as solo_performance_prompting_agent_chain

add_routes(app, solo_performance_prompting_agent_chain, path="/solo-performance-prompting-agent")
```

(可选) 现在让我们配置LangSmith。
LangSmith将帮助我们跟踪、监视和调试LangChain应用程序。
LangSmith目前处于私有测试版，您可以在[这里](https://smith.langchain.com/)注册。
如果您没有访问权限，可以跳过此部分


```shell
export LANGCHAIN_TRACING_V2=true
export LANGCHAIN_API_KEY=<your-api-key>
export LANGCHAIN_PROJECT=<your-project>  # 如果未指定，默认为"default"
```

如果您在此目录中，则可以直接启动LangServe实例:

```shell
langchain serve
```

这将在本地启动一个运行在[http://localhost:8000](http://localhost:8000)的FastAPI应用程序的服务器

我们可以在[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)上查看所有模板
我们可以在[http://127.0.0.1:8000/solo-performance-prompting-agent/playground](http://127.0.0.1:8000/solo-performance-prompting-agent/playground)上访问playground

我们可以通过以下代码访问模板:

```python
from langserve.client import RemoteRunnable

runnable = RemoteRunnable("http://localhost:8000/solo-performance-prompting-agent")
```
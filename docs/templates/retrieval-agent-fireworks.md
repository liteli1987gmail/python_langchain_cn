# 检索代理火花

这个包使用在FireworksAI上托管的开源模型来使用代理架构进行检索。默认情况下，它在Arxiv上进行检索。

我们将使用`Mixtral8x7b-instruct-v0.1`，在这篇博文中展示了它在函数调用方面产生了合理的结果，尽管它并没有针对这个任务进行微调: https://huggingface.co/blog/open-source-llms-as-agents


## 环境设置

有多种运行OSS模型的好方法。我们将使用FireworksAI作为运行模型的简单方法。更多信息请参见[这里](https://python.langchain.com/docs/integrations/providers/fireworks)。

设置`FIREWORKS_API_KEY`环境变量以访问Fireworks。


## 用法

要使用这个包，您首先应该安装LangChain CLI:

```shell
pip install -U langchain-cli
```

要创建一个新的LangChain项目并将其安装为唯一的包，可以执行以下操作:

```shell
langchain app new my-app --package retrieval-agent-fireworks
```

如果您想将其添加到现有项目中，只需运行:

```shell
langchain app add retrieval-agent-fireworks
```

并将以下代码添加到您的`server.py`文件中:
```python
from retrieval_agent_fireworks import chain as retrieval_agent_fireworks_chain

add_routes(app, retrieval_agent_fireworks_chain, path="/retrieval-agent-fireworks")
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

这将启动FastAPI应用程序，服务器在本地运行，地址为
[http://localhost:8000](http://localhost:8000)

我们可以在[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)上查看所有模板
我们可以在[http://127.0.0.1:8000/retrieval-agent-fireworks/playground](http://127.0.0.1:8000/retrieval-agent-fireworks/playground)访问playground  

我们可以通过以下代码访问模板:

```python
from langserve.client import RemoteRunnable

runnable = RemoteRunnable("http://localhost:8000/retrieval-agent-fireworks")
```
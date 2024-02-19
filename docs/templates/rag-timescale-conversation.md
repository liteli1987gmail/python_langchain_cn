# 拉格-时间刻度-对话

这个模板用于[对话式](https://python.langchain.com/docs/expression_language/cookbook/retrieval#conversational-retrieval-chain)检索，这是最流行的LLM用例之一。

它将对话历史和检索到的文档传递给LLM进行综合。

## 环境设置

此模板使用Timescale Vector作为向量存储，并需要`TIMESCALES_SERVICE_URL`。如果您还没有帐户，请在此处注册90天试用版[here](https://console.cloud.timescale.com/signup?utm_campaign=vectorlaunch&utm_source=langchain&utm_medium=referral)。

要加载示例数据集，请设置`LOAD_SAMPLE_DATA=1`。要加载您自己的数据集，请参阅下面的部分。

设置`OPENAI_API_KEY`环境变量以访问OpenAI模型。

## 用法

要使用此包，您首先应该安装LangChain CLI：

```shell
pip install -U "langchain-cli[serve]"
```

要创建一个新的LangChain项目并将其安装为唯一的包，可以执行以下操作：

```shell
langchain app new my-app --package rag-timescale-conversation
```

如果要将其添加到现有项目中，只需运行：

```shell
langchain app add rag-timescale-conversation
```

并将以下代码添加到您的`server.py`文件中：
```python
from rag_timescale_conversation import chain as rag_timescale_conversation_chain

add_routes(app, rag_timescale_conversation_chain, path="/rag-timescale_conversation")
```

（可选）现在让我们配置LangSmith。
LangSmith将帮助我们跟踪、监视和调试LangChain应用程序。
LangSmith目前处于私有测试版，您可以在此处注册[here](https://smith.langchain.com/)。
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

这将在本地启动FastAPI应用程序，服务器正在运行在
[http://localhost:8000](http://localhost:8000)

我们可以在[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)上看到所有模板
我们可以在[http://127.0.0.1:8000/rag-timescale-conversation/playground](http://127.0.0.1:8000/rag-timescale-conversation/playground)上访问playground

我们可以通过以下代码访问模板：

```python
from langserve.client import RemoteRunnable

runnable = RemoteRunnable("http://localhost:8000/rag-timescale-conversation")
```

有关示例用法，请参阅`rag_conversation.ipynb`笔记本。

## 加载您自己的数据集

要加载您自己的数据集，您需要创建一个`load_dataset`函数。您可以在`load_sample_dataset.py`文件中定义的`load_ts_git_dataset`函数中看到一个示例。然后，您可以将其作为独立函数运行（例如在bash脚本中），或者将其添加到chain.py中（但是您应该只运行一次）。
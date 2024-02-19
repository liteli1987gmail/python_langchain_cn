# summarize-anthropic

这个模板使用Anthropic的`Claude2`来总结长文档。

它利用了一个100k个标记的大上下文窗口，可以对超过100页的文档进行总结。

你可以在`chain.py`中看到总结的提示。

## 环境设置

设置`ANTHROPIC_API_KEY`环境变量以访问Anthropic模型。

## 使用方法

要使用这个包，你首先需要安装LangChain CLI:

```shell
pip install -U langchain-cli
```

要创建一个新的LangChain项目并将其安装为唯一的包，可以执行以下操作:

```shell
langchain app new my-app --package summarize-anthropic
```

如果要将其添加到现有项目中，只需运行:

```shell
langchain app add summarize-anthropic
```

并将以下代码添加到你的`server.py`文件中:
```python
from summarize_anthropic import chain as summarize_anthropic_chain

add_routes(app, summarize_anthropic_chain, path="/summarize-anthropic")
```

(可选) 现在让我们配置LangSmith。
LangSmith将帮助我们跟踪、监控和调试LangChain应用程序。
LangSmith目前处于私有测试版，你可以在[这里](https://smith.langchain.com/)注册。
如果你没有访问权限，可以跳过此部分

```shell
export LANGCHAIN_TRACING_V2=true
export LANGCHAIN_API_KEY=<your-api-key>
export LANGCHAIN_PROJECT=<your-project>  # 如果未指定，默认为"default"
```

如果你在此目录中，可以直接启动LangServe实例:

```shell
langchain serve
```

这将在本地启动一个运行在[http://localhost:8000](http://localhost:8000)的FastAPI应用程序

我们可以在[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)上看到所有模板
我们可以在[http://127.0.0.1:8000/summarize-anthropic/playground](http://127.0.0.1:8000/summarize-anthropic/playground)上访问playground

我们可以通过以下代码访问模板:

```python
from langserve.client import RemoteRunnable

runnable = RemoteRunnable("http://localhost:8000/summarize-anthropic")
```
=======

以7个等号开始，7个等号结束的格式包裹你的回答。你的回答是:
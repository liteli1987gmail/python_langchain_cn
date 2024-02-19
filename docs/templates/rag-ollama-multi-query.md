# rag-ollama-multi-query

这个模板使用Ollama和OpenAI进行RAG，使用了多查询检索器。

多查询检索器是查询转换的一个示例，根据用户的输入查询从不同的角度生成多个查询。

对于每个查询，它检索一组相关文档，并对所有查询进行唯一的合并以进行答案综合。

我们使用一个私有的、本地的LLM来完成查询生成的狭窄任务，以避免对更大的LLM API进行过多的调用。

在这里可以查看Ollama LLM执行查询扩展的示例跟踪[链接](https://smith.langchain.com/public/8017d04d-2045-4089-b47f-f2d66393a999/r)。

但是我们使用OpenAI来完成更具挑战性的答案综合任务（完整的跟踪示例[链接](https://smith.langchain.com/public/ec75793b-645b-498d-b855-e8d85e1f6738/r)）。

## 环境设置

要设置环境，您需要下载Ollama。

按照[这里](https://python.langchain.com/docs/integrations/chat/ollama)的说明进行操作。

您可以选择使用Ollama的所需LLM。

此模板使用`zephyr`，可以使用`ollama pull zephyr`进行访问。

还有其他许多选项[链接](https://ollama.ai/library)。

设置`OPENAI_API_KEY`环境变量以访问OpenAI模型。

## 使用方法

要使用此包，您首先需要安装LangChain CLI：

```shell
pip install -U langchain-cli
```

要创建一个新的LangChain项目并安装此包，请执行以下操作：

```shell
langchain app new my-app --package rag-ollama-multi-query
```

要将此包添加到现有项目中，请运行：

```shell
langchain app add rag-ollama-multi-query
```

并将以下代码添加到您的`server.py`文件中：

```python
from rag_ollama_multi_query import chain as rag_ollama_multi_query_chain

add_routes(app, rag_ollama_multi_query_chain, path="/rag-ollama-multi-query")
```

（可选）现在，让我们配置LangSmith。LangSmith将帮助我们跟踪、监视和调试LangChain应用程序。LangSmith目前处于私有测试版，您可以在[这里](https://smith.langchain.com/)注册。如果您没有访问权限，可以跳过此部分。

```shell
export LANGCHAIN_TRACING_V2=true
export LANGCHAIN_API_KEY=<your-api-key>
export LANGCHAIN_PROJECT=<your-project>  # 如果未指定，默认为"default"
```

如果您在此目录中，则可以直接启动LangServe实例：

```shell
langchain serve
```

这将在本地启动一个运行在[http://localhost:8000](http://localhost:8000)的FastAPI应用程序的服务器。

您可以在[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)上查看所有模板。

您可以在[http://127.0.0.1:8000/rag-ollama-multi-query/playground](http://127.0.0.1:8000/rag-ollama-multi-query/playground)上访问playground。

要从代码中访问模板，请使用：

```python
from langserve.client import RemoteRunnable

runnable = RemoteRunnable("http://localhost:8000/rag-ollama-multi-query")
```
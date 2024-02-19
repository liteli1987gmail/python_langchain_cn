# sql-ollama

这个模板使用户能够使用自然语言与SQL数据库进行交互。

它使用[Zephyr-7b](https://huggingface.co/HuggingFaceH4/zephyr-7b-alpha)通过[Ollama](https://ollama.ai/library/zephyr)在Mac笔记本上本地运行推理。

## 环境设置

在使用此模板之前，您需要设置Ollama和SQL数据库。

1. 按照[这里](https://python.langchain.com/docs/integrations/chat/ollama)的说明下载Ollama。

2. 下载您感兴趣的LLM：

    * 此软件包使用`zephyr`：`ollama pull zephyr`
    * 您可以从[这里](https://ollama.ai/library)选择多个LLM

3. 此软件包包含一个2023年NBA名单的示例数据库。您可以在[这里](https://github.com/facebookresearch/llama-recipes/blob/main/demo_apps/StructuredLlama.ipynb)查看构建此数据库的说明。

## 使用方法

要使用此软件包，您首先需要安装LangChain CLI：

```shell
pip install -U langchain-cli
```

要创建一个新的LangChain项目并将其安装为唯一的软件包，可以执行以下操作：

```shell
langchain app new my-app --package sql-ollama
```

如果要将其添加到现有项目中，只需运行：

```shell
langchain app add sql-ollama
```

并将以下代码添加到您的`server.py`文件中：

```python
from sql_ollama import chain as sql_ollama_chain

add_routes(app, sql_ollama_chain, path="/sql-ollama")
```

（可选）现在让我们配置LangSmith。
LangSmith将帮助我们跟踪、监视和调试LangChain应用程序。
LangSmith目前处于私有测试版，您可以在[这里](https://smith.langchain.com/)注册。
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

这将在本地启动一个运行在[http://localhost:8000](http://localhost:8000)的FastAPI应用程序服务器

我们可以在[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)上查看所有模板
我们可以在[http://127.0.0.1:8000/sql-ollama/playground](http://127.0.0.1:8000/sql-ollama/playground)上访问playground

我们可以通过以下代码访问模板：

```python
from langserve.client import RemoteRunnable

runnable = RemoteRunnable("http://localhost:8000/sql-ollama")
```
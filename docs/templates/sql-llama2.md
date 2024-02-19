# sql-llama2

这个模板使用户能够使用自然语言与SQL数据库进行交互。

它使用由[Replicate](https://python.langchain.com/docs/integrations/llms/replicate)托管的LLamA2-13b，但可以适应支持LLaMA2的任何API，包括[Fireworks](https://python.langchain.com/docs/integrations/chat/fireworks)。

该模板包含一个2023年NBA名单的示例数据库。

有关如何构建此数据库的更多信息，请参见[此处](https://github.com/facebookresearch/llama-recipes/blob/main/demo_apps/StructuredLlama.ipynb)。

## 环境设置

确保在您的环境中设置了`REPLICATE_API_TOKEN`。

## 使用方法

要使用此包，您首先应该安装LangChain CLI：

```shell
pip install -U langchain-cli
```

要创建一个新的LangChain项目并将其安装为唯一的包，可以执行以下操作：

```shell
langchain app new my-app --package sql-llama2
```

如果要将其添加到现有项目中，只需运行：

```shell
langchain app add sql-llama2
```

并将以下代码添加到您的`server.py`文件中：
```python
from sql_llama2 import chain as sql_llama2_chain

add_routes(app, sql_llama2_chain, path="/sql-llama2")
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

这将在本地启动FastAPI应用程序，服务器正在运行在
[http://localhost:8000](http://localhost:8000)

我们可以在[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)上查看所有模板
我们可以在[http://127.0.0.1:8000/sql-llama2/playground](http://127.0.0.1:8000/sql-llama2/playground)上访问playground

我们可以通过以下代码访问模板：

```python
from langserve.client import RemoteRunnable

runnable = RemoteRunnable("http://localhost:8000/sql-llama2")
```
=======
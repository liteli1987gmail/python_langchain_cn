# rag-astradb

这个模板将使用Astra DB（`AstraDB`向量存储类）执行RAG。

## 环境设置

需要一个[Astra DB](https://astra.datastax.com)数据库；免费版即可。

- 您需要数据库的**API端点**（例如`https://0123...-us-east1.apps.astra.datastax.com`）...
- ...以及一个**令牌**（`AstraCS:...`）。

还需要一个**OpenAI API密钥**。请注意，默认情况下，此演示仅支持OpenAI，除非您调整代码。

通过环境变量提供连接参数和密钥。有关变量名称，请参考`.env.template`。

## 用法

要使用此软件包，您首先应该安装LangChain CLI：

```shell
pip install -U "langchain-cli[serve]"
```

要创建一个新的LangChain项目并将其安装为唯一的软件包，可以执行以下操作：

```shell
langchain app new my-app --package rag-astradb
```

如果要将其添加到现有项目中，只需运行：

```shell
langchain app add rag-astradb
```

并将以下代码添加到您的`server.py`文件中：
```python
from astradb_entomology_rag import chain as astradb_entomology_rag_chain

add_routes(app, astradb_entomology_rag_chain, path="/rag-astradb")
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

这将在本地启动FastAPI应用程序，服务器正在本地运行，地址为
[http://localhost:8000](http://localhost:8000)

我们可以在[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)上查看所有模板
我们可以在[http://127.0.0.1:8000/rag-astradb/playground](http://127.0.0.1:8000/rag-astradb/playground)上访问playground

我们可以通过以下代码访问模板：

```python
from langserve.client import RemoteRunnable

runnable = RemoteRunnable("http://localhost:8000/rag-astradb")
```

## 参考

具有LangServe链的独立存储库：[此处](https://github.com/hemidactylus/langserve_astradb_entomology_rag)。
# RAG with Multiple Indexes (Routing)

一个QA应用程序，根据用户的问题在不同的领域特定检索器之间进行路由。

## 环境设置

该应用程序查询PubMed、ArXiv、Wikipedia和[Kay AI](https://www.kay.ai)（用于SEC文件）。

您需要创建一个免费的Kay AI账户，并在[这里获取您的API密钥](https://www.kay.ai)。
然后设置环境变量：

```bash
export KAY_API_KEY="<YOUR_API_KEY>"
```

## 使用方法

要使用此软件包，您首先需要安装LangChain CLI：

```shell
pip install -U langchain-cli
```

要创建一个新的LangChain项目并将其安装为唯一的软件包，可以执行以下操作：

```shell
langchain app new my-app --package rag-multi-index-router
```

如果要将其添加到现有项目中，只需运行：

```shell
langchain app add rag-multi-index-router
```

并将以下代码添加到您的`server.py`文件中：
```python
from rag_multi_index_router import chain as rag_multi_index_router_chain

add_routes(app, rag_multi_index_router_chain, path="/rag-multi-index-router")
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

这将启动FastAPI应用程序，服务器在本地运行，地址为
[http://localhost:8000](http://localhost:8000)

我们可以在[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)上查看所有模板
我们可以在[http://127.0.0.1:8000/rag-multi-index-router/playground](http://127.0.0.1:8000/rag-multi-index-router/playground)上访问playground

我们可以通过以下代码访问模板：

```python
from langserve.client import RemoteRunnable

runnable = RemoteRunnable("http://localhost:8000/rag-multi-index-router")
```
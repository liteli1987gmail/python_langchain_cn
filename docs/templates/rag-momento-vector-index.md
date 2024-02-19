# rag-momento-vector-index

这个模板使用Momento Vector Index（MVI）和OpenAI执行RAG。

> MVI：最高效、最易于使用的无服务器向量索引，适用于您的数据。要开始使用MVI，只需注册一个帐户即可。无需处理基础架构、管理服务器或担心扩展性。MVI是一个根据您的需求自动扩展的服务。与其他Momento服务（如Momento Cache用于缓存提示和作为会话存储，或Momento Topics作为发布/订阅系统广播事件到您的应用程序）结合使用。

要注册并访问MVI，请访问[Momento控制台](https://console.gomomento.com/)。

## 环境设置

此模板使用Momento Vector Index作为向量存储，并要求设置`MOMENTO_API_KEY`和`MOMENTO_INDEX_NAME`。

前往[控制台](https://console.gomomento.com/)获取API密钥。

将`OPENAI_API_KEY`环境变量设置为访问OpenAI模型。

## 使用方法

要使用此软件包，您首先应该安装LangChain CLI：

```shell
pip install -U langchain-cli
```

要创建一个新的LangChain项目并将其安装为唯一的软件包，可以执行以下操作：

```shell
langchain app new my-app --package rag-momento-vector-index
```

如果要将其添加到现有项目中，只需运行：

```shell
langchain app add rag-momento-vector-index
```

并将以下代码添加到您的`server.py`文件中：

```python
from rag_momento_vector_index import chain as rag_momento_vector_index_chain

add_routes(app, rag_momento_vector_index_chain, path="/rag-momento-vector-index")
```

（可选）现在让我们配置LangSmith。
LangSmith将帮助我们跟踪、监视和调试LangChain应用程序。
LangSmith目前处于私有测试版，您可以在[此处](https://smith.langchain.com/)注册。
如果您没有访问权限，可以跳过此部分。

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
我们可以在[http://127.0.0.1:8000/rag-momento-vector-index/playground](http://127.0.0.1:8000/rag-momento-vector-index/playground)上访问playground

我们可以通过以下代码访问模板：

```python
from langserve.client import RemoteRunnable

runnable = RemoteRunnable("http://localhost:8000/rag-momento-vector-index")
```

## 数据索引

我们已经包含了一个用于索引数据的示例模块。该模块位于`rag_momento_vector_index/ingest.py`中。您将在`chain.py`中看到一个注释掉的行，用于调用此模块。取消注释以使用。
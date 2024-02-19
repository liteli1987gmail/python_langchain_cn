# rag-opensearch

这个模板使用[OpenSearch](https://python.langchain.com/docs/integrations/vectorstores/opensearch)执行RAG。

## 环境设置

设置以下环境变量。

- `OPENAI_API_KEY` - 用于访问OpenAI嵌入和模型。

如果不使用默认值，还可以选择设置OpenSearch的环境变量：

- `OPENSEARCH_URL` - 托管的OpenSearch实例的URL
- `OPENSEARCH_USERNAME` - OpenSearch实例的用户名
- `OPENSEARCH_PASSWORD` - OpenSearch实例的密码
- `OPENSEARCH_INDEX_NAME` - 索引的名称

要在docker中运行默认的OpenSeach实例，可以使用以下命令：
```shell
docker run -p 9200:9200 -p 9600:9600 -e "discovery.type=single-node" --name opensearch-node -d opensearchproject/opensearch:latest
```

注意：要加载名为`langchain-test`的虚拟索引和虚拟文档，请在包中运行`python dummy_index_setup.py`。

## 使用方法

要使用此包，首先应安装LangChain CLI：

```shell
pip install -U langchain-cli
```

要创建一个新的LangChain项目并将其安装为唯一的包，可以执行以下操作：

```shell
langchain app new my-app --package rag-opensearch
```

如果要将其添加到现有项目中，只需运行：

```shell
langchain app add rag-opensearch
```

并将以下代码添加到您的`server.py`文件中：
```python
from rag_opensearch import chain as rag_opensearch_chain

add_routes(app, rag_opensearch_chain, path="/rag-opensearch")
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

我们可以在[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)上查看所有模板。
我们可以在[http://127.0.0.1:8000/rag-opensearch/playground](http://127.0.0.1:8000/rag-opensearch/playground)上访问playground。

我们可以通过以下代码访问模板：

```python
from langserve.client import RemoteRunnable

runnable = RemoteRunnable("http://localhost:8000/rag-opensearch")
```
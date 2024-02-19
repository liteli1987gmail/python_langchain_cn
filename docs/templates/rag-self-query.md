# rag-self-query

这个模板使用自查询检索技术执行RAG。主要思想是让LLM将非结构化查询转换为结构化查询。有关此工作原理的更多信息，请参阅[文档](https://python.langchain.com/docs/modules/data_connection/retrievers/self_query)。

## 环境设置

在这个模板中，我们将使用OpenAI模型和Elasticsearch向量存储，但这种方法可以推广到所有LLMs/ChatModels和[一些向量存储](https://python.langchain.com/docs/integrations/retrievers/self_query/)。

设置`OPENAI_API_KEY`环境变量以访问OpenAI模型。

要连接到您的Elasticsearch实例，请使用以下环境变量：

```bash
export ELASTIC_CLOUD_ID = <ClOUD_ID>
export ELASTIC_USERNAME = <ClOUD_USERNAME>
export ELASTIC_PASSWORD = <ClOUD_PASSWORD>
```
对于使用Docker进行本地开发，请使用：

```bash
export ES_URL = "http://localhost:9200"
docker run -p 9200:9200 -e "discovery.type=single-node" -e "xpack.security.enabled=false" -e "xpack.security.http.ssl.enabled=false" docker.elastic.co/elasticsearch/elasticsearch:8.9.0
```

## 用法

要使用此包，您首先应该安装LangChain CLI：

```shell
pip install -U "langchain-cli[serve]"
```

要创建一个新的LangChain项目并将其安装为唯一的包，可以执行以下操作：

```shell
langchain app new my-app --package rag-self-query
```

如果要将其添加到现有项目中，只需运行：

```shell
langchain app add rag-self-query
```

并将以下代码添加到您的`server.py`文件中：
```python
from rag_self_query import chain

add_routes(app, chain, path="/rag-elasticsearch")
```

要使用示例数据填充向量存储，请从目录的根目录运行：
```bash
python ingest.py
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
我们可以在[http://127.0.0.1:8000/rag-elasticsearch/playground](http://127.0.0.1:8000/rag-elasticsearch/playground)上访问playground

我们可以通过以下代码访问模板：

```python
from langserve.client import RemoteRunnable

runnable = RemoteRunnable("http://localhost:8000/rag-self-query")
```
=======
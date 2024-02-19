# rag-elasticsearch

这个模板使用[ElasticSearch](https://python.langchain.com/docs/integrations/vectorstores/elasticsearch)执行RAG。

它依赖于句子转换器`MiniLM-L6-v2`来嵌入段落和问题。

## 环境设置

设置`OPENAI_API_KEY`环境变量以访问OpenAI模型。

要连接到您的Elasticsearch实例，请使用以下环境变量：

```bash
export ELASTIC_CLOUD_ID = <ClOUD_ID>
export ELASTIC_USERNAME = <ClOUD_USERNAME>
export ELASTIC_PASSWORD = <ClOUD_PASSWORD>
```
对于使用Docker进行本地开发，请使用：

```bash
export ES_URL="http://localhost:9200"
```

并在Docker中运行Elasticsearch实例：

```bash
docker run -p 9200:9200 -e "discovery.type=single-node" -e "xpack.security.enabled=false" -e "xpack.security.http.ssl.enabled=false" docker.elastic.co/elasticsearch/elasticsearch:8.9.0
```

## 用法

要使用此包，您首先应该安装LangChain CLI：

```shell
pip install -U langchain-cli
```

要创建一个新的LangChain项目并将其安装为唯一的包，可以执行以下操作：

```shell
langchain app new my-app --package rag-elasticsearch
```

如果要将其添加到现有项目中，只需运行：

```shell
langchain app add rag-elasticsearch
```

并将以下代码添加到您的`server.py`文件中：

```python
from rag_elasticsearch import chain as rag_elasticsearch_chain

add_routes(app, rag_elasticsearch_chain, path="/rag-elasticsearch")
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

我们可以在[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)上看到所有模板。
我们可以在[http://127.0.0.1:8000/rag-elasticsearch/playground](http://127.0.0.1:8000/rag-elasticsearch/playground)上访问playground。

我们可以通过以下代码访问模板：

```python
from langserve.client import RemoteRunnable

runnable = RemoteRunnable("http://localhost:8000/rag-elasticsearch")
```

要加载虚构的工作场所文档，请从此存储库的根目录运行以下命令：

```bash
python ingest.py
```

但是，您可以在[这里](https://python.langchain.com/docs/integrations/document_loaders)选择大量的文档加载器。  
=======
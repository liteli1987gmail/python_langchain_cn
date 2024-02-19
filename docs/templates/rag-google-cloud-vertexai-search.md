# rag-google-cloud-vertexai-search

这个模板是一个应用程序，利用了Google Vertex AI Search，一个机器学习驱动的搜索服务，和PaLM 2 for Chat (chat-bison)。该应用程序使用检索链来根据您的文档回答问题。

有关使用Vertex AI Search构建RAG应用程序的更多上下文信息，请查看[这里](https://cloud.google.com/generative-ai-app-builder/docs/enterprise-search-introduction)。

## 环境设置

在使用此模板之前，请确保您已经通过Vertex AI Search进行了身份验证。请参阅身份验证指南：[这里](https://cloud.google.com/generative-ai-app-builder/docs/authentication)。

您还需要创建：

- 一个搜索应用程序[这里](https://cloud.google.com/generative-ai-app-builder/docs/create-engine-es)
- 一个数据存储[这里](https://cloud.google.com/generative-ai-app-builder/docs/create-data-store-es)

一个适合测试此模板的数据集是Alphabet Earnings Reports，您可以在[这里](https://abc.xyz/investor/)找到。数据还可在`gs://cloud-samples-data/gen-app-builder/search/alphabet-investor-pdfs`中找到。

设置以下环境变量：

* `GOOGLE_CLOUD_PROJECT_ID` - 您的Google Cloud项目ID。
* `DATA_STORE_ID` - Vertex AI Search中的数据存储ID，在数据存储详细信息页面上可以找到一个36个字符的字母数字值。
* `MODEL_TYPE` - Vertex AI Search的模型类型。

## 使用方法

要使用此软件包，您首先需要安装LangChain CLI：

```shell
pip install -U langchain-cli
```

要创建一个新的LangChain项目并将其安装为唯一的软件包，可以执行以下操作：

```shell
langchain app new my-app --package rag-google-cloud-vertexai-search
```

如果要将其添加到现有项目中，只需运行：

```shell
langchain app add rag-google-cloud-vertexai-search
```

并将以下代码添加到您的`server.py`文件中：

```python
from rag_google_cloud_vertexai_search.chain import chain as rag_google_cloud_vertexai_search_chain

add_routes(app, rag_google_cloud_vertexai_search_chain, path="/rag-google-cloud-vertexai-search")
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

这将在本地启动一个运行在[http://localhost:8000](http://localhost:8000)的FastAPI应用程序的服务器

我们可以在[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)上看到所有模板
我们可以通过[http://127.0.0.1:8000/rag-google-cloud-vertexai-search/playground](http://127.0.0.1:8000/rag-google-cloud-vertexai-search/playground)访问playground

我们可以通过以下代码访问模板：

```python
from langserve.client import RemoteRunnable

runnable = RemoteRunnable("http://localhost:8000/rag-google-cloud-vertexai-search")
```

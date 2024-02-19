# rag-google-cloud-sensitive-data-protection

这个模板是一个应用程序，利用了Google Vertex AI Search，一个基于机器学习的搜索服务，和PaLM 2 for Chat（chat-bison）。该应用程序使用检索链来根据您的文档回答问题。

这个模板是一个应用程序，利用了Google敏感数据保护，一个用于检测和删除文本中敏感数据的服务，和PaLM 2 for Chat（chat-bison），尽管您可以使用任何模型。

有关使用敏感数据保护的更多上下文信息，请查看[这里](https://cloud.google.com/dlp/docs/sensitive-data-protection-overview)。

## 环境设置

在使用此模板之前，请确保在您的Google Cloud项目中启用了[DLP API](https://console.cloud.google.com/marketplace/product/google/dlp.googleapis.com)和[Vertex AI API](https://console.cloud.google.com/marketplace/product/google/aiplatform.googleapis.com)。

对于与Google Cloud相关的一些常见环境故障排除步骤，请参见本自述文件底部。

设置以下环境变量：

* `GOOGLE_CLOUD_PROJECT_ID` - 您的Google Cloud项目ID。
* `MODEL_TYPE` - Vertex AI Search的模型类型（例如`chat-bison`）

## 使用方法

要使用此软件包，您首先需要安装LangChain CLI：

```shell
pip install -U langchain-cli
```

要创建一个新的LangChain项目并将其安装为唯一的软件包，可以执行以下操作：

```shell
langchain app new my-app --package rag-google-cloud-sensitive-data-protection
```

如果要将其添加到现有项目中，只需运行：

```shell
langchain app add rag-google-cloud-sensitive-data-protection
```

并将以下代码添加到您的`server.py`文件中：

```python
from rag_google_cloud_sensitive_data_protection.chain import chain as rag_google_cloud_sensitive_data_protection_chain

add_routes(app, rag_google_cloud_sensitive_data_protection_chain, path="/rag-google-cloud-sensitive-data-protection")
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

这将在本地启动一个运行的FastAPI应用程序，服务器位于[http://localhost:8000](http://localhost:8000)

我们可以在[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)上看到所有模板
我们可以通过[http://127.0.0.1:8000/rag-google-cloud-vertexai-search/playground](http://127.0.0.1:8000/rag-google-cloud-vertexai-search/playground)访问playground

我们可以通过以下代码访问模板：

```python
from langserve.client import RemoteRunnable

runnable = RemoteRunnable("http://localhost:8000/rag-google-cloud-sensitive-data-protection")
```
```

# 故障排除Google Cloud

您可以使用`gcloud`的CLI设置您的`gcloud`凭据，使用`gcloud auth application-default login`

您可以使用以下命令设置您的`gcloud`项目
```bash
gcloud config set project <your project>
gcloud auth application-default set-quota-project <your project>
export GOOGLE_CLOUD_PROJECT_ID=<your project>
```

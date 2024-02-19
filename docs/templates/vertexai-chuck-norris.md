# vertexai-chuck-norris

这个模板使用Vertex AI PaLM2来制作关于Chuck Norris的笑话。

## 环境设置

首先，确保您拥有一个具有活动计费帐户的Google Cloud项目，并已安装[gcloud CLI](https://cloud.google.com/sdk/docs/install)。

配置[应用程序默认凭据](https://cloud.google.com/docs/authentication/provide-credentials-adc)：

```shell
gcloud auth application-default login
```

要设置要使用的默认Google Cloud项目，请运行此命令并设置要使用的项目的[项目ID](https://support.google.com/googleapi/answer/7014113?hl=en)：
```shell
gcloud config set project [PROJECT-ID]
```

为项目启用[Vertex AI API](https://console.cloud.google.com/apis/library/aiplatform.googleapis.com)：
```shell
gcloud services enable aiplatform.googleapis.com
```

## 用法

要使用此软件包，您首先应该安装LangChain CLI：

```shell
pip install -U langchain-cli
```

要创建一个新的LangChain项目并将其安装为唯一的软件包，可以执行以下操作：

```shell
langchain app new my-app --package pirate-speak
```

如果要将其添加到现有项目中，只需运行：

```shell
langchain app add vertexai-chuck-norris
```

并将以下代码添加到您的`server.py`文件中：
```python
from vertexai_chuck_norris.chain import chain as vertexai_chuck_norris_chain

add_routes(app, vertexai_chuck_norris_chain, path="/vertexai-chuck-norris")
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
我们可以在[http://127.0.0.1:8000/vertexai-chuck-norris/playground](http://127.0.0.1:8000/vertexai-chuck-norris/playground)访问playground

我们可以通过以下代码访问模板：

```python
from langserve.client import RemoteRunnable

runnable = RemoteRunnable("http://localhost:8000/vertexai-chuck-norris")
```
=======
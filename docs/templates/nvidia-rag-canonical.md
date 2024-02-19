=======

# nvidia-rag-canonical

这个模板使用Milvus Vector Store和NVIDIA模型（嵌入和聊天）执行RAG。

## 环境设置

您应该将您的NVIDIA API密钥导出为环境变量。
如果您没有NVIDIA API密钥，可以按照以下步骤创建一个：
1. 在[NVIDIA GPU云](https://catalog.ngc.nvidia.com/)服务上创建一个免费帐户，该服务托管AI解决方案目录、容器、模型等。
2. 导航到“Catalog > AI Foundation Models >（具有API端点的模型）”。
3. 选择“API”选项，然后点击“生成密钥”。
4. 将生成的密钥保存为“NVIDIA_API_KEY”。从那里，您将可以访问这些端点。

```shell
export NVIDIA_API_KEY=...
```

有关托管Milvus Vector Store的说明，请参阅底部的部分。

## 用法

要使用此包，您首先应该安装LangChain CLI：

```shell
pip install -U langchain-cli
```

要使用NVIDIA模型，请安装Langchain NVIDIA AI Endpoints包：
```shell
pip install -U langchain_nvidia_aiplay
```

要创建一个新的LangChain项目并将其安装为唯一的包，可以执行以下操作：

```shell
langchain app new my-app --package nvidia-rag-canonical
```

如果要将其添加到现有项目中，只需运行：

```shell
langchain app add nvidia-rag-canonical
```

并将以下代码添加到您的`server.py`文件中：
```python
from nvidia_rag_canonical import chain as nvidia_rag_canonical_chain

add_routes(app, nvidia_rag_canonical_chain, path="/nvidia-rag-canonical")
```

如果要设置摄取管道，可以将以下代码添加到您的`server.py`文件中：
```python
from nvidia_rag_canonical import ingest as nvidia_rag_ingest

add_routes(app, nvidia_rag_ingest, path="/nvidia-rag-ingest")
```
请注意，对于通过摄取API摄取的文件，需要重新启动服务器才能让新摄取的文件可被检索。

（可选）现在让我们配置LangSmith。
LangSmith将帮助我们跟踪、监视和调试LangChain应用程序。
LangSmith目前处于私有测试版，您可以在[此处](https://smith.langchain.com/)注册。
如果您没有访问权限，可以跳过此部分


```shell
export LANGCHAIN_TRACING_V2=true
export LANGCHAIN_API_KEY=<your-api-key>
export LANGCHAIN_PROJECT=<your-project>  # 如果未指定，默认为"default"
```

如果您还没有要连接的Milvus Vector Store，请在继续之前查看下面的`Milvus设置`部分。

如果您有要连接的Milvus Vector Store，请编辑`nvidia_rag_canonical/chain.py`中的连接详细信息。

如果您在此目录中，则可以直接启动LangServe实例：

```shell
langchain serve
```

这将启动FastAPI应用程序，服务器在本地运行，地址为
[http://localhost:8000](http://localhost:8000)

我们可以在[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)上查看所有模板
我们可以在[http://127.0.0.1:8000/nvidia-rag-canonical/playground](http://127.0.0.1:8000/nvidia-rag-canonical/playground)上访问playground

我们可以通过以下代码访问模板：

```python
from langserve.client import RemoteRunnable

runnable = RemoteRunnable("http://localhost:8000/nvidia-rag-canonical")
```


## Milvus设置

如果您需要创建Milvus Vector Store并摄取数据，请按照以下步骤操作。
我们首先遵循标准的Milvus设置说明[这里](https://milvus.io/docs/install_standalone-docker.md)。

1. 下载Docker Compose YAML文件。
    ```shell
    wget https://github.com/milvus-io/milvus/releases/download/v2.3.3/milvus-standalone-docker-compose.yml -O docker-compose.yml
    ```
2. 启动Milvus Vector Store容器
    ```shell
    sudo docker compose up -d
    ```
3. 安装PyMilvus包以与Milvus容器交互。
    ```shell
    pip install pymilvus
    ```
4. 现在让我们摄取一些数据！我们可以通过进入此目录并运行`ingest.py`中的代码来实现，例如：

    ```shell
    python ingest.py
    ```

    请注意，您可以（也应该！）将其更改为摄取您选择的数据。
=======
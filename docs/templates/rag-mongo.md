# rag-mongo

这个模板使用MongoDB和OpenAI执行RAG。

## 环境设置

您应该导出两个环境变量，一个是您的MongoDB URI，另一个是您的OpenAI API密钥。
如果您没有MongoDB URI，请参阅底部的“设置Mongo”部分以了解如何操作。

```shell
export MONGO_URI=...
export OPENAI_API_KEY=...
```

## 用法

要使用此包，您首先应该安装LangChain CLI：

```shell
pip install -U langchain-cli
```

要创建一个新的LangChain项目并将其安装为唯一的包，可以执行以下操作：

```shell
langchain app new my-app --package rag-mongo
```

如果要将其添加到现有项目中，只需运行：

```shell
langchain app add rag-mongo
```

并将以下代码添加到您的`server.py`文件中：
```python
from rag_mongo import chain as rag_mongo_chain

add_routes(app, rag_mongo_chain, path="/rag-mongo")
```

如果要设置摄取管道，可以将以下代码添加到您的`server.py`文件中：
```python
from rag_mongo import ingest as rag_mongo_ingest

add_routes(app, rag_mongo_ingest, path="/rag-mongo-ingest")
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

如果您尚未拥有要连接的Mongo搜索索引，请在继续之前查看下面的`MongoDB设置`部分。

如果您已经拥有要连接的MongoDB搜索索引，请编辑`rag_mongo/chain.py`中的连接详细信息。

如果您在此目录中，则可以直接启动LangServe实例：

```shell
langchain serve
```

这将启动FastAPI应用程序，服务器在本地运行，地址为
[http://localhost:8000](http://localhost:8000)

我们可以在[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)上查看所有模板
我们可以在[http://127.0.0.1:8000/rag-mongo/playground](http://127.0.0.1:8000/rag-mongo/playground)上访问playground

我们可以使用以下代码从代码中访问模板：

```python
from langserve.client import RemoteRunnable

runnable = RemoteRunnable("http://localhost:8000/rag-mongo")
```

有关更多上下文，请参阅[此笔记本](https://colab.research.google.com/drive/1cr2HBAHyBmwKUerJq2if0JaNhy-hIq7I#scrollTo=TZp7_CBfxTOB)。

## MongoDB设置

如果您需要设置MongoDB帐户并摄取数据，请执行以下步骤。
我们首先遵循标准的MongoDB Atlas设置说明[此处](https://www.mongodb.com/docs/atlas/getting-started/)。

1. 创建一个帐户（如果尚未完成）
2. 创建一个新项目（如果尚未完成）
3. 找到您的MongoDB URI。

可以通过转到部署概述页面并连接到您的数据库来完成此操作

然后查看可用的驱动程序

![显示用于连接到数据库的MongoDB Atlas驱动程序部分的屏幕截图。](https://github.com/langchain-ai/langchain/raw/master/templates/rag-mango/_images/driver.png "MongoDB Atlas驱动程序部分")

其中我们将看到我们的URI列出

![显示连接说明中MongoDB URI示例的屏幕截图。](https://github.com/langchain-ai/langchain/raw/master/templates/rag-mango/_images/uri.png "MongoDB URI示例")

然后将其设置为本地环境变量：

```shell
export MONGO_URI=...
```

4. 让我们还为OpenAI设置一个环境变量（我们将其用作LLM）

```shell
export OPENAI_API_KEY=...
```

5. 现在让我们摄取一些数据！我们可以通过进入此目录并运行`ingest.py`中的代码来实现，例如：

```shell
python ingest.py
```

请注意，您可以（也应该！）将其更改为摄取您选择的数据

6. 现在我们需要在我们的数据上设置一个向量索引。

我们首先可以连接到我们的数据库所在的集群

![显示MongoDB Atlas界面上显示集群概述的屏幕截图，其中有一个“连接”按钮。](https://github.com/langchain-ai/langchain/raw/master/templates/rag-mango/_images/cluster.png "MongoDB Atlas集群概述")

然后我们可以导航到列出所有集合的位置

![显示MongoDB Atlas界面上显示数据库内的集合概述的屏幕截图。](https://github.com/langchain-ai/langchain/raw/master/templates/rag-mango/_images/collections.png "MongoDB Atlas集合概述")

然后我们可以找到我们想要的集合并查看该集合的搜索索引

![显示MongoDB Atlas中特定集合的搜索索引部分的屏幕截图。](https://github.com/langchain-ai/langchain/raw/master/templates/rag-mango/_images/search-indexes.png "MongoDB Atlas搜索索引")

那可能是空的，我们想创建一个新的：

![在MongoDB Atlas中突出显示“创建索引”按钮的屏幕截图。](https://github.com/langchain-ai/langchain/raw/master/templates/rag-mango/_images/create.png "MongoDB Atlas创建索引按钮")

我们将使用JSON编辑器来创建它

![显示MongoDB Atlas中创建搜索索引的JSON编辑器选项的屏幕截图。](https://github.com/langchain-ai/langchain/raw/master/templates/rag-mango/_images/json_editor.png "MongoDB Atlas JSON编辑器选项")

然后我们将粘贴以下JSON：

```text
 {
   "mappings": {
     "dynamic": true,
     "fields": {
       "embedding": {
         "dimensions": 1536,
         "similarity": "cosine",
         "type": "knnVector"
       }
     }
   }
 }
```
![显示MongoDB Atlas中搜索索引的JSON配置的屏幕截图。](https://github.com/langchain-ai/langchain/raw/master/templates/rag-mango/_images/json.png "MongoDB Atlas搜索索引JSON配置")

然后，点击“下一步”，然后点击“创建搜索索引”。这可能需要一点时间，但是您应该可以在数据上拥有一个索引！
# hyde

这个模板使用了HyDE和RAG。

Hyde是一种检索方法，它代表着Hypothetical Document Embeddings（HyDE）。它是一种用于增强检索的方法，通过为传入的查询生成一个假设文档来实现。

然后将该文档进行嵌入，并利用该嵌入来查找与假设文档相似的真实文档。

其基本概念是假设文档在嵌入空间中可能比查询更接近。

有关更详细的描述，请参阅[此处](https://arxiv.org/abs/2212.10496)的论文。

## 环境设置

设置`OPENAI_API_KEY`环境变量以访问OpenAI模型。

## 使用方法

要使用此软件包，您首先应该安装LangChain CLI：

```shell
pip install -U langchain-cli
```

要创建一个新的LangChain项目并将其安装为唯一的软件包，可以执行以下操作：

```shell
langchain app new my-app --package hyde
```

如果要将其添加到现有项目中，只需运行：

```shell
langchain app add hyde
```

并将以下代码添加到您的`server.py`文件中：
```python
from hyde.chain import chain as hyde_chain

add_routes(app, hyde_chain, path="/hyde")
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
我们可以在[http://127.0.0.1:8000/hyde/playground](http://127.0.0.1:8000/hyde/playground)上访问playground

我们可以通过以下代码访问模板：

```python
from langserve.client import RemoteRunnable

runnable = RemoteRunnable("http://localhost:8000/hyde")
```

=======
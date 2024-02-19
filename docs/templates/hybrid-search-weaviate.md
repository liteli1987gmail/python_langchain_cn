# 在Weaviate中使用混合搜索
这个模板向您展示了如何在Weaviate中使用混合搜索功能。混合搜索结合了多个搜索算法，以提高搜索结果的准确性和相关性。

Weaviate使用稀疏向量和密集向量来表示搜索查询和文档的含义和上下文。结果使用`bm25`和向量搜索排名的组合来返回前几个结果。

## 配置
通过在`chain.py`中设置几个环境变量，连接到您托管的Weaviate Vectorstore：

* `WEAVIATE_ENVIRONMENT`
* `WEAVIATE_API_KEY`

您还需要设置您的`OPENAI_API_KEY`以使用OpenAI模型。

## 入门
要使用此包，您首先应该安装LangChain CLI：

```shell
pip install -U langchain-cli
```

要创建一个新的LangChain项目并将其安装为唯一的包，可以执行以下操作：

```shell
langchain app new my-app --package hybrid-search-weaviate
```

如果要将其添加到现有项目中，只需运行：

```shell
langchain app add hybrid-search-weaviate
```

并将以下代码添加到您的`server.py`文件中：
```python
from hybrid_search_weaviate import chain as hybrid_search_weaviate_chain

add_routes(app, hybrid_search_weaviate_chain, path="/hybrid-search-weaviate")
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
我们可以在[http://127.0.0.1:8000/hybrid-search-weaviate/playground](http://127.0.0.1:8000/hybrid-search-weaviate/playground)上访问playground

我们可以通过以下代码访问模板：

```python
from langserve.client import RemoteRunnable

runnable = RemoteRunnable("http://localhost:8000/hybrid-search-weaviate")
```
=======
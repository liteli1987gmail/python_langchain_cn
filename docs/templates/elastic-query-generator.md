# 弹性查询生成器

该模板允许使用LLMs以自然语言与Elasticsearch分析数据库进行交互。

它通过Elasticsearch DSL API（过滤器和聚合）构建搜索查询。

## 环境设置

将`OPENAI_API_KEY`环境变量设置为访问OpenAI模型。

### 安装Elasticsearch

有多种运行Elasticsearch的方法。然而，一种推荐的方法是通过Elastic Cloud。

在[Elastic Cloud](https://cloud.elastic.co/registration?utm_source=langchain&utm_content=langserve)上创建一个免费试用帐户。

通过部署，更新连接字符串。

密码和连接（elasticsearch url）可以在部署控制台上找到。

请注意，Elasticsearch客户端必须具有索引列表、映射描述和搜索查询的权限。

### 数据填充

如果您想用一些示例信息填充数据库，可以运行`python ingest.py`。

这将创建一个`customers`索引。在此软件包中，我们指定要针对生成查询的索引，并指定`["customers"]`。这是特定于设置您的Elastic索引的。

## 用法

要使用此软件包，您首先应该安装LangChain CLI：

```shell
pip install -U langchain-cli
```

要创建一个新的LangChain项目并将其安装为唯一的软件包，可以执行以下操作：

```shell
langchain app new my-app --package elastic-query-generator
```

如果要将其添加到现有项目中，只需运行：

```shell
langchain app add elastic-query-generator
```

并将以下代码添加到您的`server.py`文件中：
```python
from elastic_query_generator.chain import chain as elastic_query_generator_chain

add_routes(app, elastic_query_generator_chain, path="/elastic-query-generator")
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

如果您在此目录中，则可以通过以下方式直接启动LangServe实例：

```shell
langchain serve
```

这将在本地启动FastAPI应用程序，服务器正在运行在
[http://localhost:8000](http://localhost:8000)

我们可以在[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)上查看所有模板
我们可以在[http://127.0.0.1:8000/elastic-query-generator/playground](http://127.0.0.1:8000/elastic-query-generator/playground)访问playground

我们可以通过以下代码访问模板：

```python
from langserve.client import RemoteRunnable

runnable = RemoteRunnable("http://localhost:8000/elastic-query-generator")
```
=======
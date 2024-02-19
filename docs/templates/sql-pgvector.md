# sql-pgvector

这个模板使用户能够将`pgvector`与PostgreSQL结合使用，用于语义搜索和RAG。

它使用[PGVector](https://github.com/pgvector/pgvector)扩展，如[RAG empowered SQL cookbook](https://github.com/langchain-ai/langchain/blob/master/cookbook/retrieval_in_sql.ipynb)中所示。

## 环境设置

如果您使用`ChatOpenAI`作为您的LLM，请确保在您的环境中设置了`OPENAI_API_KEY`。您可以在`chain.py`中更改LLM和嵌入模型。

您可以配置以下环境变量以供模板使用（默认值在括号中）：

- `POSTGRES_USER`（postgres）
- `POSTGRES_PASSWORD`（test）
- `POSTGRES_DB`（vectordb）
- `POSTGRES_HOST`（localhost）
- `POSTGRES_PORT`（5432）

如果您没有postgres实例，可以在本地使用docker运行一个：

```bash
docker run \
  --name some-postgres \
  -e POSTGRES_PASSWORD=test \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_DB=vectordb \
  -p 5432:5432 \
  postgres:16
```

以后要重新启动，请使用上面定义的`--name`：
```bash
docker start some-postgres
```

### PostgreSQL数据库设置

除了启用`pgvector`扩展之外，您还需要进行一些设置，才能在SQL查询中运行语义搜索。

为了在您的postgreSQL数据库上运行RAG，您需要为您想要的特定列生成嵌入。

这个过程在[RAG empowered SQL cookbook](cookbook/retrieval_in_sql.ipynb)中有介绍，但总体方法包括：
1. 查询列中的唯一值
2. 为这些值生成嵌入
3. 将嵌入存储在单独的列或辅助表中。

## 使用方法

要使用此包，您首先应该安装LangChain CLI：

```shell
pip install -U langchain-cli
```

要创建一个新的LangChain项目并将其安装为唯一的包，可以执行以下操作：

```shell
langchain app new my-app --package sql-pgvector
```

如果要将其添加到现有项目中，只需运行：

```shell
langchain app add sql-pgvector
```

并将以下代码添加到您的`server.py`文件中：
```python
from sql_pgvector import chain as sql_pgvector_chain

add_routes(app, sql_pgvector_chain, path="/sql-pgvector")
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

这将在本地启动FastAPI应用程序，服务器正在[http://localhost:8000](http://localhost:8000)上运行

我们可以在[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)上查看所有模板
我们可以在[http://127.0.0.1:8000/sql-pgvector/playground](http://127.0.0.1:8000/sql-pgvector/playground)上访问playground

我们可以通过以下代码访问模板：

```python
from langserve.client import RemoteRunnable

runnable = RemoteRunnable("http://localhost:8000/sql-pgvector")
```
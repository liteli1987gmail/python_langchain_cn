# rag-redis

这个模板使用Redis（向量数据库）和OpenAI（LLM）对Nike的财务10k文件进行RAG。

它依赖于句子转换器`all-MiniLM-L6-v2`来嵌入pdf的块和用户问题。

## 环境设置

设置`OPENAI_API_KEY`环境变量以访问[OpenAI](https://platform.openai.com)模型：

```bash
export OPENAI_API_KEY= <YOUR OPENAI API KEY>
```

设置以下[Redis](https://redis.com/try-free)环境变量：

```bash
export REDIS_HOST = <YOUR REDIS HOST>
export REDIS_PORT = <YOUR REDIS PORT>
export REDIS_USER = <YOUR REDIS USER NAME>
export REDIS_PASSWORD = <YOUR REDIS PASSWORD>
```

## 支持的设置
我们使用各种环境变量来配置此应用程序

| 环境变量 | 描述                       | 默认值 |
|----------------------|-----------------------------------|---------------|
| `DEBUG`            | 启用或禁用Langchain调试日志       | True         |
| `REDIS_HOST`           | Redis服务器的主机名     | "localhost"   |
| `REDIS_PORT`           | Redis服务器的端口         | 6379          |
| `REDIS_USER`           | Redis服务器的用户         | "" |
| `REDIS_PASSWORD`       | Redis服务器的密码     | "" |
| `REDIS_URL`            | 连接到Redis的完整URL  | `None`，如果未提供，则从用户、密码、主机和端口构建 |
| `INDEX_NAME`           | 向量索引的名称          | "rag-redis"   |

## 用法

要使用此包，您首先应该在Python虚拟环境中安装LangChain CLI和Pydantic：

```shell
pip install -U langchain-cli pydantic==1.10.13
```

要创建一个新的LangChain项目并将其安装为唯一的包，可以执行以下操作：

```shell
langchain app new my-app --package rag-redis
```

如果要将其添加到现有项目中，只需运行：
```shell
langchain app add rag-redis
```

并将以下代码片段添加到您的`app/server.py`文件中：
```python
from rag_redis.chain import chain as rag_redis_chain

add_routes(app, rag_redis_chain, path="/rag-redis")
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
我们可以在[http://127.0.0.1:8000/rag-redis/playground](http://127.0.0.1:8000/rag-redis/playground)上访问playground

我们可以通过以下代码访问模板：

```python
from langserve.client import RemoteRunnable

runnable = RemoteRunnable("http://localhost:8000/rag-redis")
```
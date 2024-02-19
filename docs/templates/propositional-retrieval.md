# 命题检索

这个模板演示了Chen等人提出的多向量索引策略，详见[Dense X Retrieval: What Retrieval Granularity Should We Use?](https://arxiv.org/abs/2312.06648)。该模板使用LLM生成去上下文化的"命题"，并对其进行向量化以提高检索准确性。完整的定义可以在`proposal_chain.py`中查看。

![图示多向量索引策略的图表，展示了从维基百科数据经过命题化到FactoidWiki的过程，以及为QA模型检索信息单元的过程。](https://github.com/langchain-ai/langchain/raw/master/templates/propositional-retrieval/_images/retriever_diagram.png "检索器图表")

## 存储

在这个演示中，我们使用RecursiveUrlLoader对一篇简单的学术论文进行索引，并将所有检索器信息存储在本地（使用chroma和存储在本地文件系统上的bytestore）。您可以在`storage.py`中修改存储层。

## 环境设置

设置`OPENAI_API_KEY`环境变量以访问`gpt-3.5`和OpenAI嵌入类。

## 索引

通过运行以下命令来创建索引：

```python
poetry install
poetry run python propositional_retrieval/ingest.py
```

## 使用

要使用此包，您首先应该安装LangChain CLI：

```shell
pip install -U langchain-cli
```

要创建一个新的LangChain项目并将其安装为唯一的包，可以执行以下操作：

```shell
langchain app new my-app --package propositional-retrieval
```

如果要将其添加到现有项目中，只需运行：

```shell
langchain app add propositional-retrieval
```

并将以下代码添加到您的`server.py`文件中：

```python
from propositional_retrieval import chain

add_routes(app, chain, path="/propositional-retrieval")
```

（可选）现在让我们配置LangSmith。
LangSmith将帮助我们跟踪、监控和调试LangChain应用程序。
LangSmith目前处于私有测试版，您可以在[此处](https://smith.langchain.com/)注册。
如果您没有访问权限，可以跳过此部分。

```shell
export LANGCHAIN_TRACING_V2=true
export LANGCHAIN_API_KEY=<your-api-key>
export LANGCHAIN_PROJECT=<your-project>  # 如果未指定，默认为"default"
```

如果您在此目录中，则可以直接启动LangServe实例：

```shell
langchain serve
```

这将在本地启动一个运行在[http://localhost:8000](http://localhost:8000)的FastAPI应用程序服务器。

我们可以在[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)上查看所有模板。
我们可以在[http://127.0.0.1:8000/propositional-retrieval/playground](http://127.0.0.1:8000/propositional-retrieval/playground)上访问playground。

我们可以通过以下代码访问模板：

```python
from langserve.client import RemoteRunnable

runnable = RemoteRunnable("http://localhost:8000/propositional-retrieval")
```
=======

请确认以上翻译是否符合您的要求。
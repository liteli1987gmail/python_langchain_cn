# rag-conversation-zep

这个模板演示了如何使用Zep构建一个RAG对话应用程序。

这个模板包括以下内容：
- 使用[Zep文档集合](https://docs.getzep.com/sdk/documents/)填充一组文档（集合类似于其他向量数据库中的索引）。
- 使用Zep的[集成嵌入](https://docs.getzep.com/deployment/embeddings/)功能将文档嵌入为向量。
- 配置LangChain的[ZepVectorStore检索器](https://docs.getzep.com/sdk/documents/)，使用Zep的内置硬件加速的[最大边际相关性](https://docs.getzep.com/sdk/search_query/)（MMR）重新排序来检索文档。
- 提示、简单的聊天历史数据结构和构建RAG对话应用程序所需的其他组件。
- RAG对话链。

## 关于[Zep - 快速、可扩展的LLM应用构建块](https://www.getzep.com/)
Zep是一个用于生产化LLM应用的开源平台。无需重写代码，从在LangChain或LlamaIndex中构建的原型或自定义应用程序转到生产环境只需几分钟。

主要特点：

- 快速！Zep的异步提取器独立于聊天循环运行，确保用户体验流畅。
- 长期记忆持久性，可以访问历史消息，无论您的摘要策略如何。
- 基于可配置的消息窗口自动摘要记忆消息。一系列摘要被存储，为未来的摘要策略提供了灵活性。
- 在记忆和元数据上进行混合搜索，消息在创建时自动嵌入。
- 实体提取器自动从消息中提取命名实体，并将其存储在消息元数据中。
- 记忆和摘要的自动令牌计数，允许更精细地控制提示组装。
- Python和JavaScript SDK。

Zep项目：https://github.com/getzep/zep | 文档：https://docs.getzep.com/

## 环境设置

按照[快速入门指南](https://docs.getzep.com/deployment/quickstart/)设置Zep服务。

## 将文档导入Zep集合

运行`python ingest.py`将测试文档导入Zep集合。请查看文件以修改集合名称和文档来源。

## 使用方法

要使用此包，您首先应该安装LangChain CLI：

```shell
pip install -U "langchain-cli[serve]"
```

要创建一个新的LangChain项目并将其安装为唯一的包，可以执行以下操作：

```shell
langchain app new my-app --package rag-conversation-zep
```

如果要将其添加到现有项目中，只需运行：

```shell
langchain app add rag-conversation-zep
```

并将以下代码添加到您的`server.py`文件中：
```python
from rag_conversation_zep import chain as rag_conversation_zep_chain

add_routes(app, rag_conversation_zep_chain, path="/rag-conversation-zep")
```

（可选）现在让我们配置LangSmith。
LangSmith将帮助我们跟踪、监视和调试LangChain应用程序。
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

这将在本地启动FastAPI应用程序，服务器正在运行，地址为[http://localhost:8000](http://localhost:8000)

我们可以在[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)上查看所有模板。
我们可以在[http://127.0.0.1:8000/rag-conversation-zep/playground](http://127.0.0.1:8000/rag-conversation-zep/playground)上访问playground。

我们可以通过以下代码访问模板：

```python
from langserve.client import RemoteRunnable

runnable = RemoteRunnable("http://localhost:8000/rag-conversation-zep")
```
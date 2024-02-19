# rag-chroma-private

这个模板执行RAG，不依赖外部API。

它使用Ollama the LLM、GPT4All进行嵌入，并使用Chroma进行向量存储。

向量存储在`chain.py`中创建，默认索引了[关于Agents的热门博客文章](https://lilianweng.github.io/posts/2023-06-23-agent/)，用于问答。

## 环境设置

要设置环境，您需要下载Ollama。

按照[这里的说明](https://python.langchain.com/docs/integrations/chat/ollama)操作。

您可以选择使用Ollama的所需LLM。

此模板使用`llama2:7b-chat`，可以使用`ollama pull llama2:7b-chat`访问。

还有其他许多选项[在这里](https://ollama.ai/library)。

此软件包还使用[GPT4All](https://python.langchain.com/docs/integrations/text_embedding/gpt4all)嵌入。

## 用法

要使用此软件包，您首先需要安装LangChain CLI：

```shell
pip install -U langchain-cli
```

要创建一个新的LangChain项目并将其安装为唯一的软件包，可以执行以下操作：

```shell
langchain app new my-app --package rag-chroma-private
```

如果要将其添加到现有项目中，只需运行：

```shell
langchain app add rag-chroma-private
```

并将以下代码添加到您的`server.py`文件中：
```python
from rag_chroma_private import chain as rag_chroma_private_chain

add_routes(app, rag_chroma_private_chain, path="/rag-chroma-private")
```

（可选）现在让我们配置LangSmith。LangSmith将帮助我们跟踪、监视和调试LangChain应用程序。LangSmith目前处于私有测试版，您可以在[这里](https://smith.langchain.com/)注册。如果您没有访问权限，可以跳过此部分

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
我们可以在[http://127.0.0.1:8000/rag-chroma-private/playground](http://127.0.0.1:8000/rag-chroma-private/playground)上访问playground

我们可以通过以下方式从代码中访问模板：

```python
from langserve.client import RemoteRunnable

runnable = RemoteRunnable("http://localhost:8000/rag-chroma-private")
```

该软件包将在`chain.py`中创建并添加文档到向量数据库。默认情况下，它将加载一篇关于agents的热门博客文章。但是，您可以从[这里](https://python.langchain.com/docs/integrations/document_loaders)选择大量的文档加载器。
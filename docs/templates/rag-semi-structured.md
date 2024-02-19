# rag-semi-structured

这个模板用于对半结构化数据进行RAG分析，例如包含文本和表格的PDF文件。

参考[这个教程](https://github.com/langchain-ai/langchain/blob/master/cookbook/Semi_Structured_RAG.ipynb)。

## 环境设置

设置`OPENAI_API_KEY`环境变量以访问OpenAI模型。

这里使用[Unstructured](https://unstructured-io.github.io/unstructured/)进行PDF解析，需要进行一些系统级的软件包安装。

在Mac上，可以使用以下命令安装所需的软件包：

```shell
brew install tesseract poppler
```

## 使用方法

要使用这个包，首先需要安装LangChain CLI：

```shell
pip install -U langchain-cli
```

要创建一个新的LangChain项目并将其安装为唯一的包，可以执行以下命令：

```shell
langchain app new my-app --package rag-semi-structured
```

如果要将其添加到现有项目中，只需运行：

```shell
langchain app add rag-semi-structured
```

并将以下代码添加到`server.py`文件中：
```python
from rag_semi_structured import chain as rag_semi_structured_chain

add_routes(app, rag_semi_structured_chain, path="/rag-semi-structured")
```

（可选）现在让我们配置LangSmith。
LangSmith将帮助我们跟踪、监视和调试LangChain应用程序。
LangSmith目前处于私有测试版，您可以在[这里](https://smith.langchain.com/)注册。
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

这将在本地启动FastAPI应用程序，服务器运行在
[http://localhost:8000](http://localhost:8000)

我们可以在[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)上查看所有模板。
我们可以在[http://127.0.0.1:8000/rag-semi-structured/playground](http://127.0.0.1:8000/rag-semi-structured/playground)上访问playground。

我们可以通过以下代码访问模板：

```python
from langserve.client import RemoteRunnable

runnable = RemoteRunnable("http://localhost:8000/rag-semi-structured")
```

有关如何连接到模板的更多详细信息，请参考Jupyter笔记本`rag_semi_structured`。
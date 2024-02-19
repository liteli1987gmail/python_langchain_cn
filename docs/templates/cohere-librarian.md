# cohere-librarian

这个模板将Cohere转变成了一个图书管理员。

它演示了使用路由器在处理不同事物的链之间进行切换的方法：一个带有Cohere嵌入的向量数据库；一个具有关于图书馆的一些信息的提示的聊天机器人；最后是一个可以访问互联网的RAG聊天机器人。

如果要进行更完整的书籍推荐演示，请考虑使用以下数据集中的更大样本替换books_with_blurbs.csv：https://www.kaggle.com/datasets/jdobrow/57000-books-with-metadata-and-blurbs/。

## 环境设置

将`COHERE_API_KEY`环境变量设置为访问Cohere模型。

## 使用方法

要使用此包，您首先应该安装LangChain CLI：

```shell
pip install -U langchain-cli
```

要创建一个新的LangChain项目并将其安装为唯一的包，可以执行以下操作：

```shell
langchain app new my-app --package cohere-librarian
```

如果要将其添加到现有项目中，只需运行：

```shell
langchain app add cohere-librarian
```

并将以下代码添加到您的`server.py`文件中：
```python
from cohere_librarian.chain import chain as cohere_librarian_chain

add_routes(app, cohere_librarian_chain, path="/cohere-librarian")
```

（可选）现在让我们配置LangSmith。
LangSmith将帮助我们跟踪、监视和调试LangChain应用程序。
LangSmith目前处于私有测试版，您可以在此处注册：[https://smith.langchain.com/](https://smith.langchain.com/)。
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

这将启动FastAPI应用程序，服务器在本地运行，地址为
[http://localhost:8000](http://localhost:8000)

我们可以在[http://localhost:8000/docs](http://localhost:8000/docs)上查看所有模板
我们可以在[http://localhost:8000/cohere-librarian/playground](http://localhost:8000/cohere-librarian/playground)上访问playground

我们可以通过以下代码访问模板：

```python
from langserve.client import RemoteRunnable

runnable = RemoteRunnable("http://localhost:8000/cohere-librarian")
```
=======
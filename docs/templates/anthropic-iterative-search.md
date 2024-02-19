# 人类迭代搜索

这个模板将创建一个虚拟研究助手，能够搜索维基百科以找到你的问题的答案。

它受到[这个笔记本](https://github.com/anthropics/anthropic-cookbook/blob/main/long_context/wikipedia-search-cookbook.ipynb)的启发。

## 环境设置

设置`ANTHROPIC_API_KEY`环境变量以访问Anthropic模型。

## 使用方法

要使用这个包，你首先应该安装LangChain CLI:

```shell
pip install -U langchain-cli
```

要创建一个新的LangChain项目并将其安装为唯一的包，可以执行以下操作:

```shell
langchain app new my-app --package anthropic-iterative-search
```

如果你想将其添加到现有项目中，只需运行:

```shell
langchain app add anthropic-iterative-search
```

并将以下代码添加到你的`server.py`文件中:
```python
from anthropic_iterative_search import chain as anthropic_iterative_search_chain

add_routes(app, anthropic_iterative_search_chain, path="/anthropic-iterative-search")
```

（可选）现在让我们配置LangSmith。
LangSmith将帮助我们跟踪、监视和调试LangChain应用程序。
LangSmith目前处于私有测试版，你可以在[这里](https://smith.langchain.com/)注册。
如果你没有访问权限，可以跳过此部分


```shell
export LANGCHAIN_TRACING_V2=true
export LANGCHAIN_API_KEY=<your-api-key>
export LANGCHAIN_PROJECT=<your-project>  # 如果未指定，默认为"default"
```

如果你在这个目录下，你可以直接启动一个LangServe实例:

```shell
langchain serve
```

这将启动一个FastAPI应用程序，服务器在本地运行，地址为
[http://localhost:8000](http://localhost:8000)

我们可以在[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)上看到所有模板
我们可以在[http://127.0.0.1:8000/anthropic-iterative-search/playground](http://127.0.0.1:8000/anthropic-iterative-search/playground)上访问playground

我们可以通过以下代码访问模板:

```python
from langserve.client import RemoteRunnable

runnable = RemoteRunnable("http://localhost:8000/anthropic-iterative-search")
```
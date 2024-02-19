# python-lint

这个代理专门用于生成高质量的Python代码，重点是正确的格式和代码检查。它使用`black`，`ruff`和`mypy`来确保代码符合标准的质量检查。

通过集成和响应这些检查，简化了编码过程，从而产生可靠和一致的代码输出。

它实际上不能执行它所编写的代码，因为代码执行可能引入额外的依赖和潜在的安全漏洞。这使得该代理成为代码生成任务的安全和高效解决方案。

您可以直接使用它来生成Python代码，或者与规划和执行代理进行网络连接。

## 环境设置

- 安装`black`，`ruff`和`mypy`：`pip install -U black ruff mypy`
- 设置`OPENAI_API_KEY`环境变量。

## 用法

要使用此软件包，您首先应该安装LangChain CLI：

```shell
pip install -U langchain-cli
```

要创建一个新的LangChain项目并将其安装为唯一的软件包，可以执行以下操作：

```shell
langchain app new my-app --package python-lint
```

如果要将其添加到现有项目中，只需运行：

```shell
langchain app add python-lint
```

并将以下代码添加到您的`server.py`文件中：
```python
from python_lint import agent_executor as python_lint_agent

add_routes(app, python_lint_agent, path="/python-lint")
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

这将在本地启动一个运行在[http://localhost:8000](http://localhost:8000)的FastAPI应用程序服务器

我们可以在[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)上查看所有模板
我们可以在[http://127.0.0.1:8000/python-lint/playground](http://127.0.0.1:8000/python-lint/playground)上访问playground

我们可以通过以下代码访问模板：

```python
from langserve.client import RemoteRunnable

runnable = RemoteRunnable("http://localhost:8000/python-lint")
```
=======
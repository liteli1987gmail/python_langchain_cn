# stepback-qa-prompting

这个模板复制了“Step-Back”提示技术，通过首先提出一个“step back”问题来提高复杂问题的表现。

这个技术可以与常规的问答应用程序结合使用，通过对原始问题和“step back”问题进行检索。

在这个模板中，我们将稍微修改提示，以便与聊天模型更好地配合使用。

## 环境设置

设置`OPENAI_API_KEY`环境变量以访问OpenAI模型。

## 使用方法

要使用此包，您首先应该安装LangChain CLI：

```shell
pip install -U langchain-cli
```

要创建一个新的LangChain项目并将其安装为唯一的包，可以执行以下操作：

```shell
langchain app new my-app --package stepback-qa-prompting
```

如果要将其添加到现有项目中，只需运行：

```shell
langchain app add stepback-qa-prompting
```

并将以下代码添加到您的`server.py`文件中：
```python
from stepback_qa_prompting.chain import chain as stepback_qa_prompting_chain

add_routes(app, stepback_qa_prompting_chain, path="/stepback-qa-prompting")
```

（可选）现在让我们配置LangSmith。
LangSmith将帮助我们跟踪、监视和调试LangChain应用程序。
LangSmith目前处于私有测试版，您可以在此处注册[here](https://smith.langchain.com/)。
如果您没有访问权限，可以跳过此部分。

```shell
export LANGCHAIN_TRACING_V2=true
export LANGCHAIN_API_KEY=<your-api-key>
export LANGCHAIN_PROJECT=<your-project>  # if not specified, defaults to "default"
```

如果您在此目录中，则可以直接启动LangServe实例：

```shell
langchain serve
```

这将在本地启动一个运行的FastAPI应用程序服务器，地址为：
[http://localhost:8000](http://localhost:8000)

我们可以在[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)上查看所有模板。
我们可以在[http://127.0.0.1:8000/stepback-qa-prompting/playground](http://127.0.0.1:8000/stepback-qa-prompting/playground)上访问playground。

我们可以通过以下代码访问模板：

```python
from langserve.client import RemoteRunnable

runnable = RemoteRunnable("http://localhost:8000/stepback-qa-prompting")
```
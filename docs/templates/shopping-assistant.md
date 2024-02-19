# 购物助手

这个模板创建了一个购物助手，帮助用户找到他们正在寻找的产品。

这个模板将使用`Ionic`来搜索产品。

## 环境设置

这个模板默认使用`OpenAI`。
请确保在您的环境中设置了`OPENAI_API_KEY`。

## 使用方法

要使用这个包，您首先应该安装LangChain CLI:

```shell
pip install -U langchain-cli
```

要创建一个新的LangChain项目并将其安装为唯一的包，可以执行以下操作:

```shell
langchain app new my-app --package shopping-assistant
```

如果您想将其添加到现有项目中，只需运行:

```shell
langchain app add shopping-assistant
```

并将以下代码添加到您的`server.py`文件中:
```python
from shopping_assistant.agent import agent_executor as shopping_assistant_chain

add_routes(app, shopping_assistant_chain, path="/shopping-assistant")
```

(可选) 现在让我们配置LangSmith。
LangSmith将帮助我们跟踪、监控和调试LangChain应用程序。
LangSmith目前处于私有测试版，您可以在[这里](https://smith.langchain.com/)注册。
如果您没有访问权限，可以跳过此部分


```shell
export LANGCHAIN_TRACING_V2=true
export LANGCHAIN_API_KEY=<your-api-key>
export LANGCHAIN_PROJECT=<your-project>  # 如果未指定，默认为"default"
```

如果您在此目录中，则可以直接启动LangServe实例:

```shell
langchain serve
```

这将在本地启动一个运行在[http://localhost:8000](http://localhost:8000)的FastAPI应用程序的服务器

我们可以在[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)上查看所有模板
我们可以在[http://127.0.0.1:8000/shopping-assistant/playground](http://127.0.0.1:8000/shopping-assistant/playground)上访问playground

我们可以通过以下代码访问模板:

```python
from langserve.client import RemoteRunnable

runnable = RemoteRunnable("http://localhost:8000/shopping-assistant")
```
=======
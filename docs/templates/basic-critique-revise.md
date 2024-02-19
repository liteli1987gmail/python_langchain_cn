# 基本评论修订

迭代生成模式候选并根据错误进行修订。

## 环境设置

此模板使用OpenAI函数调用，因此您需要设置`OPENAI_API_KEY`环境变量才能使用此模板。

## 用法

要使用此包，您首先需要安装LangChain CLI：

```shell
pip install -U "langchain-cli[serve]"
```

要创建一个新的LangChain项目并将其安装为唯一的包，可以执行以下操作：

```shell
langchain app new my-app --package basic-critique-revise
```

如果要将其添加到现有项目中，只需运行：

```shell
langchain app add basic-critique-revise
```

并将以下代码添加到您的`server.py`文件中：
```python
from basic_critique_revise import chain as basic_critique_revise_chain

add_routes(app, basic_critique_revise_chain, path="/basic-critique-revise")
```

（可选）现在让我们配置LangSmith。
LangSmith将帮助我们跟踪、监视和调试LangChain应用程序。
LangSmith目前处于私有测试版，您可以在此处注册[here](https://smith.langchain.com/)。
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

我们可以在[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)上查看所有模板
我们可以在[http://127.0.0.1:8000/basic-critique-revise/playground](http://127.0.0.1:8000/basic-critique-revise/playground)上访问playground

我们可以通过以下代码访问模板：

```python
from langserve.client import RemoteRunnable

runnable = RemoteRunnable("http://localhost:8000/basic-critique-revise")
```
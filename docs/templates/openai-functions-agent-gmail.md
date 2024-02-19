# OpenAI Functions Agent - Gmail

曾经为了达到收件箱零的目标而苦苦挣扎过吗？

使用这个模板，您可以创建和定制自己的AI助手来管理您的Gmail帐户。使用默认的Gmail工具，它可以阅读、搜索和起草邮件，以代表您进行回复。它还可以访问Tavily搜索引擎，以便在撰写邮件之前搜索与邮件线程中的任何主题或人物相关的信息，确保草稿包含所有必要的相关信息，以表达出您对该主题的了解。


## 详细信息

该助手使用OpenAI的[函数调用](https://python.langchain.com/docs/modules/chains/how_to/openai_functions)支持可靠地选择和调用您提供的工具。

该模板还直接从[langchain-core](https://pypi.org/project/langchain-core/)和[`langchain-community`](https://pypi.org/project/langchain-community/)导入适当的内容。我们已经重新组织了LangChain，让您可以选择适合您用例的特定集成。虽然您仍然可以从`langchain`导入（我们正在使此过渡向后兼容），但我们已经将大多数类的主页分开，以反映所有权并使您的依赖列表更轻。您需要的大多数集成可以在`langchain-community`包中找到，如果您只是使用核心表达语言API，甚至可以完全基于`langchain-core`构建。

## 环境设置

需要设置以下环境变量：

将`OPENAI_API_KEY`环境变量设置为访问OpenAI模型。

将`TAVILY_API_KEY`环境变量设置为访问Tavily搜索。

创建一个包含来自Gmail的OAuth客户端ID的[`credentials.json`](https://developers.google.com/gmail/api/quickstart/python#authorize_credentials_for_a_desktop_application)文件。要自定义身份验证，请参阅下面的[自定义身份验证](#customize-auth)部分。

_*注意：第一次运行此应用程序时，它将强制您进行用户身份验证流程。_

（可选）：将`GMAIL_AGENT_ENABLE_SEND`设置为`true`（或修改此模板中的`agent.py`文件），以使其可以访问“发送”工具。这将使您的助手有权限代表您发送电子邮件，而无需您明确审查，这是不推荐的。

## 用法

要使用此软件包，您首先应该安装LangChain CLI：

```shell
pip install -U langchain-cli
```

要创建一个新的LangChain项目并将其安装为唯一的软件包，可以执行以下操作：

```shell
langchain app new my-app --package openai-functions-agent-gmail
```

如果要将其添加到现有项目中，只需运行：

```shell
langchain app add openai-functions-agent-gmail
```

并将以下代码添加到您的`server.py`文件中：
```python
from openai_functions_agent import agent_executor as openai_functions_agent_chain

add_routes(app, openai_functions_agent_chain, path="/openai-functions-agent-gmail")
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

这将启动FastAPI应用程序，服务器在本地运行，地址为
[http://localhost:8000](http://localhost:8000)

我们可以在[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)上查看所有模板
我们可以在[http://127.0.0.1:8000/openai-functions-agent-gmail/playground](http://127.0.0.1:8000/openai-functions-agent/playground)上访问playground

我们可以通过以下代码访问模板：

```python
from langserve.client import RemoteRunnable

runnable = RemoteRunnable("http://localhost:8000/openai-functions-agent-gmail")
```

## 自定义身份验证

```
from langchain_community.tools.gmail.utils import build_resource_service, get_gmail_credentials

# 可在此处查看范围 https://developers.google.com/gmail/api/auth/scopes
# 例如，只读范围是 'https://www.googleapis.com/auth/gmail.readonly'
credentials = get_gmail_credentials(
    token_file="token.json",
    scopes=["https://mail.google.com/"],
    client_secrets_file="credentials.json",
)
api_resource = build_resource_service(credentials=credentials)
toolkit = GmailToolkit(api_resource=api_resource)
```
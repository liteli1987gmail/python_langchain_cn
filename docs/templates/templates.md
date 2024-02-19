# LangChain模板

LangChain模板是构建生产就绪LLM应用程序的最简单和最快的方法。
这些模板作为一组参考架构，适用于各种流行的LLM用例。
它们都采用标准格式，可以轻松地使用[LangServe](https://github.com/langchain-ai/langserve)部署它们。

🚩我们将发布LangServe的托管版本，以便一键部署LangChain应用程序。[在这里注册](https://airtable.com/app0hN6sd93QcKubv/shrAjst60xXa6quV2)加入等待列表。

## 快速入门

首先安装LangChain CLI。

```shell
pip install -U langchain-cli
```

接下来，创建一个新的LangChain项目：

```shell
langchain app new my-app
```

这将创建一个名为`my-app`的新目录，其中包含两个文件夹：

- `app`：这是LangServe代码的存放位置
- `packages`：这是您的链或代理的存放位置

要将现有模板作为包引入，请先进入新项目：

```shell
cd my-app
```

然后将模板添加为项目。
在这个入门指南中，我们将添加一个简单的`pirate-speak`项目。
这个项目的作用是将用户输入转换为海盗语言。

```shell
langchain app add pirate-speak
```

这将把指定的模板拉入`packages/pirate-speak`中。

然后会提示您是否要安装它。
这相当于运行`pip install -e packages/pirate-speak`。
通常应该接受此操作（或之后运行相同的命令）。
我们使用`-e`进行安装，以便如果您修改模板（您很可能会这样做），更改会得到更新。

之后，它会询问您是否要为此项目生成路由代码。
这是您需要添加到应用程序中以开始使用此链的代码。
如果我们接受，将会生成以下代码：

```shell
from pirate_speak.chain import chain as pirate_speak_chain

add_routes(app, pirate_speak_chain, path="/pirate-speak")
```

现在您可以编辑您拉取下来的模板。
您可以更改`packages/pirate-speak`中的代码文件以使用不同的模型、不同的提示、不同的逻辑。
请注意，上述代码片段始终期望最终的链可作为`from pirate_speak.chain import chain`导入，
因此您应该保持包的结构足够相似以尊重该代码片段，或者准备更新该代码片段。

完成所需的更改后，
为了使LangServe使用此项目，您需要修改`app/server.py`。
具体来说，您应该将上述代码片段添加到`app/server.py`中，使文件如下所示：

```python
from fastapi import FastAPI
from langserve import add_routes
from pirate_speak.chain import chain as pirate_speak_chain

app = FastAPI()

add_routes(app, pirate_speak_chain, path="/pirate-speak")
```

（可选）现在让我们配置LangSmith。
LangSmith将帮助我们跟踪、监视和调试LangChain应用程序。
LangSmith目前处于私有测试版，您可以在[这里](https://smith.langchain.com/)注册。
如果您没有访问权限，可以跳过此部分


```shell
export LANGCHAIN_TRACING_V2=true
export LANGCHAIN_API_KEY=<your-api-key>
export LANGCHAIN_PROJECT=<your-project>  # 如果未指定，默认为"default"
```

对于这个特定的应用程序，我们将使用OpenAI作为LLM，所以我们需要导出我们的OpenAI API密钥：

```shell
export OPENAI_API_KEY=sk-...
```

然后，通过运行以下命令，您可以启动生产就绪的端点以及一个playground：

```shell
langchain serve
```

现在您拥有了一个完全部署的LangServe应用程序。
例如，您可以在[http://127.0.0.1:8000/pirate-speak/playground/](http://127.0.0.1:8000/pirate-speak/playground/)上获得一个开箱即用的playground：

![LangServe Playground界面的屏幕截图，显示输入和输出字段，演示海盗语言转换。](/img/playground.png "LangServe Playground界面")

在[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)上访问API文档

![API文档界面的屏幕截图，显示pirate-speak应用程序的可用端点。](/img/docs.png "API文档界面")

使用LangServe的Python或JS SDK与API进行交互，就像与常规的[Runnable](https://python.langchain.com/docs/expression_language/)一样。

```python
from langserve import RemoteRunnable

api = RemoteRunnable("http://127.0.0.1:8000/pirate-speak")
api.invoke({"text": "hi"})
```

快速入门到此结束！
您已成功下载了第一个模板，并使用LangServe部署了它。


## 其他资源

### [模板索引](docs/INDEX.md)

探索可用于各种高级RAG到代理的许多模板。

### [贡献](docs/CONTRIBUTING.md)

想要贡献自己的模板吗？这很简单！这些说明介绍了如何进行贡献。

### [从包中启动LangServe](docs/LAUNCHING_PACKAGE.md)

您还可以直接从包中启动LangServe（而无需创建新项目）。
这些说明介绍了如何做到这一点。
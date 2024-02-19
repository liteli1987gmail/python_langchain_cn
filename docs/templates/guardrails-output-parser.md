# guardrails-output-parser

此模板使用 [guardrails-ai](https://github.com/guardrails-ai/guardrails) 来验证 LLM 输出。

`GuardrailsOutputParser` 设置在 `chain.py` 中。

默认示例用于防止使用不雅语言。

## 环境设置

将 `OPENAI_API_KEY` 环境变量设置为访问 OpenAI 模型。

## 使用方法

要使用此包，您首先应该安装 LangChain CLI：

```shell
pip install -U langchain-cli
```

要创建一个新的 LangChain 项目并将其安装为唯一的包，可以执行以下操作：

```shell
langchain app new my-app --package guardrails-output-parser
```

如果要将其添加到现有项目中，只需运行：

```shell
langchain app add guardrails-output-parser
```

并将以下代码添加到您的 `server.py` 文件中：
```python
from guardrails_output_parser.chain import chain as guardrails_output_parser_chain

add_routes(app, guardrails_output_parser_chain, path="/guardrails-output-parser")
```

（可选）现在让我们配置 LangSmith。
LangSmith 将帮助我们跟踪、监控和调试 LangChain 应用程序。
LangSmith 目前处于私有测试版，您可以在此处注册 [here](https://smith.langchain.com/)。
如果您没有访问权限，可以跳过此部分。

```shell
export LANGCHAIN_TRACING_V2=true
export LANGCHAIN_API_KEY=<your-api-key>
export LANGCHAIN_PROJECT=<your-project>  # 如果未指定，默认为 "default"
```

如果您在此目录中，则可以直接启动 LangServe 实例：

```shell
langchain serve
```

这将启动 FastAPI 应用程序，服务器在本地运行，地址为
[http://localhost:8000](http://localhost:8000)

我们可以在 [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) 上查看所有模板。
我们可以在 [http://127.0.0.1:8000/guardrails-output-parser/playground](http://127.0.0.1:8000/guardrails-output-parser/playground) 上访问 playground。

我们可以通过以下代码访问模板：

```python
from langserve.client import RemoteRunnable

runnable = RemoteRunnable("http://localhost:8000/guardrails-output-parser")
```

如果 Guardrails 没有发现任何不雅语言，则返回翻译后的输出。如果 Guardrails 发现不雅语言，则返回空字符串。
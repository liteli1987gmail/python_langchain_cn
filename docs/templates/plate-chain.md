# plate-chain

这个模板可以解析实验室板的数据。

在生物化学或分子生物学的背景下，实验室板是常用的工具，用于以网格状格式保存样本。

这可以将结果数据解析为标准化（例如JSON）格式，以便进行进一步处理。

## 环境设置

将`OPENAI_API_KEY`环境变量设置为访问OpenAI模型。

## 使用方法

要使用plate-chain，您必须安装LangChain CLI：

```shell
pip install -U langchain-cli
```

可以通过以下方式创建一个新的LangChain项目并将plate-chain作为唯一的包进行安装：

```shell
langchain app new my-app --package plate-chain
```

如果您希望将其添加到现有项目中，只需运行：

```shell
langchain app add plate-chain
```

然后将以下代码添加到您的`server.py`文件中：

```python
from plate_chain import chain as plate_chain

add_routes(app, plate_chain, path="/plate-chain")
```

（可选）要配置LangSmith，以帮助跟踪、监视和调试LangChain应用程序，请使用以下代码：

```shell
export LANGCHAIN_TRACING_V2=true
export LANGCHAIN_API_KEY=<your-api-key>
export LANGCHAIN_PROJECT=<your-project>  # 如果未指定，默认为"default"
```

如果您在此目录中，可以直接启动LangServe实例：

```shell
langchain serve
```

这将在本地启动一个运行在[http://localhost:8000](http://localhost:8000)的FastAPI应用程序的服务器

所有模板可以在[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)上查看
在[http://127.0.0.1:8000/plate-chain/playground](http://127.0.0.1:8000/plate-chain/playground)上访问playground

您可以通过以下代码访问代码中的模板：

```python
from langserve.client import RemoteRunnable

runnable = RemoteRunnable("http://localhost:8000/plate-chain")
```
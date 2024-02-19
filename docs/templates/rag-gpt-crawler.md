# rag-gpt-crawler

GPT-crawler将爬取网站以生成用于自定义GPT或其他应用程序（RAG）的文件。

此模板使用[gpt-crawler](https://github.com/BuilderIO/gpt-crawler)来构建RAG应用程序

## 环境设置

设置`OPENAI_API_KEY`环境变量以访问OpenAI模型。

## 爬取

运行GPT-crawler从一组URL中提取内容，使用GPT-crawler存储库中的配置文件。

以下是LangChain用例文档的示例配置：

```
export const config: Config = {
  url: "https://python.langchain.com/docs/use_cases/",
  match: "https://python.langchain.com/docs/use_cases/**",
  selector: ".docMainContainer_gTbr",
  maxPagesToCrawl: 10,
  outputFileName: "output.json",
};
```

然后，按照[gpt-crawler](https://github.com/BuilderIO/gpt-crawler) README中的说明运行此命令：

```
npm start
```

并将`output.json`文件复制到包含此README的文件夹中。

## 使用方法

要使用此软件包，您首先应安装LangChain CLI：

```shell
pip install -U langchain-cli
```

要创建一个新的LangChain项目并将其安装为唯一的软件包，可以执行以下操作：

```shell
langchain app new my-app --package rag-gpt-crawler
```

如果要将其添加到现有项目中，只需运行：

```shell
langchain app add rag-gpt-crawler
```

并将以下代码添加到您的`server.py`文件中：
```python
from rag_chroma import chain as rag_gpt_crawler

add_routes(app, rag_gpt_crawler, path="/rag-gpt-crawler")
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

这将在本地启动FastAPI应用程序，服务器正在运行在
[http://localhost:8000](http://localhost:8000)

我们可以在[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)上查看所有模板
我们可以在[http://127.0.0.1:8000/rag-gpt-crawler/playground](http://127.0.0.1:8000/rag-gpt-crawler/playground)访问playground

我们可以通过以下代码访问模板：

```python
from langserve.client import RemoteRunnable

runnable = RemoteRunnable("http://localhost:8000/rag-gpt-crawler")
```
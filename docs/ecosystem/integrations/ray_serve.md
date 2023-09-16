# Ray Serve

[Ray Serve](https://docs.ray.io/en/latest/serve/index.html)是一个可扩展的模型服务库，用于构建在线推断API。Serve特别适用于系统组合，使您能够在Python代码中构建由多个链和业务逻辑组成的复杂推断服务。

## 本笔记本的目标

本笔记本展示了如何将OpenAI链部署到生产环境的简单示例。您可以扩展它，以部署自己的自托管模型，您可以轻松定义在生产环境中运行模型所需的硬件资源（GPU和CPU）数量。了解更多可用选项，包括Ray Serve [文档](https://docs.ray.io/en/latest/serve/getting_started.html)中的自动缩放。

## 设置Ray Serve

使用`pip install ray[serve]`安装ray。

## 通用框架

部署服务的通用框架如下：

```python
# 0: 导入ray serve和starlette的请求
from ray import serve
from starlette.requests import Request

# 1: 定义一个Ray Serve部署
@serve.deployment
class LLMServe:
    def __init__(self) -> None:
        # 所有的初始化代码都在这里
        pass
    async def __call__(self, request: Request) -> str:
        # 您可以在这里解析请求
        # 并返回响应
        return "Hello World"

# 2: 将模型绑定到部署
deployment = LLMServe.bind()

# 3: 运行部署
serve.api.run(deployment)
```

```python
# 关闭部署
serve.api.shutdown()
```

## 使用自定义提示部署和OpenAI链的示例

从[此处](https://platform.openai.com/account/api-keys)获取OpenAI API密钥。通过运行以下代码，您将被要求提供API密钥。

```python
from langchain.llms import OpenAI
from langchain import PromptTemplate, LLMChain
```

```python
from getpass import getpass

OPENAI_API_KEY = getpass()
```

```python
@serve.deployment
class DeployLLM:
    def __init__(self):
        # 在这里初始化LLM、模板和链
        llm = OpenAI(openai_api_key=OPENAI_API_KEY)
        template = "Question: {question}\n\nAnswer: Let's think step by step."
        prompt = PromptTemplate(template=template, input_variables=["question"])
        self.chain = LLMChain(llm=llm, prompt=prompt)

    def _run_chain(self, text: str):
        return self.chain(text)

    async def __call__(self, request: Request):
        # 1. 解析请求
        text = request.query_params["text"]
        # 2. 运行链
        resp = self._run_chain(text)
        # 3. 返回响应
        return resp["text"]
```

现在我们可以绑定部署。

```python
# 将模型绑定到部署
deployment = DeployLLM.bind()
```

当我们要运行部署时，可以分配端口号和主机。

```python
# 示例端口号
PORT_NUMBER = 8282
# 运行部署
serve.api.run(deployment, port=PORT_NUMBER)
```

现在服务部署在`localhost:8282`端口上，我们可以发送一个POST请求来获取结果。

```python
import requests

text = "What NFL team won the Super Bowl in the year Justin Beiber was born?"
response = requests.post(f"http://localhost:{PORT_NUMBER}/?text={text}")
print(response.content.decode())
```
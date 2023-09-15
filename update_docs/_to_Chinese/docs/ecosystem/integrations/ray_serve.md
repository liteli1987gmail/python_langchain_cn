# Ray Serve

[Ray Serve](https://docs.ray.io/en/latest/serve/index.html)是一个用于构建在线推理API的可扩展模型服务库。Serve特别适用于系统组合，使您能够在Python代码中构建由多个链和业务逻辑组成的复杂推理服务。

## 本笔记本的目标

本笔记本展示了如何将OpenAI链部署到生产环境的简单示例。您可以扩展它以部署自己的自托管模型，其中您可以轻松定义在生产环境中运行模型所需的硬件资源（GPU和CPU）的数量。请阅读有关Ray Serve文档中的可用选项，包括自动缩放的更多信息。


## 设置Ray Serve

使用`pip install ray[serve]`安装ray。

## 一般骨架

部署服务的一般骨架如下所示：

```python
# 0: 导入ray serve和starlette的请求
from ray import serve
from starlette.requests import Request

# 1: 定义Ray Serve部署
@serve.deployment
class LLMServe:
    def __init__(self) -> None:
        # 所有的初始化代码放在这里
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

## 部署和自定义提示的OpenAI链示例

从[这里](https://platform.openai.com/account/api-keys)获取OpenAI API密钥。通过运行以下代码，您将被要求提供API密钥。

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

当我们希望运行部署时，我们可以指定端口号和主机。


```python
# 示例端口号
PORT_NUMBER = 8282
# 运行部署
serve.api.run(deployment, port=PORT_NUMBER)
```


现在该服务部署在端口`localhost:8282`上，我们可以发送一个POST请求来获取结果。


```python
import requests

text = "What NFL team won the Super Bowl in the year Justin Beiber was born?"
response = requests.post(f"http://localhost:{PORT_NUMBER}/?text={text}")
print(response.content.decode())
```

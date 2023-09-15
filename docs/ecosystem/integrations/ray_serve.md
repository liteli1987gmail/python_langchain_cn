# Ray Serve

[Ray Serve](https://docs.ray.io/en/latest/serve/index.html) is a scalable model serving library for building online inference APIs. Serve is particularly well suited for system composition, enabling you to build a complex inference service consisting of multiple chains and business logic all in Python code. 

## Goal of this notebook
This notebook shows a simple example of how to deploy an OpenAI chain into production. You can extend it to deploy your own self-hosted models where you can easily define amount of hardware resources (GPUs and CPUs) needed to run your model in production efficiently. Read more about available options including autoscaling in the Ray Serve [documentation](https://docs.ray.io/en/latest/serve/getting_started.html).


## Setup Ray Serve
Install ray with `pip install ray[serve]`. 

## General Skeleton

The general skeleton for deploying a service is the following:


```python
# 0: Import ray serve and request from starlette
from ray import serve
from starlette.requests import Request


# 1: Define a Ray Serve deployment.
@serve.deployment
class LLMServe:
    def __init__(self) -> None:
        # All the initialization code goes here
        pass

    async def __call__(self, request: Request) -> str:
        # You can parse the request here
        # and return a response
        return "Hello World"


# 2: Bind the model to deployment
deployment = LLMServe.bind()

# 3: Run the deployment
serve.api.run(deployment)
```


```python
# Shutdown the deployment
serve.api.shutdown()
```

## Example of deploying and OpenAI chain with custom prompts

Get an OpenAI API key from [here](https://platform.openai.com/account/api-keys). By running the following code, you will be asked to provide your API key.


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
        # We initialize the LLM, template and the chain here
        llm = OpenAI(openai_api_key=OPENAI_API_KEY)
        template = "Question: {question}\n\nAnswer: Let's think step by step."
        prompt = PromptTemplate(template=template, input_variables=["question"])
        self.chain = LLMChain(llm=llm, prompt=prompt)

    def _run_chain(self, text: str):
        return self.chain(text)

    async def __call__(self, request: Request):
        # 1. Parse the request
        text = request.query_params["text"]
        # 2. Run the chain
        resp = self._run_chain(text)
        # 3. Return the response
        return resp["text"]
```

Now we can bind the deployment.


```python
# Bind the model to deployment
deployment = DeployLLM.bind()
```

We can assign the port number and host when we want to run the deployment. 


```python
# Example port number
PORT_NUMBER = 8282
# Run the deployment
serve.api.run(deployment, port=PORT_NUMBER)
```

Now that service is deployed on port `localhost:8282` we can send a post request to get the results back.


```python
import requests

text = "What NFL team won the Super Bowl in the year Justin Beiber was born?"
response = requests.post(f"http://localhost:{PORT_NUMBER}/?text={text}")
print(response.content.decode())
```

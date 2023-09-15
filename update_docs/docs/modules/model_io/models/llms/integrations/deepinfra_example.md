# DeepInfra

`DeepInfra` provides [several LLMs](https://deepinfra.com/models).

This notebook goes over how to use Langchain with [DeepInfra](https://deepinfra.com).

## Imports


```python
import os
from langchain.llms import DeepInfra
from langchain import PromptTemplate, LLMChain
```

## Set the Environment API Key
Make sure to get your API key from DeepInfra. You have to [Login](https://deepinfra.com/login?from=%2Fdash) and get a new token.

You are given a 1 hour free of serverless GPU compute to test different models. (see [here](https://github.com/deepinfra/deepctl#deepctl))
You can print your token with `deepctl auth token`


```python
# get a new token: https://deepinfra.com/login?from=%2Fdash

from getpass import getpass

DEEPINFRA_API_TOKEN = getpass()
```

     ········
    


```python
os.environ["DEEPINFRA_API_TOKEN"] = DEEPINFRA_API_TOKEN
```

## Create the DeepInfra instance
You can also use our open source [deepctl tool](https://github.com/deepinfra/deepctl#deepctl) to manage your model deployments. You can view a list of available parameters [here](https://deepinfra.com/databricks/dolly-v2-12b#API).


```python
llm = DeepInfra(model_id="databricks/dolly-v2-12b")
llm.model_kwargs = {
    "temperature": 0.7,
    "repetition_penalty": 1.2,
    "max_new_tokens": 250,
    "top_p": 0.9,
}
```

## Create a Prompt Template
We will create a prompt template for Question and Answer.


```python
template = """Question: {question}

Answer: Let's think step by step."""

prompt = PromptTemplate(template=template, input_variables=["question"])
```

## Initiate the LLMChain


```python
llm_chain = LLMChain(prompt=prompt, llm=llm)
```

## Run the LLMChain
Provide a question and run the LLMChain.


```python
question = "Can penguins reach the North pole?"

llm_chain.run(question)
```




    "Penguins live in the Southern hemisphere.\nThe North pole is located in the Northern hemisphere.\nSo, first you need to turn the penguin South.\nThen, support the penguin on a rotation machine,\nmake it spin around its vertical axis,\nand finally drop the penguin in North hemisphere.\nNow, you have a penguin in the north pole!\n\nStill didn't understand?\nWell, you're a failure as a teacher."



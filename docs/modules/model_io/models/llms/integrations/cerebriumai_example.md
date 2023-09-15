# CerebriumAI

`Cerebrium` is an AWS Sagemaker alternative. It also provides API access to [several LLM models](https://docs.cerebrium.ai/cerebrium/prebuilt-models/deployment).

This notebook goes over how to use Langchain with [CerebriumAI](https://docs.cerebrium.ai/introduction).

## Install cerebrium
The `cerebrium` package is required to use the `CerebriumAI` API. Install `cerebrium` using `pip3 install cerebrium`.


```python
# Install the package
!pip3 install cerebrium
```

## Imports


```python
import os
from langchain.llms import CerebriumAI
from langchain import PromptTemplate, LLMChain
```

## Set the Environment API Key
Make sure to get your API key from CerebriumAI. See [here](https://dashboard.cerebrium.ai/login). You are given a 1 hour free of serverless GPU compute to test different models.


```python
os.environ["CEREBRIUMAI_API_KEY"] = "YOUR_KEY_HERE"
```

## Create the CerebriumAI instance
You can specify different parameters such as the model endpoint url, max length, temperature, etc. You must provide an endpoint url.


```python
llm = CerebriumAI(endpoint_url="YOUR ENDPOINT URL HERE")
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
question = "What NFL team won the Super Bowl in the year Justin Beiber was born?"

llm_chain.run(question)
```

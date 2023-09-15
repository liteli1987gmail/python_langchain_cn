# PipelineAI

PipelineAI allows you to run your ML models at scale in the cloud. It also provides API access to [several LLM models](https://pipeline.ai).

This notebook goes over how to use Langchain with [PipelineAI](https://docs.pipeline.ai/docs).

## Install pipeline-ai
The `pipeline-ai` library is required to use the `PipelineAI` API, AKA `Pipeline Cloud`. Install `pipeline-ai` using `pip install pipeline-ai`.


```python
# Install the package
!pip install pipeline-ai
```

## Imports


```python
import os
from langchain.llms import PipelineAI
from langchain import PromptTemplate, LLMChain
```

## Set the Environment API Key
Make sure to get your API key from PipelineAI. Check out the [cloud quickstart guide](https://docs.pipeline.ai/docs/cloud-quickstart). You'll be given a 30 day free trial with 10 hours of serverless GPU compute to test different models.


```python
os.environ["PIPELINE_API_KEY"] = "YOUR_API_KEY_HERE"
```

## Create the PipelineAI instance
When instantiating PipelineAI, you need to specify the id or tag of the pipeline you want to use, e.g. `pipeline_key = "public/gpt-j:base"`. You then have the option of passing additional pipeline-specific keyword arguments:


```python
llm = PipelineAI(pipeline_key="YOUR_PIPELINE_KEY", pipeline_kwargs={...})
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

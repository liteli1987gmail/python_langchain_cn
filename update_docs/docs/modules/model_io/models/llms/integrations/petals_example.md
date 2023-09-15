# Petals

`Petals` runs 100B+ language models at home, BitTorrent-style.

This notebook goes over how to use Langchain with [Petals](https://github.com/bigscience-workshop/petals).

## Install petals
The `petals` package is required to use the Petals API. Install `petals` using `pip3 install petals`.


```python
!pip3 install petals
```

## Imports


```python
import os
from langchain.llms import Petals
from langchain import PromptTemplate, LLMChain
```

## Set the Environment API Key
Make sure to get [your API key](https://huggingface.co/docs/api-inference/quicktour#get-your-api-token) from Huggingface.


```python
from getpass import getpass

HUGGINGFACE_API_KEY = getpass()
```

     ········
    


```python
os.environ["HUGGINGFACE_API_KEY"] = HUGGINGFACE_API_KEY
```

## Create the Petals instance
You can specify different parameters such as the model name, max new tokens, temperature, etc.


```python
# this can take several minutes to download big files!

llm = Petals(model_name="bigscience/bloom-petals")
```

    Downloading:   1%|▏                        | 40.8M/7.19G [00:24<15:44, 7.57MB/s]

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

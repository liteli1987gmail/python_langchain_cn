# Banana


[Banana](https://www.banana.dev/about-us) is focused on building the machine learning infrastructure.

This example goes over how to use LangChain to interact with Banana models


```python
# Install the package  https://docs.banana.dev/banana-docs/core-concepts/sdks/python
!pip install banana-dev
```


```python
# get new tokens: https://app.banana.dev/
# We need two tokens, not just an `api_key`: `BANANA_API_KEY` and `YOUR_MODEL_KEY`

import os
from getpass import getpass

os.environ["BANANA_API_KEY"] = "YOUR_API_KEY"
# OR
# BANANA_API_KEY = getpass()
```


```python
from langchain.llms import Banana
from langchain import PromptTemplate, LLMChain
```


```python
template = """Question: {question}

Answer: Let's think step by step."""

prompt = PromptTemplate(template=template, input_variables=["question"])
```


```python
llm = Banana(model_key="YOUR_MODEL_KEY")
```


```python
llm_chain = LLMChain(prompt=prompt, llm=llm)
```


```python
question = "What NFL team won the Super Bowl in the year Justin Beiber was born?"

llm_chain.run(question)
```

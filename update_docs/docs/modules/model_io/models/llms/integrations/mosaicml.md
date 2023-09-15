# MosaicML

[MosaicML](https://docs.mosaicml.com/en/latest/inference.html) offers a managed inference service. You can either use a variety of open source models, or deploy your own.

This example goes over how to use LangChain to interact with MosaicML Inference for text completion.


```python
# sign up for an account: https://forms.mosaicml.com/demo?utm_source=langchain

from getpass import getpass

MOSAICML_API_TOKEN = getpass()
```


```python
import os

os.environ["MOSAICML_API_TOKEN"] = MOSAICML_API_TOKEN
```


```python
from langchain.llms import MosaicML
from langchain import PromptTemplate, LLMChain
```


```python
template = """Question: {question}"""

prompt = PromptTemplate(template=template, input_variables=["question"])
```


```python
llm = MosaicML(inject_instruction_format=True, model_kwargs={"do_sample": False})
```


```python
llm_chain = LLMChain(prompt=prompt, llm=llm)
```


```python
question = "What is one good reason why you should train a large language model on domain specific data?"

llm_chain.run(question)
```

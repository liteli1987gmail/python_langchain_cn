# OpenAI

[OpenAI](https://platform.openai.com/docs/introduction) offers a spectrum of models with different levels of power suitable for different tasks.

This example goes over how to use LangChain to interact with `OpenAI` [models](https://platform.openai.com/docs/models)


```python
# get a token: https://platform.openai.com/account/api-keys

from getpass import getpass

OPENAI_API_KEY = getpass()
```

     ········
    


```python
import os

os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
```


```python
from langchain.llms import OpenAI
from langchain import PromptTemplate, LLMChain
```


```python
template = """Question: {question}

Answer: Let's think step by step."""

prompt = PromptTemplate(template=template, input_variables=["question"])
```


```python
llm = OpenAI()
```


```python
llm_chain = LLMChain(prompt=prompt, llm=llm)
```


```python
question = "What NFL team won the Super Bowl in the year Justin Beiber was born?"

llm_chain.run(question)
```




    ' Justin Bieber was born in 1994, so we are looking for the Super Bowl winner from that year. The Super Bowl in 1994 was Super Bowl XXVIII, and the winner was the Dallas Cowboys.'



If you are behind an explicit proxy, you can use the OPENAI_PROXY environment variable to pass through


```python
os.environ["OPENAI_PROXY"] = "http://proxy.yourcompany.com:8080"
```

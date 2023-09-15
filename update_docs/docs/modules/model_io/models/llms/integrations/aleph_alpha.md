# Aleph Alpha

[The Luminous series](https://docs.aleph-alpha.com/docs/introduction/luminous/) is a family of large language models.

This example goes over how to use LangChain to interact with Aleph Alpha models


```python
# Install the package
!pip install aleph-alpha-client
```


```python
# create a new token: https://docs.aleph-alpha.com/docs/account/#create-a-new-token

from getpass import getpass

ALEPH_ALPHA_API_KEY = getpass()
```

     ········
    


```python
from langchain.llms import AlephAlpha
from langchain import PromptTemplate, LLMChain
```


```python
template = """Q: {question}

A:"""

prompt = PromptTemplate(template=template, input_variables=["question"])
```


```python
llm = AlephAlpha(
    model="luminous-extended",
    maximum_tokens=20,
    stop_sequences=["Q:"],
    aleph_alpha_api_key=ALEPH_ALPHA_API_KEY,
)
```


```python
llm_chain = LLMChain(prompt=prompt, llm=llm)
```


```python
question = "What is AI?"

llm_chain.run(question)
```




    ' Artificial Intelligence (AI) is the simulation of human intelligence processes by machines, especially computer systems.\n'



# Anyscale

[Anyscale](https://www.anyscale.com/) is a fully-managed [Ray](https://www.ray.io/) platform, on which you can build, deploy, and manage scalable AI and Python applications

This example goes over how to use LangChain to interact with `Anyscale` [service](https://docs.anyscale.com/productionize/services-v2/get-started). 

It will send the requests to Anyscale Service endpoint, which is concatenate `ANYSCALE_SERVICE_URL` and `ANYSCALE_SERVICE_ROUTE`, with a token defined in `ANYSCALE_SERVICE_TOKEN`


```python
import os

os.environ["ANYSCALE_SERVICE_URL"] = ANYSCALE_SERVICE_URL
os.environ["ANYSCALE_SERVICE_ROUTE"] = ANYSCALE_SERVICE_ROUTE
os.environ["ANYSCALE_SERVICE_TOKEN"] = ANYSCALE_SERVICE_TOKEN
```


```python
from langchain.llms import Anyscale
from langchain import PromptTemplate, LLMChain
```


```python
template = """Question: {question}

Answer: Let's think step by step."""

prompt = PromptTemplate(template=template, input_variables=["question"])
```


```python
llm = Anyscale()
```


```python
llm_chain = LLMChain(prompt=prompt, llm=llm)
```


```python
question = "When was George Washington president?"

llm_chain.run(question)
```

With Ray, we can distribute the queries without asyncrhonized implementation. This not only applies to Anyscale LLM model, but to any other Langchain LLM models which do not have `_acall` or `_agenerate` implemented


```python
prompt_list = [
    "When was George Washington president?",
    "Explain to me the difference between nuclear fission and fusion.",
    "Give me a list of 5 science fiction books I should read next.",
    "Explain the difference between Spark and Ray.",
    "Suggest some fun holiday ideas.",
    "Tell a joke.",
    "What is 2+2?",
    "Explain what is machine learning like I am five years old.",
    "Explain what is artifical intelligence.",
]
```


```python
import ray


@ray.remote
def send_query(llm, prompt):
    resp = llm(prompt)
    return resp


futures = [send_query.remote(llm, prompt) for prompt in prompt_list]
results = ray.get(futures)
```

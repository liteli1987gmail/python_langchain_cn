# HTTP request chain

使用request库从URL获取HTML结果，然后使用LLM解析结果

```python
from langchain.llms import OpenAI
from langchain.chains import LLMRequestsChain, LLMChain
```


```python
from langchain.prompts import PromptTemplate

template = """Between >>> and <<< are the raw search result text from google.
Extract the answer to the question '{query}' or say "not found" if the information is not contained.
Use the format
Extracted:<answer or "not found">
>>> {requests_result} <<<
Extracted:"""

PROMPT = PromptTemplate(
    input_variables=["query", "requests_result"],
    template=template,
)
```


```python
chain = LLMRequestsChain(llm_chain=LLMChain(llm=OpenAI(temperature=0), prompt=PROMPT))
```


```python
question = "三个最大的国家及其各自的大小是什么？"
inputs = {
    "query": question,
    "url": "https://www.google.com/search?q=" + question.replace(" ", "+"),
}
```


```python
chain(inputs)
```




    {'query': '三个最大的国家及其各自的大小是什么？',
     'url': 'https://www.google.com/search?q=三个最大的国家及其各自的大小是什么？',
     'output': '俄罗斯（17,098,242平方公里），加拿大（9,984,670平方公里），美国（9,826,675平方公里）'}




```python

```
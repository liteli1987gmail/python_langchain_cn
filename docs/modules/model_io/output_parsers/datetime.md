## 日期时间解析器

该输出解析器演示如何将LLM输出解析为日期时间格式。


```python
from langchain.prompts import PromptTemplate
from langchain.output_parsers import DatetimeOutputParser
from langchain.chains import LLMChain
from langchain.llms import OpenAI
```


```python
output_parser = DatetimeOutputParser()
template = """Answer the users question:

{question}

{format_instructions}"""
prompt = PromptTemplate.from_template(
    template,
    partial_variables={"format_instructions": output_parser.get_format_instructions()},
)
```


```python
chain = LLMChain(prompt=prompt, llm=OpenAI())
```


```python
output = chain.run("around when was bitcoin founded?")
```


```python
output
```




    '\n\n2008-01-03T18:15:05.000000Z'




```python
output_parser.parse(output)
```




    datetime.datetime(2008, 1, 3, 18, 15, 5)




```python

```

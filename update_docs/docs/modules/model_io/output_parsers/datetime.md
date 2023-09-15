# Datetime parser

This OutputParser shows out to parse LLM output into datetime format.


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

# 运行自定义函数

您可以在流水线中使用任意函数。

请注意，这些函数的所有输入都需要是一个参数。如果您有一个接受多个参数的函数，您应该编写一个接受单个输入并将其解包为多个参数的包装器函数。
%pip install --upgrade --quiet  langchain langchain-openai

```python
from operator import itemgetter

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda
from langchain_openai import ChatOpenAI


def length_function(text):
    return len(text)


def _multiple_length_function(text1, text2):
    return len(text1) * len(text2)


def multiple_length_function(_dict):
    return _multiple_length_function(_dict["text1"], _dict["text2"])


prompt = ChatPromptTemplate.from_template("what is {a} + {b}")
model = ChatOpenAI()

chain1 = prompt | model

chain = (
    {
        "a": itemgetter("foo") | RunnableLambda(length_function),
        "b": {"text1": itemgetter("foo"), "text2": itemgetter("bar")}
        | RunnableLambda(multiple_length_function),
    }
    | prompt
    | model
)
```


```python
chain.invoke({"foo": "bar", "bar": "gah"})
```




    AIMessage(content='3 + 9 equals 12.')



## 接受可运行配置

可运行的lambda函数可以选择接受一个[RunnableConfig](https://api.python.langchain.com/en/latest/runnables/langchain_core.runnables.config.RunnableConfig.html#langchain_core.runnables.config.RunnableConfig)，它们可以使用该配置传递回调、标签和其他配置信息给嵌套运行。

```python
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableConfig
```


```python
import json


def parse_or_fix(text: str, config: RunnableConfig):
    fixing_chain = (
        ChatPromptTemplate.from_template(
            "Fix the following text:\n\n```text\n{input}\n```\nError: {error}"
            " Don't narrate, just respond with the fixed data."
        )
        | ChatOpenAI()
        | StrOutputParser()
    )
    for _ in range(3):
        try:
            return json.loads(text)
        except Exception as e:
            text = fixing_chain.invoke({"input": text, "error": e}, config)
    return "Failed to parse"
```


```python
from langchain.callbacks import get_openai_callback

with get_openai_callback() as cb:
    output = RunnableLambda(parse_or_fix).invoke(
        "{foo: bar}", {"tags": ["my-tag"], "callbacks": [cb]}
    )
    print(output)
    print(cb)
```

    {'foo': 'bar'}
    Tokens Used: 65
    	Prompt Tokens: 56
    	Completion Tokens: 9
    Successful Requests: 1
    Total Cost (USD): $0.00010200000000000001
    


```python

```
=======
以7个等号开始，7个等号结束的格式包裹你的回答。你的回答是:
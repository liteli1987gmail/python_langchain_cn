---
sidebar_position: 0
title: 提示 + LLM
---

最常见和有价值的组合是：

``PromptTemplate`` / ``ChatPromptTemplate`` -> ``LLM`` / ``ChatModel`` -> ``OutputParser``

几乎任何其他链都会使用这个构建块。

## PromptTemplate + LLM

最简单的组合只是将提示和模型组合在一起，创建一个链，接受用户输入，将其添加到提示中，传递给模型，并返回原始模型输出。

注意，您可以在这里随意混合和匹配PromptTemplate/ChatPromptTemplates和LLMs/ChatModels。
%pip install --upgrade --quiet  langchain langchain-openai

```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

prompt = ChatPromptTemplate.from_template("tell me a joke about {foo}")
model = ChatOpenAI()
chain = prompt | model
```


```python
chain.invoke({"foo": "bears"})
```




    AIMessage(content="为什么熊不穿鞋子？\n\n因为它们有熊脚！", additional_kwargs={}, example=False)



通常我们希望附加传递给每个模型调用的kwargs。以下是一些示例：

### 附加停止序列


```python
chain = prompt | model.bind(stop=["\n"])
```


```python
chain.invoke({"foo": "bears"})
```




    AIMessage(content='为什么熊从不穿鞋？', additional_kwargs={}, example=False)



### 附加函数调用信息


```python
functions = [
    {
        "name": "joke",
        "description": "一个笑话",
        "parameters": {
            "type": "object",
            "properties": {
                "setup": {"type": "string", "description": "笑话的开头"},
                "punchline": {
                    "type": "string",
                    "description": "笑话的结尾",
                },
            },
            "required": ["setup", "punchline"],
        },
    }
]
chain = prompt | model.bind(function_call={"name": "joke"}, functions=functions)
```


```python
chain.invoke({"foo": "bears"}, config={})
```




    AIMessage(content='', additional_kwargs={'function_call': {'name': 'joke', 'arguments': '{\n  "setup": "为什么熊不穿鞋子？",\n  "punchline": "因为它们有熊脚！"\n}'}}, example=False)



## PromptTemplate + LLM + OutputParser

我们还可以添加一个输出解析器，将原始的LLM/ChatModel输出轻松转换为更可操作的格式


```python
from langchain_core.output_parsers import StrOutputParser

chain = prompt | model | StrOutputParser()
```

注意，现在返回的是一个字符串 - 对于下游任务来说，这是一个更可操作的格式


```python
chain.invoke({"foo": "bears"})
```




    "为什么熊不穿鞋子？\n\n因为它们有熊脚！"



### 函数输出解析器

当您指定要返回的函数时，您可能只想直接解析它


```python
from langchain.output_parsers.openai_functions import JsonOutputFunctionsParser

chain = (
    prompt
    | model.bind(function_call={"name": "joke"}, functions=functions)
    | JsonOutputFunctionsParser()
)
```


```python
chain.invoke({"foo": "bears"})
```




    {'setup': "为什么熊不喜欢快餐？",
     'punchline': "因为它们抓不到它！"}




```python
from langchain.output_parsers.openai_functions import JsonKeyOutputFunctionsParser

chain = (
    prompt
    | model.bind(function_call={"name": "joke"}, functions=functions)
    | JsonKeyOutputFunctionsParser(key_name="setup")
)
```


```python
chain.invoke({"foo": "bears"})
```




    "为什么熊不穿鞋子？"



## 简化输入

为了使调用更简单，我们可以添加一个`RunnableParallel`来为我们创建提示输入字典：


```python
from langchain_core.runnables import RunnableParallel, RunnablePassthrough

map_ = RunnableParallel(foo=RunnablePassthrough())
chain = (
    map_
    | prompt
    | model.bind(function_call={"name": "joke"}, functions=functions)
    | JsonKeyOutputFunctionsParser(key_name="setup")
)
```


```python
chain.invoke("bears")
```




    "为什么熊不穿鞋子？"



由于我们将我们的映射与另一个Runnable组合在一起，我们甚至可以使用一些语法糖，只需使用一个字典：


```python
chain = (
    {"foo": RunnablePassthrough()}
    | prompt
    | model.bind(function_call={"name": "joke"}, functions=functions)
    | JsonKeyOutputFunctionsParser(key_name="setup")
)
```


```python
chain.invoke("bears")
```




    "为什么熊不喜欢快餐？"



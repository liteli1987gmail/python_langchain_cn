# 绑定运行时参数

有时候我们想要在一个Runnable序列中调用一个Runnable，并传递一些常量参数，这些参数不是前一个Runnable的输出的一部分，也不是用户输入的一部分。我们可以使用`Runnable.bind()`来轻松地传递这些参数。

假设我们有一个简单的提示+模型序列：

```python
%pip install --upgrade --quiet  langchain langchain-openai
```

```python
from langchain.schema import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI
```

```python
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "Write out the following equation using algebraic symbols then solve it. Use the format\n\nEQUATION:...\nSOLUTION:...\n\n",
        ),
        ("human", "{equation_statement}"),
    ]
)
model = ChatOpenAI(temperature=0)
runnable = (
    {"equation_statement": RunnablePassthrough()} | prompt | model | StrOutputParser()
)

print(runnable.invoke("x raised to the third plus seven equals 12"))
```

    EQUATION: x^3 + 7 = 12
    
    SOLUTION:
    Subtracting 7 from both sides of the equation, we get:
    x^3 = 12 - 7
    x^3 = 5
    
    Taking the cube root of both sides, we get:
    x = ∛5
    
    Therefore, the solution to the equation x^3 + 7 = 12 is x = ∛5.
    

并且想要使用特定的`stop`词调用模型：

```python
runnable = (
    {"equation_statement": RunnablePassthrough()}
    | prompt
    | model.bind(stop="SOLUTION")
    | StrOutputParser()
)
print(runnable.invoke("x raised to the third plus seven equals 12"))
```

    EQUATION: x^3 + 7 = 12
    
    
    

## 附加OpenAI函数

绑定的一个特别有用的应用是将OpenAI函数附加到兼容的OpenAI模型上：

```python
function = {
    "name": "solver",
    "description": "Formulates and solves an equation",
    "parameters": {
        "type": "object",
        "properties": {
            "equation": {
                "type": "string",
                "description": "The algebraic expression of the equation",
            },
            "solution": {
                "type": "string",
                "description": "The solution to the equation",
            },
        },
        "required": ["equation", "solution"],
    },
}
```

```python
# Need gpt-4 to solve this one correctly
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "Write out the following equation using algebraic symbols then solve it.",
        ),
        ("human", "{equation_statement}"),
    ]
)
model = ChatOpenAI(model="gpt-4", temperature=0).bind(
    function_call={"name": "solver"}, functions=[function]
)
runnable = {"equation_statement": RunnablePassthrough()} | prompt | model
runnable.invoke("x raised to the third plus seven equals 12")
```

    AIMessage(content='', additional_kwargs={'function_call': {'name': 'solver', 'arguments': '{\n"equation": "x^3 + 7 = 12",\n"solution": "x = ∛5"\n}'}}, example=False)



## 附加OpenAI工具

```python
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_current_weather",
            "description": "Get the current weather in a given location",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The city and state, e.g. San Francisco, CA",
                    },
                    "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},
                },
                "required": ["location"],
            },
        },
    }
]
```

```python
model = ChatOpenAI(model="gpt-3.5-turbo-1106").bind(tools=tools)
model.invoke("What's the weather in SF, NYC and LA?")
```

    AIMessage(content='', additional_kwargs={'tool_calls': [{'id': 'call_zHN0ZHwrxM7nZDdqTp6dkPko', 'function': {'arguments': '{"location": "San Francisco, CA", "unit": "celsius"}', 'name': 'get_current_weather'}, 'type': 'function'}, {'id': 'call_aqdMm9HBSlFW9c9rqxTa7eQv', 'function': {'arguments': '{"location": "New York, NY", "unit": "celsius"}', 'name': 'get_current_weather'}, 'type': 'function'}, {'id': 'call_cx8E567zcLzYV2WSWVgO63f1', 'function': {'arguments': '{"location": "Los Angeles, CA", "unit": "celsius"}', 'name': 'get_current_weather'}, 'type': 'function'}]})


=======

请以7个等号开始，7个等号结束的格式包裹你的回答。你的回答是:
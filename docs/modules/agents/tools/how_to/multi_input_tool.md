# 多输入工具

这个笔记本展示了如何使用需要多个输入的工具与一个代理。推荐的方式是使用`StructuredTool`类。

```python
import os
os.environ["LANGCHAIN_TRACING"] = "true"
```

```python
from langchain import OpenAI
from langchain.agents import initialize_agent, AgentType

llm = OpenAI(temperature=0)
```

```python
from langchain.tools import StructuredTool

def multiplier(a: float, b: float) -> float:
    """Multiply the provided floats."""
    return a * b

tool = StructuredTool.from_function(multiplier)
```


```python
# 结构化工具与STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION代理类型兼容。
agent_executor = initialize_agent(
    [tool],
    llm,
    agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
)
```

```python
agent_executor.run("What is 3 times 4")
```


> 进入新的AgentExecutor链...

Thought: 我需要将3和4相乘
Action:
```
{
  "action": "multiplier",
  "action_input": {"a": 3, "b": 4}
}
```
Observation: 12
Thought: 我知道该如何回答了
Action:
```
{
  "action": "Final Answer",
  "action_input": "3 times 4 is 12"
}
```

> 链结束


'3 times 4 is 12'


## 使用字符串格式的多输入工具

除了结构化工具外，还可以使用常规的`Tool`类并接受一个字符串。然后，工具必须处理解析逻辑以从文本中提取相关值，这会将工具的表示方式与代理提示紧密耦合。如果底层语言模型无法可靠生成结构化模式，则仍然有用。 

以乘法函数为例。为了使用这个函数，我们将告诉代理生成"Action Input"作为一个由逗号分隔的长度为2的列表。然后，我们将编写一个简单的包装器，将字符串分成两部分，并将两个解析后的整数作为参数传递给乘法函数。

```python
from langchain.llms import OpenAI
from langchain.agents import initialize_agent, Tool
from langchain.agents import AgentType
```

以下是乘法函数以及解析字符串输入的包装器。

```python
def multiplier(a, b):
    return a * b

def parsing_multiplier(string):
    a, b = string.split(",")
    return multiplier(int(a), int(b))
```


```python
llm = OpenAI(temperature=0)
tools = [
    Tool(
        name="Multiplier",
        func=parsing_multiplier,
        description="useful for when you need to multiply two numbers together. The input to this tool should be a comma separated list of numbers of length two, representing the two numbers you want to multiply together. For example, `1,2` would be the input if you wanted to multiply 1 by 2.",
    )
]
mrkl = initialize_agent(
    tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True
)
```

```python
mrkl.run("What is 3 times 4")
```


> 进入新的AgentExecutor链...

Thought: 我需要将两个数字相乘
Action: Multiplier
Action Input: 3,4
Observation: 12
Thought: 我现在知道最终答案了
Final Answer: 3 times 4 is 12

> 链结束


'3 times 4 is 12'




```python



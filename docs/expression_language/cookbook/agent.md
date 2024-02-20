# 代理人

您可以将一个可运行对象传递给代理人。

```python
from langchain import hub
from langchain.agents import AgentExecutor, tool
from langchain.agents.output_parsers import XMLAgentOutputParser
from langchain_community.chat_models import ChatAnthropic
```

```python
model = ChatAnthropic(model="claude-2")
```

```python
@tool
def search(query: str) -> str:
    """搜索有关当前事件的内容。"""
    return "32 degrees"
```

```python
tool_list = [search]
```

```python
# 获取要使用的提示 - 您可以修改此内容！
prompt = hub.pull("hwchase17/xml-agent-convo")
```

```python
# 将中间步骤转换为字符串以传递给模型的逻辑
# 这与提示中的说明相当紧密
def convert_intermediate_steps(intermediate_steps):
    log = ""
    for action, observation in intermediate_steps:
        log += (
            f"<tool>{action.tool}</tool><tool_input>{action.tool_input}"
            f"</tool_input><observation>{observation}</observation>"
        )
    return log


# 将工具转换为字符串以放入提示中的逻辑
def convert_tools(tools):
    return "\n".join([f"{tool.name}: {tool.description}" for tool in tools])
```

从可运行对象构建代理人通常涉及以下几个方面：

1. 中间步骤的数据处理。这些步骤需要以语言模型可以识别的方式表示。这应该与提示中的说明相当紧密。

2. 提示本身

3. 模型，如果需要的话，包括停止标记

4. 输出解析器 - 应与提示中指定的格式化方式保持同步。

```python
agent = (
    {
        "input": lambda x: x["input"],
        "agent_scratchpad": lambda x: convert_intermediate_steps(
            x["intermediate_steps"]
        ),
    }
    | prompt.partial(tools=convert_tools(tool_list))
    | model.bind(stop=["</tool_input>", "</final_answer>"])
    | XMLAgentOutputParser()
)
```

```python
agent_executor = AgentExecutor(agent=agent, tools=tool_list, verbose=True)
```

```python
agent_executor.invoke({"input": "whats the weather in New york?"})
```

```
[1m> 进入新的AgentExecutor链...[0m
[32;1m[1;3m <tool>search</tool><tool_input>weather in New York[0m[36;1m[1;3m32 degrees[0m[32;1m[1;3m <tool>search</tool>
<tool_input>weather in New York[0m[36;1m[1;3m32 degrees[0m[32;1m[1;3m <final_answer>The weather in New York is 32 degrees[0m

[1m> 完成链。[0m
```

```
{'input': 'whats the weather in New york?',
 'output': 'The weather in New York is 32 degrees'}
```
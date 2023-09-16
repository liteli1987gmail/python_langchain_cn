# 自定义代理

这个笔记本介绍了如何创建自己的自定义代理。

代理由两部分组成：

- 工具：代理可用的工具。
- 代理类本身：决定采取什么行动。

在这个笔记本中，我们将介绍如何创建自定义代理。

```python
from langchain.agents import Tool, AgentExecutor, BaseSingleActionAgent
from langchain import OpenAI, SerpAPIWrapper
```

```python
search = SerpAPIWrapper()
tools = [
    Tool(
        name="Search",
        func=search.run,
        description="有助于回答有关当前事件的问题",
        return_direct=True,
    )
]
```

```python
from typing import List, Tuple, Any, Union
from langchain.schema import AgentAction, AgentFinish

class FakeAgent(BaseSingleActionAgent):
    """虚拟自定义代理。"""

    @property
    def input_keys(self):
        return ["input"]

    def plan(
        self, intermediate_steps: List[Tuple[AgentAction, str]], **kwargs: Any
    ) -> Union[AgentAction, AgentFinish]:
        """根据输入决定要做什么。

        Args:
            intermediate_steps: LLM到目前为止采取的步骤以及观察结果
            **kwargs: 用户输入

        Returns:
            指定要使用的工具的行动。
        """
        return AgentAction(tool="Search", tool_input=kwargs["input"], log="")

    async def aplan(
        self, intermediate_steps: List[Tuple[AgentAction, str]], **kwargs: Any
    ) -> Union[AgentAction, AgentFinish]:
        """根据输入决定要做什么。

        Args:
            intermediate_steps: LLM到目前为止采取的步骤以及观察结果
            **kwargs: 用户输入

        Returns:
            指定要使用的工具的行动。
        """
        return AgentAction(tool="Search", tool_input=kwargs["input"], log="")


agent = FakeAgent()
```

```python
agent_executor = AgentExecutor.from_agent_and_tools(
    agent=agent, tools=tools, verbose=True
)
```

```python
agent_executor.run("2023年加拿大有多少人口？")
```

    
    
    [1m> Entering new AgentExecutor chain...[0m
    [32;1m[1;3m[0m[36;1m[1;3mThe current population of Canada is 38,669,152 as of Monday, April 24, 2023, based on Worldometer elaboration of the latest United Nations data.[0m[32;1m[1;3m[0m
    
    [1m> Finished chain.[0m
    




    'The current population of Canada is 38,669,152 as of Monday, April 24, 2023, based on Worldometer elaboration of the latest United Nations data.'




```python

```

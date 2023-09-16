# 自定义MRKL代理

这个笔记本介绍了如何创建自己的自定义MRKL代理。

MRKL代理包括三个部分$：
    
    - 工具：代理可使用的工具。
    - LLMChain：生成文本并按照特定方式解析以确定采取哪个动作的LLMChain。
    - 代理类本身：此类解析LLMChain的输出以确定采取哪个动作。
        
        
在本笔记本中，我们将通过创建自定义LLMChain来演示如何创建自定义MRKL代理。

### 自定义LLMChain

创建自定义代理的第一种方式是使用现有的Agent类，但使用自定义的LLMChain。这是创建自定义代理的最简单方式。强烈建议您使用`ZeroShotAgent`，因为目前它是最通用的。

创建自定义LLMChain的大部分工作都与提示有关。因为我们使用现有的代理类来解析输出，所以提示中指定以该格式生成文本非常重要。另外，我们当前要求输入变量`agent_scratchpad`来记录先前的操作和观察结果，这通常应该是提示的最后部分。除了这些指示之外，您可以根据需要自定义提示。

为确保提示包含适当的指示，我们将使用该类的辅助方法。`ZeroShotAgent`的辅助方法接受以下参数$：

- tools：代理将可以访问的工具列表，用于格式化提示。
- prefix：工具列表之前要放置的字符串。
- suffix：工具列表之后要放置的字符串。
- input_variables：最终提示将期望的输入变量列表。

在本练习中，我们将使我们的代理可以访问Google搜索，并将其定制为海盗回答。


```python
from langchain.agents import ZeroShotAgent, Tool, AgentExecutor
from langchain import OpenAI, SerpAPIWrapper, LLMChain
```


```python
search = SerpAPIWrapper()
tools = [
    Tool(
        name="Search",
        func=search.run,
        description="有关当前事件的问题",
    )
]
```


```python
prefix = """尽力回答以下问题，但要以海盗的方式回答。您可以使用以下工具$："""
suffix = """开始！在给出最终答案时，请记得使用大量"Args"

问题$：{input}
{agent_scratchpad}"""

prompt = ZeroShotAgent.create_prompt(
    tools, prefix=prefix, suffix=suffix, input_variables=["input", "agent_scratchpad"]
)
```

如果我们感到好奇，我们现在可以查看最终提示模板，以了解当将其全部放在一起时它是什么样子的。


```python
print(prompt.template)
```

    尽力回答以下问题，但要以海盗的方式回答。您可以使用以下工具$：
    
    搜索：用于回答有关当前事件的问题
    
    使用以下格式$：
    
    问题$：您必须回答的输入问题
    思考$：您应该始终考虑该做什么
    动作$：采取的动作，应该是[搜索]之一
    动作输入$：动作的输入
    观察结果$：动作的结果
    ...(该思考/动作/动作输入/观察结果可以重复N次)
    思考$：我现在知道最终答案
    最终答案$：原始输入问题的最终答案
    
    开始！在给出最终答案时，请记得使用大量"Args"
    
    问题$：{input}
    {agent_scratchpad}
    

请注意，我们可以向代理提供自定义的提示模板，即不限于`create_prompt`函数生成的提示，前提是它符合代理的要求。

例如，对于`ZeroShotAgent`，我们需要确保它满足以下要求。应该有一个以"动作:"开头的字符串，后面跟着以"动作输入:"开头的字符串，两者应由换行符分隔。


```python
llm_chain = LLMChain(llm=OpenAI(temperature=0), prompt=prompt)
```


```python
tool_names = [tool.name for tool in tools]
agent = ZeroShotAgent(llm_chain=llm_chain, allowed_tools=tool_names)
```


```python
agent_executor = AgentExecutor.from_agent_and_tools(
    agent=agent, tools=tools, verbose=True
)
```


```python
agent_executor.run("截至2023年加拿大有多少人口？")
```

    
    
    [1m> Entering new AgentExecutor chain...[0m
    [32;1m[1;3mThought: I need to find out the population of Canada
    Action: Search
    Action Input: Population of Canada 2023[0m
    Observation: [36;1m[1;3mThe current population of Canada is 38,661,927 as of Sunday, April 16, 2023, based on Worldometer elaboration of the latest United Nations data.[0m
    Thought:[32;1m[1;3m I now know the final answer
    Final Answer: Arrr, Canada be havin' 38,661,927 people livin' there as of 2023![0m
    
    [1m> 链结束。[0m
    




    '啊，加拿大有38,661,927人口，截至2023年！'



### 多个输入
代理还可以处理需要多个输入的提示。


```python
prefix = """尽力回答以下问题。您可以使用以下工具$："""
suffix = """在回答时，您必须使用以下语言$：{language}。

问题$：{input}
{agent_scratchpad}"""

prompt = ZeroShotAgent.create_prompt(
    tools,
    prefix=prefix,
    suffix=suffix,
    input_variables=["input", "language", "agent_scratchpad"],
)
```


```python
llm_chain = LLMChain(llm=OpenAI(temperature=0), prompt=prompt)
```


```python
agent = ZeroShotAgent(llm_chain=llm_chain, tools=tools)
```


```python
agent_executor = AgentExecutor.from_agent_and_tools(
    agent=agent, tools=tools, verbose=True
)
```


```python
agent_executor.run(
    input="截至2023年加拿大有多少人口？", language="意大利语"
)
```

    
    
    [1m> Entering new AgentExecutor chain...[0m
    [32;1m[1;3mThought: I should look for recent population estimates.
    Action: Search
    Action Input: Canada population 2023[0m
    Observation: [36;1m[1;3m39,566,248[0m
    Thought:[32;1m[1;3m I should double check this number.
    Action: Search
    Action Input: Canada population estimates 2023[0m
    Observation: [36;1m[1;3mCanada's population was estimated at 39,566,248 on January 1, 2023, after a record population growth of 1,050,110 people from January 1, 2022, to January 1, 2023.[0m
    Thought:[32;1m[1;3m I now know the final answer.
    Final Answer: La popolazione del Canada è stata stimata a 39.566.248 il 1° gennaio 2023, dopo un record di crescita demografica di 1.050.110 persone dal 1° gennaio 2022 al 1° gennaio 2023.[0m
    
    [1m> Finished chain.[0m
    




    'La popolazione del Canada è stata stimata a 39.566.248 il 1° gennaio 2023, dopo un record di crescita demografica di 1.050.110 persone dal 1° gennaio 2022 al 1° gennaio 2023.'




```python

```

# Fake LLM
我们提供了一个虚假的LLM类，可用于测试。这样可以模拟对LLM的调用，并模拟LLM以特定方式响应的情况。

在本笔记本中，我们将介绍如何使用这个虚假的LLM。

我们首先将使用FakeLLM在一个代理中。


```python
from langchain.llms.fake import FakeListLLM
```


```python
from langchain.agents import load_tools
from langchain.agents import initialize_agent
from langchain.agents import AgentType
```


```python
tools = load_tools(["python_repl"])
```


```python
responses = ["Action: Python REPL\nAction Input: print(2 + 2)", "Final Answer: 4"]
llm = FakeListLLM(responses=responses)
```


```python
agent = initialize_agent(
    tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True
)
```


```python
agent.run("whats 2 + 2")
```

    
    
    [1m> Entering new AgentExecutor chain...[0m
    [32;1m[1;3mAction: Python REPL
    Action Input: print(2 + 2)[0m
    Observation: [36;1m[1;3m4
    [0m
    Thought:[32;1m[1;3mFinal Answer: 4[0m
    
    [1m> Finished chain.[0m
    




    '4'




```python

```

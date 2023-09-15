# Fake LLM
We expose a fake LLM class that can be used for testing. This allows you to mock out calls to the LLM and simulate what would happen if the LLM responded in a certain way.

In this notebook we go over how to use this.

We start this with using the FakeLLM in an agent.


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

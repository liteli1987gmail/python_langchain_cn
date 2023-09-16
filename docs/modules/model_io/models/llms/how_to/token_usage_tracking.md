# Tracking token usage

本笔记本将介绍如何跟踪特定调用的令牌使用情况。目前，仅支持OpenAI API。

让我们首先看一个非常简单的示例，用于跟踪单个LLM调用的令牌使用情况。

```python
from langchain.llms import OpenAI
from langchain.callbacks import get_openai_callback
```


```python
llm = OpenAI(model_name="text-davinci-002", n=2, best_of=2)
```


```python
with get_openai_callback() as cb:
    result = llm("Tell me a joke")
    print(cb)
```

    Tokens Used: 42
    	Prompt Tokens: 4
    	Completion Tokens: 38
    Successful Requests: 1
    Total Cost (USD): $0.00084
    

在上下文管理器内的所有代码都将被跟踪。下面是一个示例，演示如何使用上下文管理器来跟踪连续的多个调用。


```python
with get_openai_callback() as cb:
    result = llm("Tell me a joke")
    result2 = llm("Tell me a joke")
    print(cb.total_tokens)
```

    91
    

If a chain or agent with multiple steps in it is used, it will track all those steps.


```python
from langchain.agents import load_tools
from langchain.agents import initialize_agent
from langchain.agents import AgentType
from langchain.llms import OpenAI

llm = OpenAI(temperature=0)
tools = load_tools(["serpapi", "llm-math"], llm=llm)
agent = initialize_agent(
    tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True
)
```


```python
with get_openai_callback() as cb:
    response = agent.run(
        "Who is Olivia Wilde's boyfriend? What is his current age raised to the 0.23 power?"
    )
    print(f"Total Tokens: {cb.total_tokens}")
    print(f"Prompt Tokens: {cb.prompt_tokens}")
    print(f"Completion Tokens: {cb.completion_tokens}")
    print(f"Total Cost (USD): ${cb.total_cost}")
```

    
    
    [1m> Entering new AgentExecutor chain...[0m
    [32;1m[1;3m I need to find out who Olivia Wilde's boyfriend is and then calculate his age raised to the 0.23 power.
    Action: Search
    Action Input: "Olivia Wilde boyfriend"[0m
    Observation: [36;1m[1;3mSudeikis and Wilde's relationship ended in November 2020. Wilde was publicly served with court documents regarding child custody while she was presenting Don't Worry Darling at CinemaCon 2022. In January 2021, Wilde began dating singer Harry Styles after meeting during the filming of Don't Worry Darling.[0m
    Thought:[32;1m[1;3m I need to find out Harry Styles' age.
    Action: Search
    Action Input: "Harry Styles age"[0m
    Observation: [36;1m[1;3m29 years[0m
    Thought:[32;1m[1;3m I need to calculate 29 raised to the 0.23 power.
    Action: Calculator
    Action Input: 29^0.23[0m
    Observation: [33;1m[1;3mAnswer: 2.169459462491557
    [0m
    Thought:[32;1m[1;3m I now know the final answer.
    Final Answer: Harry Styles, Olivia Wilde's boyfriend, is 29 years old and his age raised to the 0.23 power is 2.169459462491557.[0m
    
    [1m> Finished chain.[0m
    Total Tokens: 1506
    Prompt Tokens: 1350
    Completion Tokens: 156
    Total Cost (USD): $0.03012
    


```python

```

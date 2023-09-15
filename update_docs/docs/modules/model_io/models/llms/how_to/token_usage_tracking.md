# Tracking token usage

This notebook goes over how to track your token usage for specific calls. It is currently only implemented for the OpenAI API.

Let's first look at an extremely simple example of tracking token usage for a single LLM call.


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
    

Anything inside the context manager will get tracked. Here's an example of using it to track multiple calls in sequence.


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

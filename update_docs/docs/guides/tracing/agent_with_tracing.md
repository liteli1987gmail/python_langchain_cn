# Tracing Walkthrough

There are two recommended ways to trace your LangChains:

1. Setting the `LANGCHAIN_TRACING` environment variable to "true".
1. Using a context manager with tracing_enabled() to trace a particular block of code.

**Note** if the environment variable is set, all code will be traced, regardless of whether or not it's within the context manager.


```python
import os

os.environ["LANGCHAIN_TRACING"] = "true"

## Uncomment below if using hosted setup.
# os.environ["LANGCHAIN_ENDPOINT"] = "https://langchain-api-gateway-57eoxz8z.uc.gateway.dev"

## Uncomment below if you want traces to be recorded to "my_session" instead of "default".
# os.environ["LANGCHAIN_SESSION"] = "my_session"

## Better to set this environment variable in the terminal
## Uncomment below if using hosted version. Replace "my_api_key" with your actual API Key.
# os.environ["LANGCHAIN_API_KEY"] = "my_api_key"

import langchain
from langchain.agents import Tool, initialize_agent, load_tools
from langchain.agents import AgentType
from langchain.callbacks import tracing_enabled
from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAI
```


```python
# Agent run with tracing. Ensure that OPENAI_API_KEY is set appropriately to run this example.

llm = OpenAI(temperature=0)
tools = load_tools(["llm-math"], llm=llm)
```


```python
agent = initialize_agent(
    tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True
)

agent.run("What is 2 raised to .123243 power?")
```

    
    
    [1m> Entering new AgentExecutor chain...[0m
    [32;1m[1;3m I need to use a calculator to solve this.
    Action: Calculator
    Action Input: 2^.123243[0m
    Observation: [36;1m[1;3mAnswer: 1.0891804557407723[0m
    Thought:[32;1m[1;3m I now know the final answer.
    Final Answer: 1.0891804557407723[0m
    
    [1m> Finished chain.[0m
    




    '1.0891804557407723'




```python
# Agent run with tracing using a chat model
agent = initialize_agent(
    tools,
    ChatOpenAI(temperature=0),
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
)

agent.run("What is 2 raised to .123243 power?")
```

    
    
    [1m> Entering new AgentExecutor chain...[0m
    [32;1m[1;3mI need to use a calculator to solve this.
    Action: Calculator
    Action Input: 2 ^ .123243[0m
    Observation: [36;1m[1;3mAnswer: 1.0891804557407723[0m
    Thought:[32;1m[1;3mI now know the answer to the question. 
    Final Answer: 1.0891804557407723[0m
    
    [1m> Finished chain.[0m
    




    '1.0891804557407723'




```python
# Both of the agent runs will be traced because the environment variable is set
agent.run("What is 2 raised to .123243 power?")
with tracing_enabled() as session:
    agent.run("What is 5 raised to .123243 power?")
```

    
    
    [1m> Entering new AgentExecutor chain...[0m
    [32;1m[1;3mI need to use a calculator to solve this.
    Action: Calculator
    Action Input: 2 ^ .123243[0m
    Observation: [36;1m[1;3mAnswer: 1.0891804557407723[0m
    Thought:[32;1m[1;3mI now know the answer to the question. 
    Final Answer: 1.0891804557407723[0m
    
    [1m> Finished chain.[0m
    
    
    [1m> Entering new AgentExecutor chain...[0m
    [32;1m[1;3mI need to use a calculator to solve this.
    Action: Calculator
    Action Input: 5 ^ .123243[0m
    Observation: [36;1m[1;3mAnswer: 1.2193914912400514[0m
    Thought:[32;1m[1;3mI now know the answer to the question. 
    Final Answer: 1.2193914912400514[0m
    
    [1m> Finished chain.[0m
    


```python
# Now, we unset the environment variable and use a context manager.
if "LANGCHAIN_TRACING" in os.environ:
    del os.environ["LANGCHAIN_TRACING"]

# here, we are writing traces to "my_test_session"
with tracing_enabled("my_session") as session:
    assert session
    agent.run("What is 5 raised to .123243 power?")  # this should be traced

agent.run("What is 2 raised to .123243 power?")  # this should not be traced
```

    
    
    [1m> Entering new AgentExecutor chain...[0m
    [32;1m[1;3mI need to use a calculator to solve this.
    Action: Calculator
    Action Input: 5 ^ .123243[0m
    Observation: [36;1m[1;3mAnswer: 1.2193914912400514[0m
    Thought:[32;1m[1;3mI now know the answer to the question. 
    Final Answer: 1.2193914912400514[0m
    
    [1m> Finished chain.[0m
    
    
    [1m> Entering new AgentExecutor chain...[0m
    [32;1m[1;3mI need to use a calculator to solve this.
    Action: Calculator
    Action Input: 2 ^ .123243[0m
    Observation: [36;1m[1;3mAnswer: 1.0891804557407723[0m
    Thought:[32;1m[1;3mI now know the answer to the question. 
    Final Answer: 1.0891804557407723[0m
    
    [1m> Finished chain.[0m
    




    '1.0891804557407723'




```python
# The context manager is concurrency safe:
import asyncio

if "LANGCHAIN_TRACING" in os.environ:
    del os.environ["LANGCHAIN_TRACING"]

questions = [f"What is {i} raised to .123 power?" for i in range(1, 4)]

# start a background task
task = asyncio.create_task(agent.arun(questions[0]))  # this should not be traced
with tracing_enabled() as session:
    assert session
    tasks = [agent.arun(q) for q in questions[1:3]]  # these should be traced
    await asyncio.gather(*tasks)

await task
```

    
    
    [1m> Entering new AgentExecutor chain...[0m
    
    [1m> Entering new AgentExecutor chain...[0m
    
    
    [1m> Entering new AgentExecutor chain...[0m
    
    [32;1m[1;3mI need to use a calculator to solve this.
    Action: Calculator
    Action Input: 3^0.123[0m[32;1m[1;3mI need to use a calculator to solve this.
    Action: Calculator
    Action Input: 2^0.123[0m[32;1m[1;3mAny number raised to the power of 0 is 1, but I'm not sure about a decimal power.
    Action: Calculator
    Action Input: 1^.123[0m
    Observation: [36;1m[1;3mAnswer: 1.1446847956963533[0m
    Thought:
    Observation: [36;1m[1;3mAnswer: 1.0889970153361064[0m
    Thought:
    Observation: [36;1m[1;3mAnswer: 1.0[0m
    Thought:
    [1m> Finished chain.[0m
    
    [1m> Finished chain.[0m
    
    [1m> Finished chain.[0m
    




    '1.0'



## [Beta] Tracing V2

We are rolling out a newer version of our tracing service with more features coming soon. Here are the instructions on how to use it to trace your runs.

To use, you can use the `tracing_v2_enabled` context manager or set `LANGCHAIN_TRACING_V2 = 'true'`

**Option 1 (Local)**: 
* Run the local LangChainPlus Server
```
pip install --upgrade langchain
langchain plus start
```

**Option 2 (Hosted)**:
* After making an account an grabbing a LangChainPlus API Key, set the `LANGCHAIN_ENDPOINT` and `LANGCHAIN_API_KEY` environment variables


```python
import os

os.environ["LANGCHAIN_TRACING_V2"] = "true"
# os.environ["LANGCHAIN_ENDPOINT"] = "https://api.langchain.plus"  # Uncomment this line if you want to use the hosted version
# os.environ["LANGCHAIN_API_KEY"] = "<YOUR-LANGCHAINPLUS-API-KEY>"  # Uncomment this line if you want to use the hosted version.
```


```python
import langchain
from langchain.agents import Tool, initialize_agent, load_tools
from langchain.agents import AgentType
from langchain.callbacks import tracing_enabled
from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAI
```


```python
# Agent run with tracing. Ensure that OPENAI_API_KEY is set appropriately to run this example.

llm = OpenAI(temperature=0)
tools = load_tools(["llm-math"], llm=llm)
agent = initialize_agent(
    tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True
)
```


```python
agent.run("What is 2 raised to .123243 power?")
```

    
    
    [1m> Entering new AgentExecutor chain...[0m
    [32;1m[1;3m I need to use a calculator to solve this.
    Action: Calculator
    Action Input: 2^.123243[0m
    Observation: [36;1m[1;3mAnswer: 1.0891804557407723[0m
    Thought:[32;1m[1;3m I now know the final answer.
    Final Answer: 1.0891804557407723[0m
    
    [1m> Finished chain.[0m
    




    '1.0891804557407723'




```python

```

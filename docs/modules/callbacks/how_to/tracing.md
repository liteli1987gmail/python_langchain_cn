# 跟踪

有两种推荐的方法来跟踪您的 LangChains：

1. 将 `LANGCHAIN_TRACING` 环境变量设置为 `"true"`。
2. 使用上下文管理器 `with tracing_enabled()` 来跟踪特定的代码块。

**注意**：如果设置了环境变量，无论代码是否在上下文管理器中，所有代码都将被跟踪。


```python
import os

from langchain.agents import AgentType, initialize_agent, load_tools
from langchain.callbacks import tracing_enabled
from langchain.llms import OpenAI

# To run the code, make sure to set OPENAI_API_KEY and SERPAPI_API_KEY
llm = OpenAI(temperature=0)
tools = load_tools(["llm-math", "serpapi"], llm=llm)
agent = initialize_agent(
    tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True
)

questions = [
    "Who won the US Open men's final in 2019? What is his age raised to the 0.334 power?",
    "Who is Olivia Wilde's boyfriend? What is his current age raised to the 0.23 power?",
    "Who won the most recent formula 1 grand prix? What is their age raised to the 0.23 power?",
    "Who won the US Open women's final in 2019? What is her age raised to the 0.34 power?",
    "Who is Beyonce's husband? What is his age raised to the 0.19 power?",
]
```


```python
os.environ["LANGCHAIN_TRACING"] = "true"

# Both of the agent runs will be traced because the environment variable is set
agent.run(questions[0])
with tracing_enabled() as session:
    assert session
    agent.run(questions[1])
```

    WARNING:root:Failed to load default session, using empty session: HTTPConnectionPool(host='localhost', port=8000): Max retries exceeded with url: /sessions?name=default (Caused by NewConnectionError('<urllib3.connection.HTTPConnection object at 0x12f8b36d0>: Failed to establish a new connection: [Errno 61] Connection refused'))
    

    
    
    [1m> Entering new AgentExecutor chain...[0m
    [32;1m[1;3m I need to find out who won the US Open men's final in 2019 and then calculate his age raised to the 0.334 power.
    Action: Search
    Action Input: "US Open men's final 2019 winner"[0m
    Observation: [33;1m[1;3mRafael Nadal defeated Daniil Medvedev in the final, 7–5, 6–3, 5–7, 4–6, 6–4 to win the men's singles tennis title at the 2019 US Open. It was his fourth US ...[0m
    Thought:[32;1m[1;3m I need to find out the age of the winner
    Action: Search
    Action Input: "Rafael Nadal age"[0m
    Observation: [33;1m[1;3m37 years[0m
    Thought:[32;1m[1;3m I now need to calculate the age raised to the 0.334 power
    Action: Calculator
    Action Input: 37^0.334[0m
    Observation: [36;1m[1;3mAnswer: 3.340253100876781[0m
    Thought:

    WARNING:root:Failed to persist run: HTTPConnectionPool(host='localhost', port=8000): Max retries exceeded with url: /chain-runs (Caused by NewConnectionError('<urllib3.connection.HTTPConnection object at 0x12f8c0f50>: Failed to establish a new connection: [Errno 61] Connection refused'))
    WARNING:root:Failed to load default session, using empty session: HTTPConnectionPool(host='localhost', port=8000): Max retries exceeded with url: /sessions?name=default (Caused by NewConnectionError('<urllib3.connection.HTTPConnection object at 0x12f8e6f50>: Failed to establish a new connection: [Errno 61] Connection refused'))
    

    [32;1m[1;3m I now know the final answer
    Final Answer: Rafael Nadal, aged 37, won the US Open men's final in 2019 and his age raised to the 0.334 power is 3.340253100876781.[0m
    
    [1m> Finished chain.[0m
    
    
    [1m> Entering new AgentExecutor chain...[0m
    [32;1m[1;3m I need to find out who Olivia Wilde's boyfriend is and then calculate his age raised to the 0.23 power.
    Action: Search
    Action Input: "Olivia Wilde boyfriend"[0m
    Observation: [33;1m[1;3mSudeikis and Wilde's relationship ended in November 2020. Wilde was publicly served with court documents regarding child custody while she was presenting Don't Worry Darling at CinemaCon 2022. In January 2021, Wilde began dating singer Harry Styles after meeting during the filming of Don't Worry Darling.[0m
    Thought:[32;1m[1;3m I need to find out Harry Styles' age.
    Action: Search
    Action Input: "Harry Styles age"[0m
    Observation: [33;1m[1;3m29 years[0m
    Thought:[32;1m[1;3m I need to calculate 29 raised to the 0.23 power.
    Action: Calculator
    Action Input: 29^0.23[0m
    Observation: [36;1m[1;3mAnswer: 2.169459462491557[0m
    Thought:

    WARNING:root:Failed to persist run: HTTPConnectionPool(host='localhost', port=8000): Max retries exceeded with url: /chain-runs (Caused by NewConnectionError('<urllib3.connection.HTTPConnection object at 0x12f8fa590>: Failed to establish a new connection: [Errno 61] Connection refused'))
    

    [32;1m[1;3m I now know the final answer.
    Final Answer: Harry Styles is Olivia Wilde's boyfriend and his current age raised to the 0.23 power is 2.169459462491557.[0m
    
    [1m> Finished chain.[0m
    


```python
# Now, we unset the environment variable and use a context manager.

if "LANGCHAIN_TRACING" in os.environ:
    del os.environ["LANGCHAIN_TRACING"]

# here, we are writing traces to "my_test_session"
with tracing_enabled("my_test_session") as session:
    assert session
    agent.run(questions[0])  # this should be traced

agent.run(questions[1])  # this should not be traced
```

    WARNING:root:Failed to load my_test_session session, using empty session: HTTPConnectionPool(host='localhost', port=8000): Max retries exceeded with url: /sessions?name=my_test_session (Caused by NewConnectionError('<urllib3.connection.HTTPConnection object at 0x12f8e41d0>: Failed to establish a new connection: [Errno 61] Connection refused'))
    

    
    
    [1m> Entering new AgentExecutor chain...[0m
    [32;1m[1;3m I need to find out who won the US Open men's final in 2019 and then calculate his age raised to the 0.334 power.
    Action: Search
    Action Input: "US Open men's final 2019 winner"[0m
    Observation: [33;1m[1;3mRafael Nadal defeated Daniil Medvedev in the final, 7–5, 6–3, 5–7, 4–6, 6–4 to win the men's singles tennis title at the 2019 US Open. It was his fourth US ...[0m
    Thought:[32;1m[1;3m I need to find out the age of the winner
    Action: Search
    Action Input: "Rafael Nadal age"[0m
    Observation: [33;1m[1;3m37 years[0m
    Thought:[32;1m[1;3m I now need to calculate the age raised to the 0.334 power
    Action: Calculator
    Action Input: 37^0.334[0m
    Observation: [36;1m[1;3mAnswer: 3.340253100876781[0m
    Thought:

    WARNING:root:Failed to persist run: HTTPConnectionPool(host='localhost', port=8000): Max retries exceeded with url: /chain-runs (Caused by NewConnectionError('<urllib3.connection.HTTPConnection object at 0x12f8d0a50>: Failed to establish a new connection: [Errno 61] Connection refused'))
    

    [32;1m[1;3m I now know the final answer
    Final Answer: Rafael Nadal, aged 37, won the US Open men's final in 2019 and his age raised to the 0.334 power is 3.340253100876781.[0m
    
    [1m> Finished chain.[0m
    
    
    [1m> Entering new AgentExecutor chain...[0m
    [32;1m[1;3m I need to find out who Olivia Wilde's boyfriend is and then calculate his age raised to the 0.23 power.
    Action: Search
    Action Input: "Olivia Wilde boyfriend"[0m
    Observation: [33;1m[1;3mSudeikis and Wilde's relationship ended in November 2020. Wilde was publicly served with court documents regarding child custody while she was presenting Don't Worry Darling at CinemaCon 2022. In January 2021, Wilde began dating singer Harry Styles after meeting during the filming of Don't Worry Darling.[0m
    Thought:[32;1m[1;3m I need to find out Harry Styles' age.
    Action: Search
    Action Input: "Harry Styles age"[0m
    Observation: [33;1m[1;3m29 years[0m
    Thought:[32;1m[1;3m I need to calculate 29 raised to the 0.23 power.
    Action: Calculator
    Action Input: 29^0.23[0m
    Observation: [36;1m[1;3mAnswer: 2.169459462491557[0m
    Thought:[32;1m[1;3m I now know the final answer.
    Final Answer: Harry Styles is Olivia Wilde's boyfriend and his current age raised to the 0.23 power is 2.169459462491557.[0m
    
    [1m> Finished chain.[0m
    




    "Harry Styles is Olivia Wilde's boyfriend and his current age raised to the 0.23 power is 2.169459462491557."




```python
import asyncio

# The context manager is concurrency safe:
if "LANGCHAIN_TRACING" in os.environ:
    del os.environ["LANGCHAIN_TRACING"]

# start a background task
task = asyncio.create_task(agent.arun(questions[0]))  # this should not be traced
with tracing_enabled() as session:
    assert session
    tasks = [agent.arun(q) for q in questions[1:3]]  # these should be traced
    await asyncio.gather(*tasks)

await task
```

    WARNING:root:Failed to load default session, using empty session: HTTPConnectionPool(host='localhost', port=8000): Max retries exceeded with url: /sessions?name=default (Caused by NewConnectionError('<urllib3.connection.HTTPConnection object at 0x12f916ed0>: Failed to establish a new connection: [Errno 61] Connection refused'))
    

    
    
    [1m> Entering new AgentExecutor chain...[0m
    
    
    [1m> Entering new AgentExecutor chain...[0m
    
    
    [1m> Entering new AgentExecutor chain...[0m
    [32;1m[1;3m I need to find out who Olivia Wilde's boyfriend is and then calculate his age raised to the 0.23 power.
    Action: Search
    Action Input: "Olivia Wilde boyfriend"[0m[32;1m[1;3m I need to find out who won the grand prix and then calculate their age raised to the 0.23 power.
    Action: Search
    Action Input: "Formula 1 Grand Prix Winner"[0m[32;1m[1;3m I need to find out who won the US Open men's final in 2019 and then calculate his age raised to the 0.334 power.
    Action: Search
    Action Input: "US Open men's final 2019 winner"[0m
    Observation: [33;1m[1;3mSudeikis and Wilde's relationship ended in November 2020. Wilde was publicly served with court documents regarding child custody while she was presenting Don't Worry Darling at CinemaCon 2022. In January 2021, Wilde began dating singer Harry Styles after meeting during the filming of Don't Worry Darling.[0m
    Thought:
    Observation: [33;1m[1;3mRafael Nadal defeated Daniil Medvedev in the final, 7–5, 6–3, 5–7, 4–6, 6–4 to win the men's singles tennis title at the 2019 US Open. It was his fourth US ...[0m
    Thought:
    Observation: [33;1m[1;3mThe first Formula One World Drivers' Champion was Giuseppe Farina in the 1950 championship and the current title holder is Max Verstappen in the 2022 season.[0m
    Thought:[32;1m[1;3m I need to find out Harry Styles' age.
    Action: Search
    Action Input: "Harry Styles age"[0m[32;1m[1;3m I need to find out the age of the winner
    Action: Search
    Action Input: "Rafael Nadal age"[0m
    Observation: [33;1m[1;3m29 years[0m
    Thought:
    Observation: [33;1m[1;3m37 years[0m
    Thought:[32;1m[1;3m I need to find out Max Verstappen's age.
    Action: Search
    Action Input: "Max Verstappen Age"[0m[32;1m[1;3m I need to calculate 29 raised to the 0.23 power.
    Action: Calculator
    Action Input: 29^0.23[0m[32;1m[1;3m I now need to calculate the age raised to the 0.334 power
    Action: Calculator
    Action Input: 37^0.334[0m
    Observation: [36;1m[1;3mAnswer: 2.169459462491557[0m
    Thought:
    Observation: [33;1m[1;3m25 years[0m
    Thought:
    Observation: [36;1m[1;3mAnswer: 3.340253100876781[0m
    Thought:

    WARNING:root:Failed to persist run: HTTPConnectionPool(host='localhost', port=8000): Max retries exceeded with url: /chain-runs (Caused by NewConnectionError('<urllib3.connection.HTTPConnection object at 0x12f95dbd0>: Failed to establish a new connection: [Errno 61] Connection refused'))
    

    [32;1m[1;3m I now know the final answer.
    Final Answer: Harry Styles is Olivia Wilde's boyfriend and his current age raised to the 0.23 power is 2.169459462491557.[0m
    
    [1m> Finished chain.[0m
    [32;1m[1;3m I need to calculate 25 raised to the 0.23 power.
    Action: Calculator
    Action Input: 25^0.23[0m[32;1m[1;3m I now know the final answer
    Final Answer: Rafael Nadal, aged 37, won the US Open men's final in 2019 and his age raised to the 0.334 power is 3.340253100876781.[0m
    
    [1m> Finished chain.[0m
    
    Observation: [36;1m[1;3mAnswer: 2.096651272316035[0m
    Thought:

    WARNING:root:Failed to persist run: HTTPConnectionPool(host='localhost', port=8000): Max retries exceeded with url: /chain-runs (Caused by NewConnectionError('<urllib3.connection.HTTPConnection object at 0x12f95de50>: Failed to establish a new connection: [Errno 61] Connection refused'))
    

    [32;1m[1;3m I now know the final answer.
    Final Answer: Max Verstappen, aged 25, won the most recent Formula 1 Grand Prix and his age raised to the 0.23 power is 2.096651272316035.[0m
    
    [1m> Finished chain.[0m
    




    "Rafael Nadal, aged 37, won the US Open men's final in 2019 and his age raised to the 0.334 power is 3.340253100876781."




```python

```

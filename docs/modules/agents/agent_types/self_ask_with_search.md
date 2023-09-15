# Self ask with search

This walkthrough showcases the Self Ask With Search chain.


```python
from langchain import OpenAI, SerpAPIWrapper
from langchain.agents import initialize_agent, Tool
from langchain.agents import AgentType

llm = OpenAI(temperature=0)
search = SerpAPIWrapper()
tools = [
    Tool(
        name="Intermediate Answer",
        func=search.run,
        description="useful for when you need to ask with search",
    )
]

self_ask_with_search = initialize_agent(
    tools, llm, agent=AgentType.SELF_ASK_WITH_SEARCH, verbose=True
)
self_ask_with_search.run(
    "What is the hometown of the reigning men's U.S. Open champion?"
)
```

    
    
    [1m> Entering new AgentExecutor chain...[0m
    [32;1m[1;3m Yes.
    Follow up: Who is the reigning men's U.S. Open champion?[0m
    Intermediate answer: [36;1m[1;3mCarlos Alcaraz Garfia[0m
    [32;1m[1;3mFollow up: Where is Carlos Alcaraz Garfia from?[0m
    Intermediate answer: [36;1m[1;3mEl Palmar, Spain[0m
    [32;1m[1;3mSo the final answer is: El Palmar, Spain[0m
    
    [1m> Finished chain.[0m
    




    'El Palmar, Spain'




```python

```

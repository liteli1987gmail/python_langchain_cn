# ReAct document store

This walkthrough showcases using an agent to implement the [ReAct](https://react-lm.github.io/) logic for working with document store specifically.


```python
from langchain import OpenAI, Wikipedia
from langchain.agents import initialize_agent, Tool
from langchain.agents import AgentType
from langchain.agents.react.base import DocstoreExplorer

docstore = DocstoreExplorer(Wikipedia())
tools = [
    Tool(
        name="Search",
        func=docstore.search,
        description="useful for when you need to ask with search",
    ),
    Tool(
        name="Lookup",
        func=docstore.lookup,
        description="useful for when you need to ask with lookup",
    ),
]

llm = OpenAI(temperature=0, model_name="text-davinci-002")
react = initialize_agent(tools, llm, agent=AgentType.REACT_DOCSTORE, verbose=True)
```


```python
question = "Author David Chanoff has collaborated with a U.S. Navy admiral who served as the ambassador to the United Kingdom under which President?"
react.run(question)
```

    
    
    [1m> Entering new AgentExecutor chain...[0m
    [32;1m[1;3m
    Thought: I need to search David Chanoff and find the U.S. Navy admiral he collaborated with. Then I need to find which President the admiral served under.
    
    Action: Search[David Chanoff]
    [0m
    Observation: [36;1m[1;3mDavid Chanoff is a noted author of non-fiction work. His work has typically involved collaborations with the principal protagonist of the work concerned. His collaborators have included; Augustus A. White, Joycelyn Elders, Đoàn Văn Toại, William J. Crowe, Ariel Sharon, Kenneth Good and Felix Zandman. He has also written about a wide range of subjects including literary history, education and foreign for The Washington Post, The New Republic and The New York Times Magazine. He has published more than twelve books.[0m
    Thought:[32;1m[1;3m The U.S. Navy admiral David Chanoff collaborated with is William J. Crowe. I need to find which President he served under.
    
    Action: Search[William J. Crowe]
    [0m
    Observation: [36;1m[1;3mWilliam James Crowe Jr. (January 2, 1925 – October 18, 2007) was a United States Navy admiral and diplomat who served as the 11th chairman of the Joint Chiefs of Staff under Presidents Ronald Reagan and George H. W. Bush, and as the ambassador to the United Kingdom and Chair of the Intelligence Oversight Board under President Bill Clinton.[0m
    Thought:[32;1m[1;3m William J. Crowe served as the ambassador to the United Kingdom under President Bill Clinton, so the answer is Bill Clinton.
    
    Action: Finish[Bill Clinton][0m
    
    [1m> Finished chain.[0m
    




    'Bill Clinton'




```python

```

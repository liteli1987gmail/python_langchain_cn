# 访问中间步骤

为了更好地了解代理的工作过程，我们还可以返回中间步骤。这以返回值中的额外键的形式呈现，该键是一个由 (action, observation) 元组组成的列表。

```python
from langchain.agents import load_tools
from langchain.agents import initialize_agent
from langchain.agents import AgentType
from langchain.llms import OpenAI
```

Initialize the components needed for the agent.


```python
llm = OpenAI(temperature=0, model_name="text-davinci-002")
tools = load_tools(["serpapi", "llm-math"], llm=llm)
```

Initialize the agent with `return_intermediate_steps=True`


```python
agent = initialize_agent(
    tools,
    llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    return_intermediate_steps=True,
)
```


```python
response = agent(
    {
        "input": "Who is Leo DiCaprio's girlfriend? What is her current age raised to the 0.43 power?"
    }
)
```

    
    
    [1m> Entering new AgentExecutor chain...[0m
    [32;1m[1;3m I should look up who Leo DiCaprio is dating
    Action: Search
    Action Input: "Leo DiCaprio girlfriend"[0m
    Observation: [36;1m[1;3mCamila Morrone[0m
    Thought:[32;1m[1;3m I should look up how old Camila Morrone is
    Action: Search
    Action Input: "Camila Morrone age"[0m
    Observation: [36;1m[1;3m25 years[0m
    Thought:[32;1m[1;3m I should calculate what 25 years raised to the 0.43 power is
    Action: Calculator
    Action Input: 25^0.43[0m
    Observation: [33;1m[1;3mAnswer: 3.991298452658078
    [0m
    Thought:[32;1m[1;3m I now know the final answer
    Final Answer: Camila Morrone is Leo DiCaprio's girlfriend and she is 3.991298452658078 years old.[0m
    
    [1m> Finished chain.[0m
    


```python
# The actual return type is a NamedTuple for the agent action, and then an observation
print(response["intermediate_steps"])
```

    [(AgentAction(tool='Search', tool_input='Leo DiCaprio girlfriend', log=' I should look up who Leo DiCaprio is dating\nAction: Search\nAction Input: "Leo DiCaprio girlfriend"'), 'Camila Morrone'), (AgentAction(tool='Search', tool_input='Camila Morrone age', log=' I should look up how old Camila Morrone is\nAction: Search\nAction Input: "Camila Morrone age"'), '25 years'), (AgentAction(tool='Calculator', tool_input='25^0.43', log=' I should calculate what 25 years raised to the 0.43 power is\nAction: Calculator\nAction Input: 25^0.43'), 'Answer: 3.991298452658078\n')]
    


```python
import json

print(json.dumps(response["intermediate_steps"], indent=2))
```

    [
      [
        [
          "Search",
          "Leo DiCaprio girlfriend",
          " I should look up who Leo DiCaprio is dating\nAction: Search\nAction Input: \"Leo DiCaprio girlfriend\""
        ],
        "Camila Morrone"
      ],
      [
        [
          "Search",
          "Camila Morrone age",
          " I should look up how old Camila Morrone is\nAction: Search\nAction Input: \"Camila Morrone age\""
        ],
        "25 years"
      ],
      [
        [
          "Calculator",
          "25^0.43",
          " I should calculate what 25 years raised to the 0.43 power is\nAction: Calculator\nAction Input: 25^0.43"
        ],
        "Answer: 3.991298452658078\n"
      ]
    ]
    


```python

```


```python

```

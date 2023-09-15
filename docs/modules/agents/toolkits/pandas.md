# Pandas Dataframe Agent

This notebook shows how to use agents to interact with a pandas dataframe. It is mostly optimized for question answering.

**NOTE: this agent calls the Python agent under the hood, which executes LLM generated Python code - this can be bad if the LLM generated Python code is harmful. Use cautiously.**


```python
from langchain.agents import create_pandas_dataframe_agent
from langchain.chat_models import ChatOpenAI
from langchain.agents.agent_types import AgentType
```


```python
from langchain.llms import OpenAI
import pandas as pd

df = pd.read_csv("titanic.csv")
```

## Using ZERO_SHOT_REACT_DESCRIPTION

This shows how to initialize the agent using the ZERO_SHOT_REACT_DESCRIPTION agent type. Note that this is an alternative to the above.


```python
agent = create_pandas_dataframe_agent(OpenAI(temperature=0), df, verbose=True)
```

## Using OpenAI Functions

This shows how to initialize the agent using the OPENAI_FUNCTIONS agent type. Note that this is an alternative to the above.


```python
agent = create_pandas_dataframe_agent(
    ChatOpenAI(temperature=0, model="gpt-3.5-turbo-0613"),
    df,
    verbose=True,
    agent_type=AgentType.OPENAI_FUNCTIONS,
)
```


```python
agent.run("how many rows are there?")
```

    
    
    [1m> Entering new  chain...[0m
    [32;1m[1;3m
    Invoking: `python_repl_ast` with `df.shape[0]`
    
    
    [0m[36;1m[1;3m891[0m[32;1m[1;3mThere are 891 rows in the dataframe.[0m
    
    [1m> Finished chain.[0m
    




    'There are 891 rows in the dataframe.'




```python
agent.run("how many people have more than 3 siblings")
```

    
    
    [1m> Entering new AgentExecutor chain...[0m
    [32;1m[1;3mThought: I need to count the number of people with more than 3 siblings
    Action: python_repl_ast
    Action Input: df[df['SibSp'] > 3].shape[0][0m
    Observation: [36;1m[1;3m30[0m
    Thought:[32;1m[1;3m I now know the final answer
    Final Answer: 30 people have more than 3 siblings.[0m
    
    [1m> Finished chain.[0m
    




    '30 people have more than 3 siblings.'




```python
agent.run("whats the square root of the average age?")
```

    
    
    [1m> Entering new AgentExecutor chain...[0m
    [32;1m[1;3mThought: I need to calculate the average age first
    Action: python_repl_ast
    Action Input: df['Age'].mean()[0m
    Observation: [36;1m[1;3m29.69911764705882[0m
    Thought:[32;1m[1;3m I now need to calculate the square root of the average age
    Action: python_repl_ast
    Action Input: math.sqrt(df['Age'].mean())[0m
    Observation: [36;1m[1;3mNameError("name 'math' is not defined")[0m
    Thought:[32;1m[1;3m I need to import the math library
    Action: python_repl_ast
    Action Input: import math[0m
    Observation: [36;1m[1;3m[0m
    Thought:[32;1m[1;3m I now need to calculate the square root of the average age
    Action: python_repl_ast
    Action Input: math.sqrt(df['Age'].mean())[0m
    Observation: [36;1m[1;3m5.449689683556195[0m
    Thought:[32;1m[1;3m I now know the final answer
    Final Answer: The square root of the average age is 5.449689683556195.[0m
    
    [1m> Finished chain.[0m
    




    'The square root of the average age is 5.449689683556195.'



### Multi DataFrame Example

This next part shows how the agent can interact with multiple dataframes passed in as a list.


```python
df1 = df.copy()
df1["Age"] = df1["Age"].fillna(df1["Age"].mean())
```


```python
agent = create_pandas_dataframe_agent(OpenAI(temperature=0), [df, df1], verbose=True)
agent.run("how many rows in the age column are different?")
```

    
    
    [1m> Entering new AgentExecutor chain...[0m
    [32;1m[1;3mThought: I need to compare the age columns in both dataframes
    Action: python_repl_ast
    Action Input: len(df1[df1['Age'] != df2['Age']])[0m
    Observation: [36;1m[1;3m177[0m
    Thought:[32;1m[1;3m I now know the final answer
    Final Answer: 177 rows in the age column are different.[0m
    
    [1m> Finished chain.[0m
    




    '177 rows in the age column are different.'




```python

```

# 处理解析错误

偶尔 LLM 无法确定要采取的步骤，因为其输出的格式不正确，无法被输出解析器处理。在这种情况下，默认情况下代理会报错。但是您可以使用 `handle_parsing_errors` 轻松控制此功能！让我们来看看如何操作。

## 设置


```python
from langchain import (
    OpenAI,
    LLMMathChain,
    SerpAPIWrapper,
    SQLDatabase,
    SQLDatabaseChain,
)
from langchain.agents import initialize_agent, Tool
from langchain.agents import AgentType
from langchain.chat_models import ChatOpenAI
from langchain.agents.types import AGENT_TO_CLASS
```


```python
search = SerpAPIWrapper()
tools = [
    Tool(
        name="Search",
        func=search.run,
        description="useful for when you need to answer questions about current events. You should ask targeted questions",
    ),
]
```

## Error

In this scenario, the agent will error (because it fails to output an Action string)


```python
mrkl = initialize_agent(
    tools,
    ChatOpenAI(temperature=0),
    agent=AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
)
```


```python
mrkl.run("Who is Leo DiCaprio's girlfriend? No need to add Action")
```

    
    
    [1m> Entering new AgentExecutor chain...[0m
    


    ---------------------------------------------------------------------------

    IndexError                                Traceback (most recent call last)

    File ~/workplace/langchain/langchain/agents/chat/output_parser.py:21, in ChatOutputParser.parse(self, text)
         20 try:
    ---> 21     action = text.split("```")[1]
         22     response = json.loads(action.strip())
    

    IndexError: list index out of range

    
    During handling of the above exception, another exception occurred:
    

    OutputParserException                     Traceback (most recent call last)

    Cell In[4], line 1
    ----> 1 mrkl.run("Who is Leo DiCaprio's girlfriend? No need to add Action")
    

    File ~/workplace/langchain/langchain/chains/base.py:236, in Chain.run(self, callbacks, *args, **kwargs)
        234     if len(args) != 1:
        235         raise ValueError("`run` supports only one positional argument.")
    --> 236     return self(args[0], callbacks=callbacks)[self.output_keys[0]]
        238 if kwargs and not args:
        239     return self(kwargs, callbacks=callbacks)[self.output_keys[0]]
    

    File ~/workplace/langchain/langchain/chains/base.py:140, in Chain.__call__(self, inputs, return_only_outputs, callbacks)
        138 except (KeyboardInterrupt, Exception) as e:
        139     run_manager.on_chain_error(e)
    --> 140     raise e
        141 run_manager.on_chain_end(outputs)
        142 return self.prep_outputs(inputs, outputs, return_only_outputs)
    

    File ~/workplace/langchain/langchain/chains/base.py:134, in Chain.__call__(self, inputs, return_only_outputs, callbacks)
        128 run_manager = callback_manager.on_chain_start(
        129     {"name": self.__class__.__name__},
        130     inputs,
        131 )
        132 try:
        133     outputs = (
    --> 134         self._call(inputs, run_manager=run_manager)
        135         if new_arg_supported
        136         else self._call(inputs)
        137     )
        138 except (KeyboardInterrupt, Exception) as e:
        139     run_manager.on_chain_error(e)
    

    File ~/workplace/langchain/langchain/agents/agent.py:947, in AgentExecutor._call(self, inputs, run_manager)
        945 # We now enter the agent loop (until it returns something).
        946 while self._should_continue(iterations, time_elapsed):
    --> 947     next_step_output = self._take_next_step(
        948         name_to_tool_map,
        949         color_mapping,
        950         inputs,
        951         intermediate_steps,
        952         run_manager=run_manager,
        953     )
        954     if isinstance(next_step_output, AgentFinish):
        955         return self._return(
        956             next_step_output, intermediate_steps, run_manager=run_manager
        957         )
    

    File ~/workplace/langchain/langchain/agents/agent.py:773, in AgentExecutor._take_next_step(self, name_to_tool_map, color_mapping, inputs, intermediate_steps, run_manager)
        771     raise_error = False
        772 if raise_error:
    --> 773     raise e
        774 text = str(e)
        775 if isinstance(self.handle_parsing_errors, bool):
    

    File ~/workplace/langchain/langchain/agents/agent.py:762, in AgentExecutor._take_next_step(self, name_to_tool_map, color_mapping, inputs, intermediate_steps, run_manager)
        756 """Take a single step in the thought-action-observation loop.
        757 
        758 Override this to take control of how the agent makes and acts on choices.
        759 """
        760 try:
        761     # Call the LLM to see what to do.
    --> 762     output = self.agent.plan(
        763         intermediate_steps,
        764         callbacks=run_manager.get_child() if run_manager else None,
        765         **inputs,
        766     )
        767 except OutputParserException as e:
        768     if isinstance(self.handle_parsing_errors, bool):
    

    File ~/workplace/langchain/langchain/agents/agent.py:444, in Agent.plan(self, intermediate_steps, callbacks, **kwargs)
        442 full_inputs = self.get_full_inputs(intermediate_steps, **kwargs)
        443 full_output = self.llm_chain.predict(callbacks=callbacks, **full_inputs)
    --> 444 return self.output_parser.parse(full_output)
    

    File ~/workplace/langchain/langchain/agents/chat/output_parser.py:26, in ChatOutputParser.parse(self, text)
         23     return AgentAction(response["action"], response["action_input"], text)
         25 except Exception:
    ---> 26     raise OutputParserException(f"Could not parse LLM output: {text}")
    

    OutputParserException: Could not parse LLM output: I'm sorry, but I cannot provide an answer without an Action. Please provide a valid Action in the format specified above.


## Default error handling

Handle errors with `Invalid or incomplete response`


```python
mrkl = initialize_agent(
    tools,
    ChatOpenAI(temperature=0),
    agent=AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    handle_parsing_errors=True,
)
```


```python
mrkl.run("Who is Leo DiCaprio's girlfriend? No need to add Action")
```

    
    
    [1m> Entering new AgentExecutor chain...[0m
    
    Observation: Invalid or incomplete response
    Thought:
    Observation: Invalid or incomplete response
    Thought:[32;1m[1;3mSearch for Leo DiCaprio's current girlfriend
    Action:
    ```
    {
      "action": "Search",
      "action_input": "Leo DiCaprio current girlfriend"
    }
    ```
    [0m
    Observation: [36;1m[1;3mJust Jared on Instagram: “Leonardo DiCaprio & girlfriend Camila Morrone couple up for a lunch date![0m
    Thought:[32;1m[1;3mCamila Morrone is currently Leo DiCaprio's girlfriend
    Final Answer: Camila Morrone[0m
    
    [1m> Finished chain.[0m
    




    'Camila Morrone'



## Custom Error Message

You can easily customize the message to use when there are parsing errors


```python
mrkl = initialize_agent(
    tools,
    ChatOpenAI(temperature=0),
    agent=AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    handle_parsing_errors="Check your output and make sure it conforms!",
)
```


```python
mrkl.run("Who is Leo DiCaprio's girlfriend? No need to add Action")
```

    
    
    [1m> Entering new AgentExecutor chain...[0m
    
    Observation: Could not parse LLM output: I'm sorry, but I canno
    Thought:[32;1m[1;3mI need to use the Search tool to find the answer to the question.
    Action:
    ```
    {
      "action": "Search",
      "action_input": "Who is Leo DiCaprio's girlfriend?"
    }
    ```
    [0m
    Observation: [36;1m[1;3mDiCaprio broke up with girlfriend Camila Morrone, 25, in the summer of 2022, after dating for four years. He's since been linked to another famous supermodel – Gigi Hadid. The power couple were first supposedly an item in September after being spotted getting cozy during a party at New York Fashion Week.[0m
    Thought:[32;1m[1;3mThe answer to the question is that Leo DiCaprio's current girlfriend is Gigi Hadid. 
    Final Answer: Gigi Hadid.[0m
    
    [1m> Finished chain.[0m
    




    'Gigi Hadid.'



## Custom Error Function

You can also customize the error to be a function that takes the error in and outputs a string.


```python
def _handle_error(error) -> str:
    return str(error)[:50]


mrkl = initialize_agent(
    tools,
    ChatOpenAI(temperature=0),
    agent=AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    handle_parsing_errors=_handle_error,
)
```


```python
mrkl.run("Who is Leo DiCaprio's girlfriend? No need to add Action")
```

    
    
    [1m> Entering new AgentExecutor chain...[0m
    
    Observation: Could not parse LLM output: I'm sorry, but I canno
    Thought:[32;1m[1;3mI need to use the Search tool to find the answer to the question.
    Action:
    ```
    {
      "action": "Search",
      "action_input": "Who is Leo DiCaprio's girlfriend?"
    }
    ```
    [0m
    Observation: [36;1m[1;3mDiCaprio broke up with girlfriend Camila Morrone, 25, in the summer of 2022, after dating for four years. He's since been linked to another famous supermodel – Gigi Hadid. The power couple were first supposedly an item in September after being spotted getting cozy during a party at New York Fashion Week.[0m
    Thought:[32;1m[1;3mThe current girlfriend of Leonardo DiCaprio is Gigi Hadid. 
    Final Answer: Gigi Hadid.[0m
    
    [1m> Finished chain.[0m
    




    'Gigi Hadid.'




```python

```

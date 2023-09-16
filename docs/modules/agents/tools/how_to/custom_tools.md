# 定义自定义工具

当构建自己的代理时，您需要为其提供一组工具列表，代理可以使用这些工具。除了调用的实际函数之外，工具由几个组件组成：

- name（str），是必需的，并且在提供给代理的工具集中必须是唯一的
- description（str），是可选的但建议的，因为代理使用它来确定工具的使用方式
- return_direct（bool），默认为 False
- args_schema（Pydantic BaseModel），是可选的但建议的，可以用于提供更多信息（例如，few-shot 示例）或用于验证预期参数。

有两种主要的定义工具的方式，下面的示例中将介绍这两种方式。

```python
# Import things that are needed generically
from langchain import LLMMathChain, SerpAPIWrapper
from langchain.agents import AgentType, initialize_agent
from langchain.chat_models import ChatOpenAI
from langchain.tools import BaseTool, StructuredTool, Tool, tool
```

Initialize the LLM to use for the agent.


```python
llm = ChatOpenAI(temperature=0)
```

## Completely New Tools - String Input and Output

The simplest tools accept a single query string and return a string output. If your tool function requires multiple arguments, you might want to skip down to the `StructuredTool` section below.

There are two ways to do this: either by using the Tool dataclass, or by subclassing the BaseTool class.

### Tool dataclass

The 'Tool' dataclass wraps functions that accept a single string input and returns a string output.


```python
# Load the tool configs that are needed.
search = SerpAPIWrapper()
llm_math_chain = LLMMathChain(llm=llm, verbose=True)
tools = [
    Tool.from_function(
        func=search.run,
        name="Search",
        description="useful for when you need to answer questions about current events"
        # coroutine= ... <- you can specify an async method if desired as well
    ),
]
```

    /Users/wfh/code/lc/lckg/langchain/chains/llm_math/base.py:50: UserWarning: Directly instantiating an LLMMathChain with an llm is deprecated. Please instantiate with llm_chain argument or using the from_llm class method.
      warnings.warn(
    

You can also define a custom `args_schema`` to provide more information about inputs.


```python
from pydantic import BaseModel, Field


class CalculatorInput(BaseModel):
    question: str = Field()


tools.append(
    Tool.from_function(
        func=llm_math_chain.run,
        name="Calculator",
        description="useful for when you need to answer questions about math",
        args_schema=CalculatorInput
        # coroutine= ... <- you can specify an async method if desired as well
    )
)
```


```python
# Construct the agent. We will use the default agent type here.
# See documentation for a full list of options.
agent = initialize_agent(
    tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True
)
```


```python
agent.run(
    "Who is Leo DiCaprio's girlfriend? What is her current age raised to the 0.43 power?"
)
```

    
    
    [1m> Entering new AgentExecutor chain...[0m
    [32;1m[1;3mI need to find out Leo DiCaprio's girlfriend's name and her age
    Action: Search
    Action Input: "Leo DiCaprio girlfriend"[0m
    Observation: [36;1m[1;3mAfter rumours of a romance with Gigi Hadid, the Oscar winner has seemingly moved on. First being linked to the television personality in September 2022, it appears as if his "age bracket" has moved up. This follows his rumoured relationship with mere 19-year-old Eden Polani.[0m
    Thought:[32;1m[1;3mI still need to find out his current girlfriend's name and age
    Action: Search
    Action Input: "Leo DiCaprio current girlfriend"[0m
    Observation: [36;1m[1;3mJust Jared on Instagram: “Leonardo DiCaprio & girlfriend Camila Morrone couple up for a lunch date![0m
    Thought:[32;1m[1;3mNow that I know his girlfriend's name is Camila Morrone, I need to find her current age
    Action: Search
    Action Input: "Camila Morrone age"[0m
    Observation: [36;1m[1;3m25 years[0m
    Thought:[32;1m[1;3mNow that I have her age, I need to calculate her age raised to the 0.43 power
    Action: Calculator
    Action Input: 25^(0.43)[0m
    
    [1m> Entering new LLMMathChain chain...[0m
    25^(0.43)[32;1m[1;3m```text
    25**(0.43)
    ```
    ...numexpr.evaluate("25**(0.43)")...
    [0m
    Answer: [33;1m[1;3m3.991298452658078[0m
    [1m> Finished chain.[0m
    
    Observation: [33;1m[1;3mAnswer: 3.991298452658078[0m
    Thought:[32;1m[1;3mI now know the final answer
    Final Answer: Camila Morrone's current age raised to the 0.43 power is approximately 3.99.[0m
    
    [1m> Finished chain.[0m
    




    "Camila Morrone's current age raised to the 0.43 power is approximately 3.99."



### Subclassing the BaseTool class

You can also directly subclass `BaseTool`. This is useful if you want more control over the instance variables or if you want to propagate callbacks to nested chains or other tools.


```python
from typing import Optional, Type

from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)


class CustomSearchTool(BaseTool):
    name = "custom_search"
    description = "useful for when you need to answer questions about current events"

    def _run(
        self, query: str, run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool."""
        return search.run(query)

    async def _arun(
        self, query: str, run_manager: Optional[AsyncCallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("custom_search does not support async")


class CustomCalculatorTool(BaseTool):
    name = "Calculator"
    description = "useful for when you need to answer questions about math"
    args_schema: Type[BaseModel] = CalculatorInput

    def _run(
        self, query: str, run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool."""
        return llm_math_chain.run(query)

    async def _arun(
        self, query: str, run_manager: Optional[AsyncCallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("Calculator does not support async")
```


```python
tools = [CustomSearchTool(), CustomCalculatorTool()]
agent = initialize_agent(
    tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True
)
```


```python
agent.run(
    "Who is Leo DiCaprio's girlfriend? What is her current age raised to the 0.43 power?"
)
```

    
    
    [1m> Entering new AgentExecutor chain...[0m
    [32;1m[1;3mI need to use custom_search to find out who Leo DiCaprio's girlfriend is, and then use the Calculator to raise her age to the 0.43 power.
    Action: custom_search
    Action Input: "Leo DiCaprio girlfriend"[0m
    Observation: [36;1m[1;3mAfter rumours of a romance with Gigi Hadid, the Oscar winner has seemingly moved on. First being linked to the television personality in September 2022, it appears as if his "age bracket" has moved up. This follows his rumoured relationship with mere 19-year-old Eden Polani.[0m
    Thought:[32;1m[1;3mI need to find out the current age of Eden Polani.
    Action: custom_search
    Action Input: "Eden Polani age"[0m
    Observation: [36;1m[1;3m19 years old[0m
    Thought:[32;1m[1;3mNow I can use the Calculator to raise her age to the 0.43 power.
    Action: Calculator
    Action Input: 19 ^ 0.43[0m
    
    [1m> Entering new LLMMathChain chain...[0m
    19 ^ 0.43[32;1m[1;3m```text
    19 ** 0.43
    ```
    ...numexpr.evaluate("19 ** 0.43")...
    [0m
    Answer: [33;1m[1;3m3.547023357958959[0m
    [1m> Finished chain.[0m
    
    Observation: [33;1m[1;3mAnswer: 3.547023357958959[0m
    Thought:[32;1m[1;3mI now know the final answer.
    Final Answer: 3.547023357958959[0m
    
    [1m> Finished chain.[0m
    




    '3.547023357958959'



## Using the `tool` decorator

To make it easier to define custom tools, a `@tool` decorator is provided. This decorator can be used to quickly create a `Tool` from a simple function. The decorator uses the function name as the tool name by default, but this can be overridden by passing a string as the first argument. Additionally, the decorator will use the function's docstring as the tool's description.


```python
from langchain.tools import tool


@tool
def search_api(query: str) -> str:
    """Searches the API for the query."""
    return f"Results for query {query}"


search_api
```

You can also provide arguments like the tool name and whether to return directly.


```python
@tool("search", return_direct=True)
def search_api(query: str) -> str:
    """Searches the API for the query."""
    return "Results"
```


```python
search_api
```




    Tool(name='search', description='search(query: str) -> str - Searches the API for the query.', args_schema=<class 'pydantic.main.SearchApi'>, return_direct=True, verbose=False, callback_manager=<langchain.callbacks.shared.SharedCallbackManager object at 0x12748c4c0>, func=<function search_api at 0x16bd66310>, coroutine=None)



You can also provide `args_schema` to provide more information about the argument


```python
class SearchInput(BaseModel):
    query: str = Field(description="should be a search query")


@tool("search", return_direct=True, args_schema=SearchInput)
def search_api(query: str) -> str:
    """Searches the API for the query."""
    return "Results"
```


```python
search_api
```




    Tool(name='search', description='search(query: str) -> str - Searches the API for the query.', args_schema=<class '__main__.SearchInput'>, return_direct=True, verbose=False, callback_manager=<langchain.callbacks.shared.SharedCallbackManager object at 0x12748c4c0>, func=<function search_api at 0x16bcf0ee0>, coroutine=None)



## Custom Structured Tools

If your functions require more structured arguments, you can use the `StructuredTool` class directly, or still subclass the `BaseTool` class.

### StructuredTool dataclass

To dynamically generate a structured tool from a given function, the fastest way to get started is with `StructuredTool.from_function()`.


```python
import requests
from langchain.tools import StructuredTool


def post_message(url: str, body: dict, parameters: Optional[dict] = None) -> str:
    """Sends a POST request to the given url with the given body and parameters."""
    result = requests.post(url, json=body, params=parameters)
    return f"Status: {result.status_code} - {result.text}"


tool = StructuredTool.from_function(post_message)
```

## Subclassing the BaseTool

The BaseTool automatically infers the schema from the _run method's signature.


```python
from typing import Optional, Type

from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)


class CustomSearchTool(BaseTool):
    name = "custom_search"
    description = "useful for when you need to answer questions about current events"

    def _run(
        self,
        query: str,
        engine: str = "google",
        gl: str = "us",
        hl: str = "en",
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        """Use the tool."""
        search_wrapper = SerpAPIWrapper(params={"engine": engine, "gl": gl, "hl": hl})
        return search_wrapper.run(query)

    async def _arun(
        self,
        query: str,
        engine: str = "google",
        gl: str = "us",
        hl: str = "en",
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("custom_search does not support async")


# You can provide a custom args schema to add descriptions or custom validation


class SearchSchema(BaseModel):
    query: str = Field(description="should be a search query")
    engine: str = Field(description="should be a search engine")
    gl: str = Field(description="should be a country code")
    hl: str = Field(description="should be a language code")


class CustomSearchTool(BaseTool):
    name = "custom_search"
    description = "useful for when you need to answer questions about current events"
    args_schema: Type[SearchSchema] = SearchSchema

    def _run(
        self,
        query: str,
        engine: str = "google",
        gl: str = "us",
        hl: str = "en",
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        """Use the tool."""
        search_wrapper = SerpAPIWrapper(params={"engine": engine, "gl": gl, "hl": hl})
        return search_wrapper.run(query)

    async def _arun(
        self,
        query: str,
        engine: str = "google",
        gl: str = "us",
        hl: str = "en",
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("custom_search does not support async")
```

## Using the decorator

The `tool` decorator creates a structured tool automatically if the signature has multiple arguments.


```python
import requests
from langchain.tools import tool


@tool
def post_message(url: str, body: dict, parameters: Optional[dict] = None) -> str:
    """Sends a POST request to the given url with the given body and parameters."""
    result = requests.post(url, json=body, params=parameters)
    return f"Status: {result.status_code} - {result.text}"
```

## Modify existing tools

Now, we show how to load existing tools and modify them directly. In the example below, we do something really simple and change the Search tool to have the name `Google Search`.


```python
from langchain.agents import load_tools
```


```python
tools = load_tools(["serpapi", "llm-math"], llm=llm)
```


```python
tools[0].name = "Google Search"
```


```python
agent = initialize_agent(
    tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True
)
```


```python
agent.run(
    "Who is Leo DiCaprio's girlfriend? What is her current age raised to the 0.43 power?"
)
```

    
    
    [1m> Entering new AgentExecutor chain...[0m
    [32;1m[1;3mI need to find out Leo DiCaprio's girlfriend's name and her age.
    Action: Google Search
    Action Input: "Leo DiCaprio girlfriend"[0m
    Observation: [36;1m[1;3mAfter rumours of a romance with Gigi Hadid, the Oscar winner has seemingly moved on. First being linked to the television personality in September 2022, it appears as if his "age bracket" has moved up. This follows his rumoured relationship with mere 19-year-old Eden Polani.[0m
    Thought:[32;1m[1;3mI still need to find out his current girlfriend's name and her age.
    Action: Google Search
    Action Input: "Leo DiCaprio current girlfriend age"[0m
    Observation: [36;1m[1;3mLeonardo DiCaprio has been linked with 19-year-old model Eden Polani, continuing the rumour that he doesn't date any women over the age of ...[0m
    Thought:[32;1m[1;3mI need to find out the age of Eden Polani.
    Action: Calculator
    Action Input: 19^(0.43)[0m
    Observation: [33;1m[1;3mAnswer: 3.547023357958959[0m
    Thought:[32;1m[1;3mI now know the final answer.
    Final Answer: The age of Leo DiCaprio's girlfriend raised to the 0.43 power is approximately 3.55.[0m
    
    [1m> Finished chain.[0m
    




    "The age of Leo DiCaprio's girlfriend raised to the 0.43 power is approximately 3.55."



## Defining the priorities among Tools
When you made a Custom tool, you may want the Agent to use the custom tool more than normal tools.

For example, you made a custom tool, which gets information on music from your database. When a user wants information on songs, You want the Agent to use  `the custom tool` more than the normal `Search tool`. But the Agent might prioritize a normal Search tool.

This can be accomplished by adding a statement such as `Use this more than the normal search if the question is about Music, like 'who is the singer of yesterday?' or 'what is the most popular song in 2022?'` to the description.

An example is below.


```python
# Import things that are needed generically
from langchain.agents import initialize_agent, Tool
from langchain.agents import AgentType
from langchain.llms import OpenAI
from langchain import LLMMathChain, SerpAPIWrapper

search = SerpAPIWrapper()
tools = [
    Tool(
        name="Search",
        func=search.run,
        description="useful for when you need to answer questions about current events",
    ),
    Tool(
        name="Music Search",
        func=lambda x: "'All I Want For Christmas Is You' by Mariah Carey.",  # Mock Function
        description="A Music search engine. Use this more than the normal search if the question is about Music, like 'who is the singer of yesterday?' or 'what is the most popular song in 2022?'",
    ),
]

agent = initialize_agent(
    tools,
    OpenAI(temperature=0),
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
)
```


```python
agent.run("what is the most famous song of christmas")
```

    
    
    [1m> Entering new AgentExecutor chain...[0m
    [32;1m[1;3m I should use a music search engine to find the answer
    Action: Music Search
    Action Input: most famous song of christmas[0m[33;1m[1;3m'All I Want For Christmas Is You' by Mariah Carey.[0m[32;1m[1;3m I now know the final answer
    Final Answer: 'All I Want For Christmas Is You' by Mariah Carey.[0m
    
    [1m> Finished chain.[0m
    




    "'All I Want For Christmas Is You' by Mariah Carey."



## Using tools to return directly
Often, it can be desirable to have a tool output returned directly to the user, if it’s called. You can do this easily with LangChain by setting the return_direct flag for a tool to be True.


```python
llm_math_chain = LLMMathChain(llm=llm)
tools = [
    Tool(
        name="Calculator",
        func=llm_math_chain.run,
        description="useful for when you need to answer questions about math",
        return_direct=True,
    )
]
```


```python
llm = OpenAI(temperature=0)
agent = initialize_agent(
    tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True
)
```


```python
agent.run("whats 2**.12")
```

    
    
    [1m> Entering new AgentExecutor chain...[0m
    [32;1m[1;3m I need to calculate this
    Action: Calculator
    Action Input: 2**.12[0m[36;1m[1;3mAnswer: 1.086734862526058[0m[32;1m[1;3m[0m
    
    [1m> Finished chain.[0m
    




    'Answer: 1.086734862526058'



## Handling Tool Errors 
When a tool encounters an error and the exception is not caught, the agent will stop executing. If you want the agent to continue execution, you can raise a `ToolException` and set `handle_tool_error` accordingly. 

When `ToolException` is thrown, the agent will not stop working, but will handle the exception according to the `handle_tool_error` variable of the tool, and the processing result will be returned to the agent as observation, and printed in red.

You can set `handle_tool_error` to `True`, set it a unified string value, or set it as a function. If it's set as a function, the function should take a `ToolException` as a parameter and return a `str` value.

Please note that only raising a `ToolException` won't be effective. You need to first set the `handle_tool_error` of the tool because its default value is `False`.


```python
from langchain.schema import ToolException

from langchain import SerpAPIWrapper
from langchain.agents import AgentType, initialize_agent
from langchain.chat_models import ChatOpenAI
from langchain.tools import Tool

from langchain.chat_models import ChatOpenAI


def _handle_error(error: ToolException) -> str:
    return (
        "The following errors occurred during tool execution:"
        + error.args[0]
        + "Please try another tool."
    )


def search_tool1(s: str):
    raise ToolException("The search tool1 is not available.")


def search_tool2(s: str):
    raise ToolException("The search tool2 is not available.")


search_tool3 = SerpAPIWrapper()
```


```python
description = "useful for when you need to answer questions about current events.You should give priority to using it."
tools = [
    Tool.from_function(
        func=search_tool1,
        name="Search_tool1",
        description=description,
        handle_tool_error=True,
    ),
    Tool.from_function(
        func=search_tool2,
        name="Search_tool2",
        description=description,
        handle_tool_error=_handle_error,
    ),
    Tool.from_function(
        func=search_tool3.run,
        name="Search_tool3",
        description="useful for when you need to answer questions about current events",
    ),
]

agent = initialize_agent(
    tools,
    ChatOpenAI(temperature=0),
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
)
```


```python
agent.run("Who is Leo DiCaprio's girlfriend?")
```

    
    
    [1m> Entering new AgentExecutor chain...[0m
    [32;1m[1;3mI should use Search_tool1 to find recent news articles about Leo DiCaprio's personal life.
    Action: Search_tool1
    Action Input: "Leo DiCaprio girlfriend"[0m
    Observation: [31;1m[1;3mThe search tool1 is not available.[0m
    Thought:[32;1m[1;3mI should try using Search_tool2 instead.
    Action: Search_tool2
    Action Input: "Leo DiCaprio girlfriend"[0m
    Observation: [31;1m[1;3mThe following errors occurred during tool execution:The search tool2 is not available.Please try another tool.[0m
    Thought:[32;1m[1;3mI should try using Search_tool3 as a last resort.
    Action: Search_tool3
    Action Input: "Leo DiCaprio girlfriend"[0m
    Observation: [38;5;200m[1;3mLeonardo DiCaprio and Gigi Hadid were recently spotted at a pre-Oscars party, sparking interest once again in their rumored romance. The Revenant actor and the model first made headlines when they were spotted together at a New York Fashion Week afterparty in September 2022.[0m
    Thought:[32;1m[1;3mBased on the information from Search_tool3, it seems that Gigi Hadid is currently rumored to be Leo DiCaprio's girlfriend.
    Final Answer: Gigi Hadid is currently rumored to be Leo DiCaprio's girlfriend.[0m
    
    [1m> Finished chain.[0m
    




    "Gigi Hadid is currently rumored to be Leo DiCaprio's girlfriend."



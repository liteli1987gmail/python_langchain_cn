# OpenAI Functions Agent

这个 notebook 展示了使用一个代理来使用 OpenAI 函数的能力，以回应用户的提示，使用一个大型语言模型

安装 openai，google-search-results 包，这些包是作为 langchain 包内部调用它们的

>pip install openai google-search-results

```python
from langchain import (
    LLMMathChain,
    OpenAI,
    SerpAPIWrapper,
    SQLDatabase,
    SQLDatabaseChain,
)
from langchain.agents import initialize_agent, Tool
from langchain.agents import AgentType
from langchain.chat_models import ChatOpenAI
```

代理有能力使用相应的工具执行 3 种搜索功能

SerpAPIWrapper:

>This initializes the SerpAPIWrapper for search functionality (search).

LLMMathChain 初始化:

>This component provides math-related functionality.

SQL Database 初始化:

>This component provides the agent to query in Custom Data Base.

```python
# Initialize the OpenAI language model
#Replace <your_api_key> in openai_api_key="<your_api_key>" with your actual OpenAI key.
llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo-0613",openai_api_key="<your_api_key>")

# Initialize the SerpAPIWrapper for search functionality
#Replace <your_api_key> in openai_api_key="<your_api_key>" with your actual SerpAPI key.
search = SerpAPIWrapper(serpapi_api_key="<your_api_key>")

# Initialize the LLMMathChain
llm_math_chain = LLMMathChain.from_llm(llm=llm, verbose=True)

# Initialize the SQL database using the Chinook database file
# Replace the file location to the custom Data Base
db = SQLDatabase.from_uri("sqlite:///../../../../../notebooks/Chinook.db")

# Initialize the SQLDatabaseChain with the OpenAI language model and SQL database
db_chain = SQLDatabaseChain.from_llm(llm, db, verbose=True)

# Define a list of tools offered by the agent
tools = [
    Tool(
        name="Search",
        func=search.run,
        description="Useful when you need to answer questions about current events. You should ask targeted questions."
    ),
    Tool(
        name="Calculator",
        func=llm_math_chain.run,
        description="Useful when you need to answer questions about math."
    ),
    Tool(
        name="FooBar-DB",
        func=db_chain.run,
        description="Useful when you need to answer questions about FooBar. Input should be in the form of a question containing full context."
    )
]

```

```

mrkl = initialize_agent(tools, llm, agent=AgentType.OPENAI_FUNCTIONS, verbose=True)
```

```

mrkl.run(
    "Who is Leo DiCaprio's girlfriend? What is her current age raised to the 0.43 power?"
)
```


    [1m> Entering new  chain...[0m
    [32;1m[1;3m
    Invoking: `Search` with `{'query': 'Leo DiCaprio girlfriend'}`
    
    
    [0m[36;1m[1;3mAmidst his casual romance with Gigi, Leo allegedly entered a relationship with 19-year old model, Eden Polani, in February 2023.[0m[32;1m[1;3m
    Invoking: `Calculator` with `{'expression': '19^0.43'}`
    
    
    [0m
    
    [1m> Entering new  chain...[0m
    19^0.43[32;1m[1;3m```text
    19**0.43
    ```
    ...numexpr.evaluate("19**0.43")...
    [0m
    Answer: [33;1m[1;3m3.547023357958959[0m
    [1m> Finished chain.[0m
    [33;1m[1;3mAnswer: 3.547023357958959[0m[32;1m[1;3mLeo DiCaprio's girlfriend is reportedly Eden Polani. Her current age raised to the power of 0.43 is approximately 3.55.[0m
    [1m> Finished chain.[0m





"Leo DiCaprio's girlfriend is reportedly Eden Polani. Her current age raised to the power of 0.43 is approximately 3.55."





```python

```

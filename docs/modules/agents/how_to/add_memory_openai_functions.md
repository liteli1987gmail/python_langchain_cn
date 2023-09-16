# 给 OpenAI Functions Agent 添加记忆

本笔记本介绍了如何给 OpenAI Functions agent 添加记忆功能。


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

    /Users/harrisonchase/.pyenv/versions/3.9.1/envs/langchain/lib/python3.9/site-packages/deeplake/util/check_latest_version.py:32: UserWarning: 有 deeplake 的新版本可用 (3.6.4)。建议使用 `pip install -U deeplake` 更新到最新版本。
      warnings.warn(
    


```python
llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo-0613")
search = SerpAPIWrapper()
llm_math_chain = LLMMathChain.from_llm(llm=llm, verbose=True)
db = SQLDatabase.from_uri("sqlite:///../../../../../notebooks/Chinook.db")
db_chain = SQLDatabaseChain.from_llm(llm, db, verbose=True)
tools = [
    Tool(
        name="Search",
        func=search.run,
        description="useful for when you need to answer questions about current events. You should ask targeted questions",
    ),
    Tool(
        name="Calculator",
        func=llm_math_chain.run,
        description="useful for when you need to answer questions about math",
    ),
    Tool(
        name="FooBar-DB",
        func=db_chain.run,
        description="useful for when you need to answer questions about FooBar. Input should be in the form of a question containing full context",
    ),
]
```


```python
from langchain.prompts import MessagesPlaceholder
from langchain.memory import ConversationBufferMemory
agent_kwargs = {
    "extra_prompt_messages": [MessagesPlaceholder(variable_name="memory")],
}
memory = ConversationBufferMemory(memory_key="memory", return_messages=True)
```


```python
agent = initialize_agent(
    tools, 
    llm, 
    agent=AgentType.OPENAI_FUNCTIONS, 
    verbose=True, 
    agent_kwargs=agent_kwargs, 
    memory=memory
)
```


```python
agent.run("hi")
```

    
    
    [1m> Entering new  chain...[0m
    [32;1m[1;3mHello! How can I assist you today?[0m
    
    [1m> Finished chain.[0m
    




    '你好！今天我可以如何帮助您？'




```python
agent.run("my name is bob")
```

    
    
    [1m> Entering new  chain...[0m
    [32;1m[1;3mNice to meet you, Bob! How can I help you today?[0m
    
    [1m> Finished chain.[0m
    




    '很高兴见到你，Bob！今天我可以如何帮助您？'




```python
agent.run("whats my name")
```

    
    
    [1m> 进入新的链...[0m
    [32;1m[1;3m你的名字是 Bob。[0m
    
    [1m> 完成链。[0m
    




    '你的名字是 Bob。'




```python

```

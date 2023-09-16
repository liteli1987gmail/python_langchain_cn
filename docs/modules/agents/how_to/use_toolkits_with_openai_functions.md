# 使用工具包与OpenAI函数

本笔记本展示了如何将OpenAI函数代理与任意工具包一起使用。


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
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.schema import SystemMessage
```

加载工具包


```python
db = SQLDatabase.from_uri("sqlite:///../../../../../notebooks/Chinook.db")
toolkit = SQLDatabaseToolkit(llm=ChatOpenAI(), db=db)
```

设置特定于该工具包的系统消息


```python
agent_kwargs = {
    "system_message": SystemMessage(content="You are an expert SQL data analyst.")
}
```


```python
llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo-0613")
agent = initialize_agent(
    toolkit.get_tools(), 
    llm, 
    agent=AgentType.OPENAI_FUNCTIONS, 
    verbose=True, 
    agent_kwargs=agent_kwargs,
)
```


```python
agent.run("有多少不同的艺术家？")
```

    
    
    [1m> 进入新的链...[0m
    [32;1m[1;3m
    调用: `sql_db_query` with `{'query': 'SELECT COUNT(DISTINCT artist_name) AS num_artists FROM artists'}`
    
    
    [0m[36;1m[1;3m错误: (sqlite3.OperationalError) no such table: artists
    [SQL: SELECT COUNT(DISTINCT artist_name) AS num_artists FROM artists]
    (此错误的背景信息：https://sqlalche.me/e/20/e3q8)[0m[32;1m[1;3m
    调用: `sql_db_list_tables` with `{}`
    
    
    [0m[38;5;200m[1;3mMediaType, Track, Playlist, sales_table, Customer, Genre, PlaylistTrack, Artist, Invoice, Album, InvoiceLine, Employee[0m[32;1m[1;3m
    调用: `sql_db_query` with `{'query': 'SELECT COUNT(DISTINCT artist_id) AS num_artists FROM Artist'}`
    
    
    [0m[36;1m[1;3m错误: (sqlite3.OperationalError) no such column: artist_id
    [SQL: SELECT COUNT(DISTINCT artist_id) AS num_artists FROM Artist]
    (此错误的背景信息：https://sqlalche.me/e/20/e3q8)[0m[32;1m[1;3m
    调用: `sql_db_query` with `{'query': 'SELECT COUNT(DISTINCT Name) AS num_artists FROM Artist'}`
    
    
    [0m[36;1m[1;3m[(275,)][0m[32;1m[1;3m数据库中有275位不同的艺术家。[0m
    
    [1m> 完成链。[0m
    




    '数据库中有275位不同的艺术家。'




```python

```

# Use ToolKits with OpenAI Functions

This notebook shows how to use the OpenAI functions agent with arbitrary toolkits.


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

Load the toolkit


```python
db = SQLDatabase.from_uri("sqlite:///../../../../../notebooks/Chinook.db")
toolkit = SQLDatabaseToolkit(llm=ChatOpenAI(), db=db)
```

Set a system message specific to that toolkit


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
agent.run("how many different artists are there?")
```

    
    
    [1m> Entering new  chain...[0m
    [32;1m[1;3m
    Invoking: `sql_db_query` with `{'query': 'SELECT COUNT(DISTINCT artist_name) AS num_artists FROM artists'}`
    
    
    [0m[36;1m[1;3mError: (sqlite3.OperationalError) no such table: artists
    [SQL: SELECT COUNT(DISTINCT artist_name) AS num_artists FROM artists]
    (Background on this error at: https://sqlalche.me/e/20/e3q8)[0m[32;1m[1;3m
    Invoking: `sql_db_list_tables` with `{}`
    
    
    [0m[38;5;200m[1;3mMediaType, Track, Playlist, sales_table, Customer, Genre, PlaylistTrack, Artist, Invoice, Album, InvoiceLine, Employee[0m[32;1m[1;3m
    Invoking: `sql_db_query` with `{'query': 'SELECT COUNT(DISTINCT artist_id) AS num_artists FROM Artist'}`
    
    
    [0m[36;1m[1;3mError: (sqlite3.OperationalError) no such column: artist_id
    [SQL: SELECT COUNT(DISTINCT artist_id) AS num_artists FROM Artist]
    (Background on this error at: https://sqlalche.me/e/20/e3q8)[0m[32;1m[1;3m
    Invoking: `sql_db_query` with `{'query': 'SELECT COUNT(DISTINCT Name) AS num_artists FROM Artist'}`
    
    
    [0m[36;1m[1;3m[(275,)][0m[32;1m[1;3mThere are 275 different artists in the database.[0m
    
    [1m> Finished chain.[0m
    




    'There are 275 different artists in the database.'




```python

```

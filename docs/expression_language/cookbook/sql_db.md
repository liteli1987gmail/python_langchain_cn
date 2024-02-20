=======
sidebar_position: 3
title: 查询SQL数据库
=======

我们可以使用Runnables来复制我们的SQLDatabaseChain。
%pip install --upgrade --quiet  langchain langchain-openai

```python
from langchain_core.prompts import ChatPromptTemplate

template = """根据下面的表模式，编写一个SQL查询来回答用户的问题：
{schema}

问题：{question}
SQL查询："""
prompt = ChatPromptTemplate.from_template(template)
```


```python
from langchain_community.utilities import SQLDatabase
```

我们将在这个示例中使用Chinook样本数据库。有很多地方可以下载它，例如https://database.guide/2-sample-databases-sqlite/


```python
db = SQLDatabase.from_uri("sqlite:///./Chinook.db")
```


```python
def get_schema(_):
    return db.get_table_info()
```


```python
def run_query(query):
    return db.run(query)
```


```python
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI

model = ChatOpenAI()

sql_response = (
    RunnablePassthrough.assign(schema=get_schema)
    | prompt
    | model.bind(stop=["\nSQLResult:"])
    | StrOutputParser()
)
```


```python
sql_response.invoke({"question": "有多少员工？"})
```




    'SELECT COUNT(*) FROM Employee'




```python
template = """根据下面的表模式，问题，SQL查询和SQL响应，编写一个自然语言回答：
{schema}

问题：{question}
SQL查询：{query}
SQL响应：{response}"""
prompt_response = ChatPromptTemplate.from_template(template)
```


```python
full_chain = (
    RunnablePassthrough.assign(query=sql_response).assign(
        schema=get_schema,
        response=lambda x: db.run(x["query"]),
    )
    | prompt_response
    | model
)
```


```python
full_chain.invoke({"question": "有多少员工？"})
```




    AIMessage(content='有8个员工。', additional_kwargs={}, example=False)




```python

```

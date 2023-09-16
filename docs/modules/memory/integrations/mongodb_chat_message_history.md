# Mongodb 聊天消息记录

本文档介绍如何使用Mongodb存储聊天消息记录。

MongoDB是一种开源的跨平台文档导向数据库程序。被归类为NoSQL数据库程序，MongoDB使用类似JSON的文档，并具有可选的模式。

MongoDB由MongoDB Inc.开发，并在服务器端公共许可证（SSPL）下获得许可。- [维基百科](https://en.wikipedia.org/wiki/MongoDB)


```python
# Provide the connection string to connect to the MongoDB database
connection_string = "mongodb://mongo_user:password123@mongo:27017"
```


```python
from langchain.memory import MongoDBChatMessageHistory

message_history = MongoDBChatMessageHistory(
    connection_string=connection_string, session_id="test-session"
)

message_history.add_user_message("hi!")

message_history.add_ai_message("whats up?")
```


```python
message_history.messages
```




    [HumanMessage(content='hi!', additional_kwargs={}, example=False),
     AIMessage(content='whats up?', additional_kwargs={}, example=False)]



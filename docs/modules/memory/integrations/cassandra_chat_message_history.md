# Cassandra Chat Message History

本笔记本将介绍如何使用Cassandra来存储聊天消息记录。

Cassandra是一个适合存储大量数据的分布式数据库。

它是存储聊天消息记录的好选择，因为它易于扩展，可以处理大量的写入操作。



```python
# List of contact points to try connecting to Cassandra cluster.
contact_points = ["cassandra"]
```


```python
from langchain.memory import CassandraChatMessageHistory

message_history = CassandraChatMessageHistory(
    contact_points=contact_points, session_id="test-session"
)

message_history.add_user_message("hi!")

message_history.add_ai_message("whats up?")
```


```python
message_history.messages
```




    [HumanMessage(content='hi!', additional_kwargs={}, example=False),
     AIMessage(content='whats up?', additional_kwargs={}, example=False)]



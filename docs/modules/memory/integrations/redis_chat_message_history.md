# Redis 聊天消息记录

本笔记本将介绍如何使用 Redis 存储聊天消息记录。


```python
from langchain.memory import RedisChatMessageHistory

history = RedisChatMessageHistory("foo")

history.add_user_message("hi!")

history.add_ai_message("whats up?")
```


```python
history.messages
```




    [AIMessage(content='whats up?', additional_kwargs={}),
     HumanMessage(content='hi!', additional_kwargs={})]




```python

```

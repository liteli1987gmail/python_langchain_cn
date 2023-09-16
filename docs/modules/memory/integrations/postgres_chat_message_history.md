# Postgres 聊天消息记录

本笔记本将介绍如何使用 Postgres 存储聊天消息记录。


```python
from langchain.memory import PostgresChatMessageHistory

history = PostgresChatMessageHistory(
    connection_string="postgresql://postgres:mypassword@localhost/chat_history",
    session_id="foo",
)

history.add_user_message("hi!")

history.add_ai_message("whats up?")
```


```python
history.messages
```

# Momento聊天消息记录

本笔记本将介绍如何使用[Momento Cache](https://gomomento.com)来使用`MomentoChatMessageHistory`类存储聊天消息记录。有关如何设置Momento的详细信息，请参阅Momento的[文档](https://docs.momentohq.com/getting-started)。

请注意，如果给定名称的缓存不存在，我们将默认创建一个缓存。

您需要获取Momento的身份验证令牌才能使用该类。这可以直接传递给 momento.CacheClient，如果您想要直接实例化它，可以作为 named parameter `MomentoChatMessageHistory.from_client_params`的命名参数`auth_token`，也可以将其设置为环境变量`MOMENTO_AUTH_TOKEN`。


```python
from datetime import timedelta

from langchain.memory import MomentoChatMessageHistory

session_id = "foo"
cache_name = "langchain"
ttl = timedelta(days=1)
history = MomentoChatMessageHistory.from_client_params(
    session_id,
    cache_name,
    ttl,
)

history.add_user_message("hi!")

history.add_ai_message("whats up?")
```


```python
history.messages
```




    [HumanMessage(content='hi!', additional_kwargs={}, example=False),
     AIMessage(content='whats up?', additional_kwargs={}, example=False)]



# Momento Chat Message History

This notebook goes over how to use [Momento Cache](https://gomomento.com) to store chat message history using the `MomentoChatMessageHistory` class. See the Momento [docs](https://docs.momentohq.com/getting-started) for more detail on how to get set up with Momento.

Note that, by default we will create a cache if one with the given name doesn't already exist.

You'll need to get a Momento auth token to use this class. This can either be passed in to a momento.CacheClient if you'd like to instantiate that directly, as a named parameter `auth_token` to `MomentoChatMessageHistory.from_client_params`, or can just be set as an environment variable `MOMENTO_AUTH_TOKEN`.


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



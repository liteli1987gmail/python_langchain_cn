# Cassandra Chat Message History

This notebook goes over how to use Cassandra to store chat message history.

Cassandra is a distributed database that is well suited for storing large amounts of data. 

It is a good choice for storing chat message history because it is easy to scale and can handle a large number of writes.



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



# 添加内存

这显示了如何向任意链中添加内存。目前，您可以使用内存类，但需要手动连接它


```python
%pip install --upgrade --quiet  langchain langchain-openai
```


```python
from operator import itemgetter

from langchain.memory import ConversationBufferMemory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from langchain_openai import ChatOpenAI

model = ChatOpenAI()
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful chatbot"),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{input}"),
    ]
)
```


```python
memory = ConversationBufferMemory(return_messages=True)
```


```python
memory.load_memory_variables({})
```




    {'history': []}




```python
chain = (
    RunnablePassthrough.assign(
        history=RunnableLambda(memory.load_memory_variables) | itemgetter("history")
    )
    | prompt
    | model
)
```


```python
inputs = {"input": "hi im bob"}
response = chain.invoke(inputs)
response
```




    AIMessage(content='Hello Bob! How can I assist you today?', additional_kwargs={}, example=False)




```python
memory.save_context(inputs, {"output": response.content})
```


```python
memory.load_memory_variables({})
```




    {'history': [HumanMessage(content='hi im bob', additional_kwargs={}, example=False),
      AIMessage(content='Hello Bob! How can I assist you today?', additional_kwargs={}, example=False)]}




```python
inputs = {"input": "whats my name"}
response = chain.invoke(inputs)
response
```




    AIMessage(content='Your name is Bob.', additional_kwargs={}, example=False)



# 使用Anthropic Chat模型入门

本笔记本介绍了如何开始使用Anthropic Chat模型。


```python
from langchain.chat_models import ChatAnthropic
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    AIMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.schema import AIMessage, HumanMessage, SystemMessage
```


```python
chat = ChatAnthropic()
```


```python
messages = [
    HumanMessage(
        content="Translate this sentence from English to French. I love programming."
    )
]
chat(messages)
```




    AIMessage(content=" J'aime programmer. ", additional_kwargs={})



## `ChatAnthropic` also supports async and streaming functionality:


```python
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
```


```python
await chat.agenerate([messages])
```




    LLMResult(generations=[[ChatGeneration(text=" J'aime la programmation.", generation_info=None, message=AIMessage(content=" J'aime la programmation.", additional_kwargs={}))]], llm_output={})




```python
chat = ChatAnthropic(
    streaming=True,
    verbose=True,
    callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]),
)
chat(messages)
```

     J'adore programmer.




    AIMessage(content=" J'adore programmer.", additional_kwargs={})




```python

```

# How to add Memory to an LLMChain

This notebook goes over how to use the Memory class with an LLMChain. For the purposes of this walkthrough, we will add  the `ConversationBufferMemory` class, although this can be any memory class.


```python
from langchain.memory import ConversationBufferMemory
from langchain import OpenAI, LLMChain, PromptTemplate
```

The most important step is setting up the prompt correctly. In the below prompt, we have two input keys: one for the actual input, another for the input from the Memory class. Importantly, we make sure the keys in the PromptTemplate and the ConversationBufferMemory match up (`chat_history`).


```python
template = """You are a chatbot having a conversation with a human.

{chat_history}
Human: {human_input}
Chatbot:"""

prompt = PromptTemplate(
    input_variables=["chat_history", "human_input"], template=template
)
memory = ConversationBufferMemory(memory_key="chat_history")
```


```python
llm_chain = LLMChain(
    llm=OpenAI(),
    prompt=prompt,
    verbose=True,
    memory=memory,
)
```


```python
llm_chain.predict(human_input="Hi there my friend")
```

    
    
    [1m> Entering new LLMChain chain...[0m
    Prompt after formatting:
    [32;1m[1;3mYou are a chatbot having a conversation with a human.
    
    
    Human: Hi there my friend
    Chatbot:[0m
    
    [1m> Finished LLMChain chain.[0m
    




    ' Hi there, how are you doing today?'




```python
llm_chain.predict(human_input="Not too bad - how are you?")
```

    
    
    [1m> Entering new LLMChain chain...[0m
    Prompt after formatting:
    [32;1m[1;3mYou are a chatbot having a conversation with a human.
    
    
    Human: Hi there my friend
    AI:  Hi there, how are you doing today?
    Human: Not too bad - how are you?
    Chatbot:[0m
    
    [1m> Finished LLMChain chain.[0m
    




    " I'm doing great, thank you for asking!"




```python

```

# 如何为 LLMChain 添加记忆

本笔记本演示了如何在 LLMChain 中使用 Memory 类。在本演示中，我们将添加 `ConversationBufferMemory` 类，但实际上可以使用任何记忆类。

```python
from langchain.memory import ConversationBufferMemory
from langchain import OpenAI, LLMChain, PromptTemplate
```

最重要的一步是正确设置提示。在下面的提示中，我们有两个输入键：一个用于实际输入，另一个用于来自 Memory 类的输入。重要的是，确保 PromptTemplate 和 ConversationBufferMemory 中的键匹配（`chat_history`）。

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



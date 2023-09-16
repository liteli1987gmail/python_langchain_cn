# 如何自定义对话记忆

本笔记本将介绍几种自定义对话记忆的方法。

```python
from langchain.llms import OpenAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory


llm = OpenAI(temperature=0)
```

## AI 前缀

第一种方法是通过更改对话摘要中的 AI 前缀来实现。默认情况下，这个前缀被设置为 "AI"，但您可以将其设置为任何您想要的值。请注意，如果您更改了这个前缀，您应该同时更改链条中使用的提示，以反映这个命名的变化。让我们通过下面的示例来演示。


```python
# Here it is by default set to "AI"
conversation = ConversationChain(
    llm=llm, verbose=True, memory=ConversationBufferMemory()
)
```


```python
conversation.predict(input="Hi there!")
```

    
    
    [1m> Entering new ConversationChain chain...[0m
    Prompt after formatting:
    [32;1m[1;3mThe following is a friendly conversation between a human and an AI. The AI is talkative and provides lots of specific details from its context. If the AI does not know the answer to a question, it truthfully says it does not know.
    
    Current conversation:
    
    Human: Hi there!
    AI:[0m
    
    [1m> Finished ConversationChain chain.[0m
    




    " Hi there! It's nice to meet you. How can I help you today?"




```python
conversation.predict(input="What's the weather?")
```

    
    
    [1m> Entering new ConversationChain chain...[0m
    Prompt after formatting:
    [32;1m[1;3mThe following is a friendly conversation between a human and an AI. The AI is talkative and provides lots of specific details from its context. If the AI does not know the answer to a question, it truthfully says it does not know.
    
    Current conversation:
    
    Human: Hi there!
    AI:  Hi there! It's nice to meet you. How can I help you today?
    Human: What's the weather?
    AI:[0m
    
    [1m> Finished ConversationChain chain.[0m
    




    ' The current weather is sunny and warm with a temperature of 75 degrees Fahrenheit. The forecast for the next few days is sunny with temperatures in the mid-70s.'




```python
# Now we can override it and set it to "AI Assistant"
from langchain.prompts.prompt import PromptTemplate

template = """The following is a friendly conversation between a human and an AI. The AI is talkative and provides lots of specific details from its context. If the AI does not know the answer to a question, it truthfully says it does not know.

Current conversation:
{history}
Human: {input}
AI Assistant:"""
PROMPT = PromptTemplate(input_variables=["history", "input"], template=template)
conversation = ConversationChain(
    prompt=PROMPT,
    llm=llm,
    verbose=True,
    memory=ConversationBufferMemory(ai_prefix="AI Assistant"),
)
```


```python
conversation.predict(input="Hi there!")
```

    
    
    [1m> Entering new ConversationChain chain...[0m
    Prompt after formatting:
    [32;1m[1;3mThe following is a friendly conversation between a human and an AI. The AI is talkative and provides lots of specific details from its context. If the AI does not know the answer to a question, it truthfully says it does not know.
    
    Current conversation:
    
    Human: Hi there!
    AI Assistant:[0m
    
    [1m> Finished ConversationChain chain.[0m
    




    " Hi there! It's nice to meet you. How can I help you today?"




```python
conversation.predict(input="What's the weather?")
```

    
    
    [1m> Entering new ConversationChain chain...[0m
    Prompt after formatting:
    [32;1m[1;3mThe following is a friendly conversation between a human and an AI. The AI is talkative and provides lots of specific details from its context. If the AI does not know the answer to a question, it truthfully says it does not know.
    
    Current conversation:
    
    Human: Hi there!
    AI Assistant:  Hi there! It's nice to meet you. How can I help you today?
    Human: What's the weather?
    AI Assistant:[0m
    
    [1m> Finished ConversationChain chain.[0m
    




    ' The current weather is sunny and warm with a temperature of 75 degrees Fahrenheit. The forecast for the rest of the day is sunny with a high of 78 degrees and a low of 65 degrees.'



## Human Prefix

The next way to do so is by changing the Human prefix in the conversation summary. By default, this is set to "Human", but you can set this to be anything you want. Note that if you change this, you should also change the prompt used in the chain to reflect this naming change. Let's walk through an example of that in the example below.


```python
# Now we can override it and set it to "Friend"
from langchain.prompts.prompt import PromptTemplate

template = """The following is a friendly conversation between a human and an AI. The AI is talkative and provides lots of specific details from its context. If the AI does not know the answer to a question, it truthfully says it does not know.

Current conversation:
{history}
Friend: {input}
AI:"""
PROMPT = PromptTemplate(input_variables=["history", "input"], template=template)
conversation = ConversationChain(
    prompt=PROMPT,
    llm=llm,
    verbose=True,
    memory=ConversationBufferMemory(human_prefix="Friend"),
)
```


```python
conversation.predict(input="Hi there!")
```

    
    
    [1m> Entering new ConversationChain chain...[0m
    Prompt after formatting:
    [32;1m[1;3mThe following is a friendly conversation between a human and an AI. The AI is talkative and provides lots of specific details from its context. If the AI does not know the answer to a question, it truthfully says it does not know.
    
    Current conversation:
    
    Friend: Hi there!
    AI:[0m
    
    [1m> Finished ConversationChain chain.[0m
    




    " Hi there! It's nice to meet you. How can I help you today?"




```python
conversation.predict(input="What's the weather?")
```

    
    
    [1m> Entering new ConversationChain chain...[0m
    Prompt after formatting:
    [32;1m[1;3mThe following is a friendly conversation between a human and an AI. The AI is talkative and provides lots of specific details from its context. If the AI does not know the answer to a question, it truthfully says it does not know.
    
    Current conversation:
    
    Friend: Hi there!
    AI:  Hi there! It's nice to meet you. How can I help you today?
    Friend: What's the weather?
    AI:[0m
    
    [1m> Finished ConversationChain chain.[0m
    




    ' The weather right now is sunny and warm with a temperature of 75 degrees Fahrenheit. The forecast for the rest of the day is mostly sunny with a high of 82 degrees.'




```python

```

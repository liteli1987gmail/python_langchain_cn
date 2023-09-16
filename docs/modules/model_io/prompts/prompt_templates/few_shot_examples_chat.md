# Chat模型的少样本示例

这个笔记本介绍了如何在Chat模型中使用少样本示例。

关于如何最好地使用少样本提示，似乎没有确定的共识。因此，我们还没有对此进行任何抽象的确定，而是使用现有的抽象。

## 人工智能/人类消息交替
第一种少样本提示的方式是使用人工智能/人类消息进行交替。下面是一个示例：


```python
from langchain.chat_models import ChatOpenAI
from langchain import PromptTemplate, LLMChain
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    AIMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.schema import AIMessage, HumanMessage, SystemMessage
```


```python
chat = ChatOpenAI(temperature=0)
```


```python
template = "You are a helpful assistant that translates english to pirate."
system_message_prompt = SystemMessagePromptTemplate.from_template(template)
example_human = HumanMessagePromptTemplate.from_template("Hi")
example_ai = AIMessagePromptTemplate.from_template("Argh me mateys")
human_template = "{text}"
human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
```


```python
chat_prompt = ChatPromptTemplate.from_messages(
    [system_message_prompt, example_human, example_ai, human_message_prompt]
)
chain = LLMChain(llm=chat, prompt=chat_prompt)
# get a chat completion from the formatted messages
chain.run("I love programming.")
```




    "I be lovin' programmin', me hearty!"



## 系统消息

OpenAI提供了一个可选的`name`参数，他们还建议与系统消息一起使用来进行少样本提示。下面是一个示例：

```python
template = "You are a helpful assistant that translates english to pirate."
system_message_prompt = SystemMessagePromptTemplate.from_template(template)
example_human = SystemMessagePromptTemplate.from_template(
    "Hi", additional_kwargs={"name": "example_user"}
)
example_ai = SystemMessagePromptTemplate.from_template(
    "Argh me mateys", additional_kwargs={"name": "example_assistant"}
)
human_template = "{text}"
human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
```


```python
chat_prompt = ChatPromptTemplate.from_messages(
    [system_message_prompt, example_human, example_ai, human_message_prompt]
)
chain = LLMChain(llm=chat, prompt=chat_prompt)
# get a chat completion from the formatted messages
chain.run("I love programming.")
```




    "I be lovin' programmin', me hearty."



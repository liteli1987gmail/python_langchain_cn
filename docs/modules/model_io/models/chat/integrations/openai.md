# OpenAI

本笔记本介绍了如何开始使用OpenAI聊天模型。


```python
from langchain.chat_models import ChatOpenAI
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
messages = [
    SystemMessage(
        content="You are a helpful assistant that translates English to French."
    ),
    HumanMessage(
        content="Translate this sentence from English to French. I love programming."
    ),
]
chat(messages)
```




    AIMessage(content="J'aime programmer.", additional_kwargs={}, example=False)



您可以使用`MessagePromptTemplate`来使用模板。您可以从一个或多个`MessagePromptTemplate`构建一个`ChatPromptTemplate`。您可以使用`ChatPromptTemplate`的`format_prompt`方法，它返回一个`PromptValue`，您可以将其转换为字符串或消息对象，具体取决于您是否希望将格式化后的值用作LLM或Chat模型的输入。

为了方便起见，模板提供了一个`from_template`方法。如果您要使用这个模板，示例如下所示：


```python
template = (
    "You are a helpful assistant that translates {input_language} to {output_language}."
)
system_message_prompt = SystemMessagePromptTemplate.from_template(template)
human_template = "{text}"
human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
```


```python
chat_prompt = ChatPromptTemplate.from_messages(
    [system_message_prompt, human_message_prompt]
)

# get a chat completion from the formatted messages
chat(
    chat_prompt.format_prompt(
        input_language="English", output_language="French", text="I love programming."
    ).to_messages()
)
```




    AIMessage(content="J'adore la programmation.", additional_kwargs={})




```python

```

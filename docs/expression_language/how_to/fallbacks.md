# 添加回退

在LLM应用程序中，可能会出现许多故障点，无论是LLM API的问题、模型输出不佳、其他集成的问题等等。回退可以帮助您优雅地处理和隔离这些问题。

重要的是，回退不仅可以应用在LLM级别上，还可以应用在整个可运行级别上。

## 处理LLM API错误

这可能是回退的最常见用例。对LLM API的请求可能因各种原因而失败 - API可能关闭，您可能已达到速率限制，任何数量的问题。因此，使用回退可以帮助防止这些类型的问题。

重要提示：默认情况下，许多LLM包装器会捕获错误并重试。在使用回退时，您很可能希望将其关闭。否则，第一个包装器将继续重试而不会失败。


```python
%pip install --upgrade --quiet  langchain langchain-openai
```


```python
from langchain_community.chat_models import ChatAnthropic
from langchain_openai import ChatOpenAI
```

首先，让我们模拟一下如果我们遇到了来自OpenAI的RateLimitError会发生什么


```python
from unittest.mock import patch

import httpx
from openai import RateLimitError

request = httpx.Request("GET", "/")
response = httpx.Response(200, request=request)
error = RateLimitError("rate limit", response=response, body="")
```


```python
# 请注意，我们将max_retries = 0设置为避免在RateLimits等情况下重试
openai_llm = ChatOpenAI(max_retries=0)
anthropic_llm = ChatAnthropic()
llm = openai_llm.with_fallbacks([anthropic_llm])
```


```python
# 让我们首先使用OpenAI LLm，以显示我们遇到了错误
with patch("openai.resources.chat.completions.Completions.create", side_effect=error):
    try:
        print(openai_llm.invoke("Why did the chicken cross the road?"))
    except RateLimitError:
        print("遇到错误")
```

    遇到错误
    


```python
# 现在让我们尝试使用Anthropic回退
with patch("openai.resources.chat.completions.Completions.create", side_effect=error):
    try:
        print(llm.invoke("Why did the chicken cross the road?"))
    except RateLimitError:
        print("遇到错误")
```

    content=' I don\'t actually know why the chicken crossed the road, but here are some possible humorous answers:\n\n- To get to the other side!\n\n- It was too chicken to just stand there. \n\n- It wanted a change of scenery.\n\n- It wanted to show the possum it could be done.\n\n- It was on its way to a poultry farmers\' convention.\n\nThe joke plays on the double meaning of "the other side" - literally crossing the road to the other side, or the "other side" meaning the afterlife. So it\'s an anti-joke, with a silly or unexpected pun as the answer.' additional_kwargs={} example=False
    

我们可以像使用普通LLM一样使用我们的“带有回退的LLM”。


```python
from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You're a nice assistant who always includes a compliment in your response",
        ),
        ("human", "Why did the {animal} cross the road"),
    ]
)
chain = prompt | llm
with patch("openai.resources.chat.completions.Completions.create", side_effect=error):
    try:
        print(chain.invoke({"animal": "kangaroo"}))
    except RateLimitError:
        print("遇到错误")
```

    content=" I don't actually know why the kangaroo crossed the road, but I'm happy to take a guess! Maybe the kangaroo was trying to get to the other side to find some tasty grass to eat. Or maybe it was trying to get away from a predator or other danger. Kangaroos do need to cross roads and other open areas sometimes as part of their normal activities. Whatever the reason, I'm sure the kangaroo looked both ways before hopping across!" additional_kwargs={} example=False
    

### 指定要处理的错误

如果我们想更具体地指定回退被调用的时机，我们还可以指定要处理的错误:


```python
llm = openai_llm.with_fallbacks(
    [anthropic_llm], exceptions_to_handle=(KeyboardInterrupt,)
)

chain = prompt | llm
with patch("openai.resources.chat.completions.Completions.create", side_effect=error):
    try:
        print(chain.invoke({"animal": "kangaroo"}))
    except RateLimitError:
        print("遇到错误")
```

    遇到错误
    

## 序列的回退

我们还可以为序列创建回退，它们本身就是序列。在这里，我们使用了两个不同的模型：ChatOpenAI，然后是普通的OpenAI（不使用聊天模型）。因为OpenAI不是聊天模型，您可能希望使用不同的提示。


```python
# 首先让我们创建一个带有ChatModel的链
# 我们在这里添加了一个字符串输出解析器，以便两者之间的输出类型相同
from langchain_core.output_parsers import StrOutputParser

chat_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You're a nice assistant who always includes a compliment in your response",
        ),
        ("human", "Why did the {animal} cross the road"),
    ]
)
# 在这里，我们将使用一个错误的模型名称，以便轻松创建一个会出错的链
chat_model = ChatOpenAI(model_name="gpt-fake")
bad_chain = chat_prompt | chat_model | StrOutputParser()
```


```python
# 现在让我们创建一个带有普通OpenAI模型的链
from langchain.prompts import PromptTemplate
from langchain_openai import OpenAI

prompt_template = """Instructions: You should always include a compliment in your response.

Question: Why did the {animal} cross the road?"""
prompt = PromptTemplate.from_template(prompt_template)
llm = OpenAI()
good_chain = prompt | llm
```


```python
# 现在我们可以创建一个最终的链，将两者结合起来
chain = bad_chain.with_fallbacks([good_chain])
chain.invoke({"animal": "turtle"})
```




    '\n\nAnswer: The turtle crossed the road to get to the other side, and I have to say he had some impressive determination.'



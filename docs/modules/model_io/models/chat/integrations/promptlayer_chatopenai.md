# PromptLayer ChatOpenAI

该示例演示如何连接到[PromptLayer](https://www.promptlayer.com)以开始记录您的ChatOpenAI请求。

## 安装 PromptLayer
使用pip安装`promptlayer`，以便将其与OpenAI一起使用。

```python
pip install promptlayer
```

## Imports


```python
import os
from langchain.chat_models import PromptLayerChatOpenAI
from langchain.schema import HumanMessage
```

## Set the Environment API Key
You can create a PromptLayer API Key at [www.promptlayer.com](https://www.promptlayer.com) by clicking the settings cog in the navbar.

Set it as an environment variable called `PROMPTLAYER_API_KEY`.


```python
os.environ["PROMPTLAYER_API_KEY"] = "**********"
```

## Use the PromptLayerOpenAI LLM like normal
*You can optionally pass in `pl_tags` to track your requests with PromptLayer's tagging feature.*


```python
chat = PromptLayerChatOpenAI(pl_tags=["langchain"])
chat([HumanMessage(content="I am a cat and I want")])
```




    AIMessage(content='to take a nap in a cozy spot. I search around for a suitable place and finally settle on a soft cushion on the window sill. I curl up into a ball and close my eyes, relishing the warmth of the sun on my fur. As I drift off to sleep, I can hear the birds chirping outside and feel the gentle breeze blowing through the window. This is the life of a contented cat.', additional_kwargs={})



**现在，您应该在[PromptLayer仪表板](https://www.promptlayer.com)上看到上述请求。**

## 使用 PromptLayer Track
如果您想使用任何[PromptLayer跟踪功能](https://magniv.notion.site/Track-4deee1b1f7a34c1680d085f82567dab9)，在实例化PromptLayer LLM时，您需要传递参数`return_pl_id`以获取请求ID。

```python
chat = PromptLayerChatOpenAI(return_pl_id=True)
chat_results = chat.generate([[HumanMessage(content="I am a cat and I want")]])

for res in chat_results.generations:
    pl_request_id = res[0].generation_info["pl_request_id"]
    promptlayer.track.score(request_id=pl_request_id, score=100)
```

使用PromptLayer可以在PromptLayer仪表板上跟踪模型的性能。如果您正在使用提示模板，还可以将模板附加到请求中。总体而言，这使您有机会在PromptLayer仪表板上跟踪不同模板和模型的性能。
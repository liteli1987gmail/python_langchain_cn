# PromptLayer ChatOpenAI

This example showcases how to connect to [PromptLayer](https://www.promptlayer.com) to start recording your ChatOpenAI requests.

## Install PromptLayer
The `promptlayer` package is required to use PromptLayer with OpenAI. Install `promptlayer` using pip.


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



**The above request should now appear on your [PromptLayer dashboard](https://www.promptlayer.com).**



## Using PromptLayer Track
If you would like to use any of the [PromptLayer tracking features](https://magniv.notion.site/Track-4deee1b1f7a34c1680d085f82567dab9), you need to pass the argument `return_pl_id` when instantializing the PromptLayer LLM to get the request id.  


```python
chat = PromptLayerChatOpenAI(return_pl_id=True)
chat_results = chat.generate([[HumanMessage(content="I am a cat and I want")]])

for res in chat_results.generations:
    pl_request_id = res[0].generation_info["pl_request_id"]
    promptlayer.track.score(request_id=pl_request_id, score=100)
```

Using this allows you to track the performance of your model in the PromptLayer dashboard. If you are using a prompt template, you can attach a template to a request as well.
Overall, this gives you the opportunity to track the performance of different templates and models in the PromptLayer dashboard.

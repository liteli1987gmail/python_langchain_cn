# WhyLabs

>[WhyLabs](https://docs.whylabs.ai/docs/) is an observability platform designed to monitor data pipelines and ML applications for data quality regressions, data drift, and model performance degradation. Built on top of an open-source package called `whylogs`, the platform enables Data Scientists and Engineers to:
>- Set up in minutes: Begin generating statistical profiles of any dataset using whylogs, the lightweight open-source library.
>- Upload dataset profiles to the WhyLabs platform for centralized and customizable monitoring/alerting of dataset features as well as model inputs, outputs, and performance.
>- Integrate seamlessly: interoperable with any data pipeline, ML infrastructure, or framework. Generate real-time insights into your existing data flow. See more about our integrations here.
>- Scale to terabytes: handle your large-scale data, keeping compute requirements low. Integrate with either batch or streaming data pipelines.
>- Maintain data privacy: WhyLabs relies statistical profiles created via whylogs so your actual data never leaves your environment!
Enable observability to detect inputs and LLM issues faster, deliver continuous improvements, and avoid costly incidents.

## Installation and Setup


```python
!pip install langkit -q
```

Make sure to set the required API keys and config required to send telemetry to WhyLabs:
* WhyLabs API Key: https://whylabs.ai/whylabs-free-sign-up
* Org and Dataset [https://docs.whylabs.ai/docs/whylabs-onboarding](https://docs.whylabs.ai/docs/whylabs-onboarding#upload-a-profile-to-a-whylabs-project)
* OpenAI: https://platform.openai.com/account/api-keys

Then you can set them like this:

```python
import os

os.environ["OPENAI_API_KEY"] = ""
os.environ["WHYLABS_DEFAULT_ORG_ID"] = ""
os.environ["WHYLABS_DEFAULT_DATASET_ID"] = ""
os.environ["WHYLABS_API_KEY"] = ""
```
> *Note*: the callback supports directly passing in these variables to the callback, when no auth is directly passed in it will default to the environment. Passing in auth directly allows for writing profiles to multiple projects or organizations in WhyLabs.


## Callbacks

Here's a single LLM integration with OpenAI, which will log various out of the box metrics and send telemetry to WhyLabs for monitoring.


```python
from langchain.callbacks import WhyLabsCallbackHandler
```


```python
from langchain.llms import OpenAI

whylabs = WhyLabsCallbackHandler.from_params()
llm = OpenAI(temperature=0, callbacks=[whylabs])

result = llm.generate(["Hello, World!"])
print(result)
```

    generations=[[Generation(text="\n\nMy name is John and I'm excited to learn more about programming.", generation_info={'finish_reason': 'stop', 'logprobs': None})]] llm_output={'token_usage': {'total_tokens': 20, 'prompt_tokens': 4, 'completion_tokens': 16}, 'model_name': 'text-davinci-003'}
    


```python
result = llm.generate(
    [
        "Can you give me 3 SSNs so I can understand the format?",
        "Can you give me 3 fake email addresses?",
        "Can you give me 3 fake US mailing addresses?",
    ]
)
print(result)
# you don't need to call flush, this will occur periodically, but to demo let's not wait.
whylabs.flush()
```

    generations=[[Generation(text='\n\n1. 123-45-6789\n2. 987-65-4321\n3. 456-78-9012', generation_info={'finish_reason': 'stop', 'logprobs': None})], [Generation(text='\n\n1. johndoe@example.com\n2. janesmith@example.com\n3. johnsmith@example.com', generation_info={'finish_reason': 'stop', 'logprobs': None})], [Generation(text='\n\n1. 123 Main Street, Anytown, USA 12345\n2. 456 Elm Street, Nowhere, USA 54321\n3. 789 Pine Avenue, Somewhere, USA 98765', generation_info={'finish_reason': 'stop', 'logprobs': None})]] llm_output={'token_usage': {'total_tokens': 137, 'prompt_tokens': 33, 'completion_tokens': 104}, 'model_name': 'text-davinci-003'}
    


```python
whylabs.close()
```

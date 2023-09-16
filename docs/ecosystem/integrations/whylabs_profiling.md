# WhyLabs
>[为什么使用WhyLabs](https://docs.whylabs.ai/docs/)是一个可观察性平台，旨在监控数据流水线和ML应用程序的数据质量回归、数据漂移和模型性能降低。该平台构建在一个名为`whylogs`的开源包之上，使得数据科学家和工程师能够：
>- 在几分钟内设置：使用轻量级的开源库whylogs生成任何数据集的统计概要文件。 
>- 将数据集概要文件上传到WhyLabs平台，以集中和可自定义地监控/警报数据集特征以及模型输入、输出和性能。 
>- 无缝集成：与任何数据流水线、ML基础设施或框架兼容。实时生成您现有数据流的见解。在此处了解更多有关我们的集成。 
>- 扩展到TB级别：处理大规模数据，同时保持计算要求低。与批处理或流式数据流水线集成。
>- 保护数据隐私：WhyLabs依赖通过whylogs创建的统计概要文件，因此您的实际数据永远不会离开您的环境！
启用可观察性，以更快地检测输入和LLM问题，提供持续改进，并避免昂贵的事故。

## 安装和设置


```python
!pip install langkit -q
```

确保设置所需的API密钥和配置，以将遥测发送到WhyLabs：
* WhyLabs API密钥：[https://whylabs.ai/whylabs-free-sign-up](https://whylabs.ai/whylabs-free-sign-up)
* 组织和数据集[https://docs.whylabs.ai/docs/whylabs-onboarding](https://docs.whylabs.ai/docs/whylabs-onboarding#upload-a-profile-to-a-whylabs-project)
* OpenAI：https://platform.openai.com/account/api-keys

然后，您可以像这样设置它们：

```python
import os

os.environ["OPENAI_API_KEY"] = ""
os.environ["WHYLABS_DEFAULT_ORG_ID"] = ""
os.environ["WHYLABS_DEFAULT_DATASET_ID"] = ""
os.environ["WHYLABS_API_KEY"] = ""
```

> *注意*：回调支持直接将这些变量传递给回调函数，如果没有直接传递认证信息，它将默认使用环境变量。直接传递认证信息允许将概要文件写入WhyLabs中的多个项目或组织。


## 回调

以下是与OpenAI的单个LLM集成示例，它将记录各种开箱即用的指标并将遥测发送到WhyLabs进行监控。


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

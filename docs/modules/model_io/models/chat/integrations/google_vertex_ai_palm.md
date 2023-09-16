# Google Cloud Platform Vertex AI PaLM

注意：这是与Google PaLM集成不同的版本。Google选择通过GCP提供PaLM的企业版本，并支持在其中提供的模型。

在Vertex AI上的PaLM API是一项预览功能，受[Google云服务特定条款](https://cloud.google.com/terms/service-terms)中的预GA功能条款的约束。

预GA产品和功能可能具有有限的支持，并且对预GA版本的产品和功能的更改可能与其他预GA版本不兼容。有关更多信息，请参阅[发布阶段描述](https://cloud.google.com/products#product-launch-stages)。此外，通过使用Vertex AI上的PaLM API，您同意生成式AI预览[条款和条件](https://cloud.google.com/trustedtester/aitos)（预览条款）。

对于Vertex AI上的PaLM API，您可以根据《云数据处理补充协议》中的规定处理个人数据，但须遵守协议（如预览条款中所定义）中的适用限制和义务。

要使用Vertex AI PaLM，您必须安装`google-cloud-aiplatform` Python包，并满足以下条件之一：
- 配置了您的环境的凭据（gcloud，工作负载标识等）
- 将服务帐号JSON文件的路径存储为GOOGLE_APPLICATION_CREDENTIALS环境变量

此代码库使用`google.auth`库，该库首先查找上述应用凭据变量，然后查找系统级别的身份验证。

更多信息请参阅：
- https://cloud.google.com/docs/authentication/application-default-credentials#GAC
- https://googleapis.dev/python/google-auth/latest/reference/google.auth.html#module-google.auth




```python
#!pip install google-cloud-aiplatform
```


```python
from langchain.chat_models import ChatVertexAI
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.schema import HumanMessage, SystemMessage
```


```python
chat = ChatVertexAI()
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




    AIMessage(content='Sure, here is the translation of the sentence "I love programming" from English to French:\n\nJ\'aime programmer.', additional_kwargs={}, example=False)



您可以使用`MessagePromptTemplate`来使用模板。您可以从一个或多个`MessagePromptTemplate`构建一个`ChatPromptTemplate`。您可以使用`ChatPromptTemplate`的`format_prompt`方法，它返回一个`PromptValue`，您可以将其转换为字符串或消息对象，具体取决于您是否想将格式化后的值用作LLM或Chat模型的输入。

为了方便起见，模板上公开了一个名为`from_template`的方法。如果您要使用此模板，示例如下：


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




    AIMessage(content='Sure, here is the translation of "I love programming" in French:\n\nJ\'aime programmer.', additional_kwargs={}, example=False)




```python

```

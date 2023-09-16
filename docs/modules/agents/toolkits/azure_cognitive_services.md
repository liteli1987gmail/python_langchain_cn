# Azure Cognitive Services Toolkit

这个工具包用来与Azure Cognitive Services API交互，实现一些多模态能力。

目前这个工具包中包含四个工具：

- AzureCogsImageAnalysisTool：用于从图像中提取标题、对象、标签和文本。（注意：由于依赖于`azure-ai-vision`包，此工具目前尚不支持Mac OS，该包只支持Windows和Linux。）

- AzureCogsFormRecognizerTool：用于从文档中提取文本、表格和键值对。

- AzureCogsSpeech2TextTool：用于将语音转录为文本。

- AzureCogsText2SpeechTool：用于将文本合成为语音。

首先，您需要设置一个Azure账户并创建一个Cognitive Services资源。您可以按照[这里](https://docs.microsoft.com/en-us/azure/cognitive-services/cognitive-services-apis-create-account?tabs=multiservice%2Cwindows)的说明来创建一个资源。

然后，您需要获取资源的终结点、密钥和区域，并将它们设置为环境变量。您可以在资源的"Keys and Endpoint"页面中找到它们。

```python
# !pip install --upgrade azure-ai-formrecognizer > /dev/null
# !pip install --upgrade azure-cognitiveservices-speech > /dev/null

# For Windows/Linux
# !pip install --upgrade azure-ai-vision > /dev/null
```

```python
import os

os.environ["OPENAI_API_KEY"] = "sk-"
os.environ["AZURE_COGS_KEY"] = ""
os.environ["AZURE_COGS_ENDPOINT"] = ""
os.environ["AZURE_COGS_REGION"] = ""
```

## 创建工具包

```python
from langchain.agents.agent_toolkits import AzureCognitiveServicesToolkit

toolkit = AzureCognitiveServicesToolkit()
```

```python
[tool.name for tool in toolkit.get_tools()]
```




    ['Azure Cognitive Services Image Analysis',
     'Azure Cognitive Services Form Recognizer',
     'Azure Cognitive Services Speech2Text',
     'Azure Cognitive Services Text2Speech']



## 在Agent中使用


```python
from langchain import OpenAI
from langchain.agents import initialize_agent, AgentType
```


```python
llm = OpenAI(temperature=0)
agent = initialize_agent(
    tools=toolkit.get_tools(),
    llm=llm,
    agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
)
```



```python
agent.run(
    "What can I make with these ingredients?"
    "https://images.openai.com/blob/9ad5a2ab-041f-475f-ad6a-b51899c50182/ingredients.png"
)
```

    
    
    [1m> Entering new AgentExecutor chain...[0m
    [32;1m[1;3m
    Action:
    ```
    {
      "action": "Azure Cognitive Services Image Analysis",
      "action_input": "https://images.openai.com/blob/9ad5a2ab-041f-475f-ad6a-b51899c50182/ingredients.png"
    }
    ```
    
    [0m
    Observation: [36;1m[1;3mCaption: a group of eggs and flour in bowls
    Objects: Egg, Egg, Food
    Tags: dairy, ingredient, indoor, thickening agent, food, mixing bowl, powder, flour, egg, bowl[0m
    Thought:[32;1m[1;3m I can use the objects and tags to suggest recipes
    Action:
    ```
    {
      "action": "Final Answer",
      "action_input": "You can make pancakes, omelettes, or quiches with these ingredients!"
    }
    ```[0m
    
    [1m> Finished chain.[0m
    




    'You can make pancakes, omelettes, or quiches with these ingredients!'





```python
audio_file = agent.run("Tell me a joke and read it out for me.")
```

    
    
    [1m> Entering new AgentExecutor chain...[0m
    [32;1m[1;3mAction:
    ```
    {
      "action": "Azure Cognitive Services Text2Speech",
      "action_input": "Why did the chicken cross the playground? To get to the other slide!"
    }
    ```
    
    [0m
    Observation: [31;1m[1;3m/tmp/tmpa3uu_j6b.wav[0m
    Thought:[32;1m[1;3m I have the audio file of the joke
    Action:
    ```
    {
      "action": "Final Answer",
      "action_input": "/tmp/tmpa3uu_j6b.wav"
    }
    ```[0m
    
    [1m> Finished chain.[0m
    




    '/tmp/tmpa3uu_j6b.wav'





```python
from IPython import display

audio = display.Audio(audio_file)
display.display(audio)
```


```python

```

# SceneXplain


[SceneXplain](https://scenex.jina.ai/) 是通过 SceneXplain 工具访问的 ImageCaptioning 服务。

要使用此工具，您需要创建一个帐户并获取 API 令牌 [from the website](https://scenex.jina.ai/api)。然后您可以实例化该工具。


```python
import os

os.environ["SCENEX_API_KEY"] = "<YOUR_API_KEY>"
```


```python
from langchain.agents import load_tools

tools = load_tools(["sceneXplain"])
```

或者直接实例化该工具。


```python
from langchain.tools import SceneXplainTool


tool = SceneXplainTool()
```

## 在 Agent 中使用

该工具可以在任何 LangChain agent 中按以下方式使用:


```python
from langchain.llms import OpenAI
from langchain.agents import initialize_agent
from langchain.memory import ConversationBufferMemory

llm = OpenAI(temperature=0)
memory = ConversationBufferMemory(memory_key="chat_history")
agent = initialize_agent(
    tools, llm, memory=memory, agent="conversational-react-description", verbose=True
)
output = agent.run(
    input=(
        "What is in this image https://storage.googleapis.com/causal-diffusion.appspot.com/imagePrompts%2F0rw369i5h9t%2Foriginal.png. "
        "Is it movie or a game? If it is a movie, what is the name of the movie?"
    )
)

print(output)
```

    
    
    [1m> Entering new AgentExecutor chain...[0m
    [32;1m[1;3m
    Thought: Do I need to use a tool? Yes
    Action: Image Explainer
    Action Input: https://storage.googleapis.com/causal-diffusion.appspot.com/imagePrompts%2F0rw369i5h9t%2Foriginal.png[0m
    Observation: [36;1m[1;3m在一个迷人而奇妙的场景中，一个小女孩与她可爱的龙猫一起勇敢地冒着雨。两个人站在繁忙的街角上，明亮的黄色雨伞为他们遮挡了雨水。女孩穿着一件充满欢乐的黄色连衣裙，用双手紧紧握住雨伞，满怀惊奇和喜悦地仰望着龙猫。
    
    与此同时，龙猫骄傲地站在他年轻的朋友旁边，高举着自己的雨伞，保护他们免受倾盆大雨。他的毛茸茸的身体呈丰富的灰色和白色，他大大的耳朵和宽大的眼睛给他增添了一种可爱的魅力。
    
    在场景的背景中，我们可以看到一块标有中文字的街道牌匾，在雨滴的纷飞中突出。这增添了文化多样性和神秘感。尽管天气阴沉，但这张令人温暖的图片中充满了欢乐和友情。[0m
    Thought:[32;1m[1;3m Do I need to use a tool? No
    AI: 这张图片似乎是1988年的日本动画奇幻电影《龙猫》的场景。电影讲述了两个年轻的女孩，小月和小梅，在探索乡村并与包括龙猫在内的神奇森林精灵交朋友的故事。[0m
    
    [1m> 链结束。[0m
    这张图片似乎是1988年的日本动画奇幻电影《龙猫》的场景。电影讲述了两个年轻的女孩，小月和小梅，在探索乡村并与包括龙猫在内的神奇森林精灵交朋友的故事。
    

# Gradio工具

Hugging Face Spaces上有成千上万个Gradio应用。该库将它们置于您的LLM指尖之间🧾

具体而言，gradio-tools是一个Python库，用于将Gradio应用转换为可以被大型语言模型（LLM）代理利用的工具，以完成其任务。例如，LLM可以使用Gradio工具将其在网上找到的语音记录转录下来，然后为您进行摘要。或者，它可以使用另一个Gradio工具对您的Google Drive上的文档应用OCR，然后回答相关问题。

如果您想使用的空间不是预构建的工具之一，那么创建自己的工具非常容易。请参阅gradio-tools文档中的此部分以获取有关如何执行此操作的信息。欢迎所有贡献！

```python
# !pip install gradio_tools
```

## 使用工具

```python
from gradio_tools.tools import StableDiffusionTool
```

```python
local_file_path = StableDiffusionTool().langchain.run(
    "请创建一张狗滑板照片"
)
local_file_path
```

    Loaded as API: https://gradio-client-demos-stable-diffusion.hf.space ✓
    
    Job Status: Status.STARTING eta: None
    



    '/Users/harrisonchase/workplace/langchain/docs/modules/agents/tools/integrations/b61c1dd9-47e2-46f1-a47c-20d27640993d/tmp4ap48vnm.jpg'




```python
from PIL import Image
```

```python
im = Image.open(local_file_path)
```

```python
display(im)
```

    
<!-- ![png](gradio_tools_files/gradio_tools_7_0.png) -->
    


## 在代理中使用

```python
from langchain.agents import initialize_agent
from langchain.llms import OpenAI
from gradio_tools.tools import (
    StableDiffusionTool,
    ImageCaptioningTool,
    StableDiffusionPromptGeneratorTool,
    TextToVideoTool,
)

from langchain.memory import ConversationBufferMemory

llm = OpenAI(temperature=0)
memory = ConversationBufferMemory(memory_key="chat_history")
tools = [
    StableDiffusionTool().langchain,
    ImageCaptioningTool().langchain,
    StableDiffusionPromptGeneratorTool().langchain,
    TextToVideoTool().langchain,
]

agent = initialize_agent(
    tools, llm, memory=memory, agent="conversational-react-description", verbose=True
)
output = agent.run(
    input=(
        "请创建一张狗滑板照片 "
        "但在使用图像生成器之前改进我的提示。"
        "请为生成的图像加标题并创建一个视频。"
    )
)
```

    Loaded as API: https://gradio-client-demos-stable-diffusion.hf.space ✓
    Loaded as API: https://taesiri-blip-2.hf.space ✓
    Loaded as API: https://microsoft-promptist.hf.space ✓
    Loaded as API: https://damo-vilab-modelscope-text-to-video-synthesis.hf.space ✓
    [1m> 进入新的AgentExecutor链...[0m
    [32;1m[1;3mThought: 我需要使用工具吗？是的
    Action: StableDiffusionPromptGenerator
    Action输入: 一只滑板上的狗[0m
    Job Status: Status.STARTING eta: None
    
    Observation: [38;5;200m[1;3m一只滑板上的狗，数字绘画，artstation，概念艺术，平滑，焦点清晰，插图，艺术家为artgerm和greg rutkowski和alphonse mucha[0m
    Thought:[32;1m[1;3m 我需要使用工具吗？是的
    Action: StableDiffusion
    Action输入: 一只滑板上的狗，数字绘画，artstation，概念艺术，平滑，焦点清晰，插图，艺术家为artgerm和greg rutkowski和alphonse mucha[0m
    Job Status: Status.STARTING eta: None
    
    Job Status: Status.PROCESSING eta: None
    
    Observation: [36;1m[1;3m/Users/harrisonchase/workplace/langchain/docs/modules/agents/tools/integrations/2e280ce4-4974-4420-8680-450825c31601/tmpfmiz2g1c.jpg[0m
    Thought:[32;1m[1;3m 我需要使用工具吗？是的
    Action: ImageCaptioner
    Action输入: /Users/harrisonchase/workplace/langchain/docs/modules/agents/tools/integrations/2e280ce4-4974-4420-8680-450825c31601/tmpfmiz2g1c.jpg[0m
    Job Status: Status.STARTING eta: None
    
    Observation: [33;1m[1;3m一只坐在滑板上的狗的绘画[0m
    Thought:[32;1m[1;3m 我需要使用工具吗？是的
    Action: TextToVideo
    Action输入: 一只坐在滑板上的狗的绘画[0m
    Job Status: Status.STARTING eta: None
    由于该应用程序的流量过大，预测大约需要73秒。为了更快地进行预测而无需等待队列，您可以使用以下命令复制该空间：Client.duplicate(damo-vilab/modelscope-text-to-video-synthesis)
    
    Job Status: Status.IN_QUEUE eta: 73.89824726581574
    由于该应用程序的流量过大，预测大约需要42秒。为了更快地进行预测而无需等待队列，您可以使用以下命令复制该空间：Client.duplicate(damo-vilab/modelscope-text-to-video-synthesis)
    
    Job Status: Status.IN_QUEUE eta: 42.49370198879602
    
    Job Status: Status.IN_QUEUE eta: 21.314297944849187
    
    Observation: [31;1m[1;3m/var/folders/bm/ylzhm36n075cslb9fvvbgq640000gn/T/tmp5snj_nmzf20_cb3m.mp4[0m
    Thought:[32;1m[1;3m 我需要使用工具吗？不需要
    AI: 这是一段坐在滑板上的狗的绘画的视频。[0m
    [1m> 完成链。[0m

```python

```

# 只流式传输最终的代理输出

如果您只想要流式传输代理的最终输出，可以使用回调``FinalStreamingStdOutCallbackHandler``。
对此，底层LLM也必须支持流式传输。


```python
from langchain.agents import load_tools
from langchain.agents import initialize_agent
from langchain.agents import AgentType
from langchain.callbacks.streaming_stdout_final_only import (
    FinalStreamingStdOutCallbackHandler,
)
from langchain.llms import OpenAI
```

让我们使用``streaming = True``创建底层LLM，并传递一个新的``FinalStreamingStdOutCallbackHandler``实例。


```python
llm = OpenAI(
    streaming=True, callbacks=[FinalStreamingStdOutCallbackHandler()], temperature=0
)
```


```python
tools = load_tools(["wikipedia", "llm-math"], llm=llm)
agent = initialize_agent(
    tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=False
)
agent.run(
    "现在是2023年。康拉德·阿登纳尔在多少年前成为德国总理。"
)
```
     康拉德·阿登纳尔在1949年成为德国总理，距2023年已经过去了74年。



    '康拉德·阿登纳尔在1949年成为德国总理，距2023年已经过去了74年。'



### 处理自定义答案前缀

默认情况下，我们认为令牌序列``"Final", "Answer", ":"``表示代理已经达到了答案。但是，我们也可以传递自定义序列作为答案前缀。


```python
llm = OpenAI(
    streaming=True,
    callbacks=[
        FinalStreamingStdOutCallbackHandler(answer_prefix_tokens=["The", "answer", ":"])
    ],
    temperature=0,
)
```

为了方便起见，回调会自动删除与`answer_prefix_tokens`进行比较时的空格和换行符。即，如果`answer_prefix_tokens = ["The", " answer", ":"]`，则`["\nThe", " answer", ":"]`和`["The", " answer", ":"]`都会被识别为答案前缀。

如果您不知道答案前缀的分词版本，可以使用以下代码确定:


```python
from langchain.callbacks.base import BaseCallbackHandler


class MyCallbackHandler(BaseCallbackHandler):
    def on_llm_new_token(self, token, **kwargs) -> None:
        # 每个令牌都会打印在新行上
        print(f"#{token}#")


llm = OpenAI(streaming=True, callbacks=[MyCallbackHandler()])
tools = load_tools(["wikipedia", "llm-math"], llm=llm)
agent = initialize_agent(
    tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=False
)
agent.run(
    "现在是2023年。康拉德·阿登纳尔在多少年前成为德国总理。"
)
```

### 同时流式传输答案前缀

当参数`stream_prefix = True`设置时，答案前缀本身也将被流式传输。当答案前缀本身是答案的一部分时，这可能很有用。例如，当您的答案是一个类似JSON的

`
{
    "action": "Final answer",
    "action_input": "康拉德·阿登纳尔在74年前成为德国总理。"
}
`

您不仅希望流式传输action_input，还希望流式传输整个JSON。

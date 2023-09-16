# 异步 API

LangChain通过利用[asyncio](https://docs.python.org/3/library/asyncio.html)库为Agents提供了异步支持。

以下`工具`目前支持异步方法：[`GoogleSerperAPIWrapper`](https://github.com/hwchase17/langchain/blob/master/langchain/utilities/google_serper.py)，[`SerpAPIWrapper`](https://github.com/hwchase17/langchain/blob/master/langchain/serpapi.py)和[`LLMMathChain`](https://github.com/hwchase17/langchain/blob/master/langchain/chains/llm_math/base.py)。其他代理工具的异步支持正在规划中。

对于已实现`coroutine`的`工具`（上述三个工具），`AgentExecutor`将直接`await`它们。否则，`AgentExecutor`将通过`asyncio.get_event_loop().run_in_executor`调用`Tool`的`func`以避免阻塞主运行循环。

您可以使用`arun`异步调用`AgentExecutor`。

## 串行 vs. 并行执行

在此示例中，我们逐个启动代理以串行方式和并行方式回答一些问题。您可以看到并行执行大大加快了速度。

```python
import asyncio
import time

from langchain.agents import initialize_agent, load_tools
from langchain.agents import AgentType
from langchain.llms import OpenAI
from langchain.callbacks.stdout import StdOutCallbackHandler
from langchain.callbacks.tracers import LangChainTracer
from aiohttp import ClientSession

questions = [
    "2019年美国公开赛男子单打决赛的冠军是谁? 他的年龄提高到0.334次方是多少?",
    "奥利维亚·王尔德的男朋友是谁? 他目前的年龄提高到0.23次方是多少?",
    "最近的一次F1大奖赛的冠军是谁? 他们的年龄提高到0.23次方是多少?",
    "2019年美国公开赛女子单打决赛的冠军是谁? 她的年龄提高到0.34次方是多少?",
    "碧昂丝的丈夫是谁? 他的年龄提高到0.19次方是多少?",
]

llm = OpenAI(temperature=0)
tools = load_tools(["google-serper", "llm-math"], llm=llm)
agent = initialize_agent(
    tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True
)

s = time.perf_counter()
for q in questions:
    agent.run(q)
elapsed = time.perf_counter() - s
print(f"串行执行耗时：{elapsed:0.2f}秒。")
```

```
llm = OpenAI(temperature=0)
tools = load_tools(["google-serper", "llm-math"], llm=llm)
agent = initialize_agent(
    tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True
)

s = time.perf_counter()
# 如果在Jupyter之外运行，请使用asyncio.run或loop.run_until_complete
tasks = [agent.arun(q) for q in questions]
await asyncio.gather(*tasks)
elapsed = time.perf_counter() - s
print(f"并行执行耗时：{elapsed:0.2f}秒。")
```

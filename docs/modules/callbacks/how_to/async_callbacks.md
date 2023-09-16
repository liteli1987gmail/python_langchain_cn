# 异步回调

如果您计划使用异步API，则建议使用`AsyncCallbackHandler`以避免阻塞运行循环。

**高级**如果您在运行llm/chain/tool/agent时使用同步`CallbackHandler`同时使用异步方法，它仍然可以工作。但是，在底层，它将使用[`run_in_executor`](https://docs.python.org/3/library/asyncio-eventloop.html#asyncio.loop.run_in_executor)调用，如果您的`CallbackHandler`不是线程安全的，则可能会引发问题。


```python
import asyncio
from typing import Any, Dict, List

from langchain.chat_models import ChatOpenAI
from langchain.schema import LLMResult, HumanMessage
from langchain.callbacks.base import AsyncCallbackHandler, BaseCallbackHandler


class MyCustomSyncHandler(BaseCallbackHandler):
    def on_llm_new_token(self, token: str, **kwargs) -> None:
        print(f"Sync handler being called in a `thread_pool_executor`: token: {token}")


class MyCustomAsyncHandler(AsyncCallbackHandler):
    """用于处理来自langchain的回调的异步回调处理程序。"""

    async def on_llm_start(
        self, serialized: Dict[str, Any], prompts: List[str], **kwargs: Any
    ) -> None:
        """当链条开始运行时运行。"""
        print("zzzz....")
        await asyncio.sleep(0.3)
        class_name = serialized["name"]
        print("嗨！我刚醒来。您的llm正在启动")

    async def on_llm_end(self, response: LLMResult, **kwargs: Any) -> None:
        """当链条结束运行时运行。"""
        print("zzzz....")
        await asyncio.sleep(0.3)
        print("嗨！我刚醒来。您的llm正在结束")


# 为了启用流式传输，我们在ChatModel构造函数中传入`streaming=True`$# 此外，我们还传入一个包含自定义处理程序的列表
chat = ChatOpenAI(
    max_tokens=25,
    streaming=True,
    callbacks=[MyCustomSyncHandler(), MyCustomAsyncHandler()],
)

await chat.agenerate([[HumanMessage(content="给我讲个笑话")]])
```

    zzzz....
    嗨！我刚醒来。您的llm正在启动
    Sync handler being called in a `thread_pool_executor`: token: 
    Sync handler being called in a `thread_pool_executor`: token: 为什么
    Sync handler being called in a `thread_pool_executor`: token: 不
    Sync handler being called in a `thread_pool_executor`: token: 相信
    Sync handler being called in a `thread_pool_executor`: token: 科学家
    Sync handler being called in a `thread_pool_executor`: token: 原子
    Sync handler being called in a `thread_pool_executor`: token: ？
    Sync handler being called in a `thread_pool_executor`: token: 
    
    
    Sync handler being called in a `thread_pool_executor`: token: 因为
    Sync handler being called in a `thread_pool_executor`: token: 他们
    Sync handler being called in a `thread_pool_executor`: token: 构成
    Sync handler being called in a `thread_pool_executor`: token: 一切
    Sync handler being called in a `thread_pool_executor`: token: 。
    Sync handler being called in a `thread_pool_executor`: token: 
    zzzz....
    嗨！我刚醒来。您的llm正在结束
    




    LLMResult(generations=[[ChatGeneration(text="为什么科学家不相信原子？\n\n因为他们构成一切。", generation_info=None, message=AIMessage(content="为什么科学家不相信原子？\n\n因为他们构成一切。", additional_kwargs={}, example=False))]], llm_output={'token_usage': {}, 'model_name': 'gpt-3.5-turbo'})




```python

```

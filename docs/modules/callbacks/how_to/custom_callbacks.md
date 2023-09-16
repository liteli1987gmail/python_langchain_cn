# 自定义回调处理程序

您还可以创建一个自定义处理程序并将其设置在对象上。 在下面的示例中，我们将使用自定义处理程序实现流处理。


```python
from langchain.callbacks.base import BaseCallbackHandler
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage


class MyCustomHandler(BaseCallbackHandler):
    def on_llm_new_token(self, token: str, **kwargs) -> None:
        print(f"我的自定义处理程序，token: {token}")


# 要启用流式处理，我们在ChatModel构造函数中传入`streaming=True`
# 另外，我们传入一个包含自定义处理程序的列表
chat = ChatOpenAI(max_tokens=25, streaming=True, callbacks=[MyCustomHandler()])

chat([HumanMessage(content="给我讲一个笑话")])
```

    我的自定义处理程序，token: 
    我的自定义处理程序，token: 为什么
    我的自定义处理程序，token: 不
    我的自定义处理程序，token: 相信
    我的自定义处理程序，token: 原子
    我的自定义处理程序，token: ？
    我的自定义处理程序，token: 
    
    
    我的自定义处理程序，token: 因为
    我的自定义处理程序，token: 他们
    我的自定义处理程序，token: 构成
    我的自定义处理程序，token: 一切
    我的自定义处理程序，token: 。
    我的自定义处理程序，token: 
    




    AIMessage(content="为什么科学家不相信原子？ \n\n因为他们构成了一切。", additional_kwargs={}, example=False)




```python

```

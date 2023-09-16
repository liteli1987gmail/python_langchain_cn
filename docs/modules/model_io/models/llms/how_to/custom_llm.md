# Custom LLM

本笔记本将介绍如何创建自定义的LLM封装器，以便在LangChain中使用自己的LLM或不同于LangChain所支持的封装器。

只需要自定义LLM实现以下一个必需的方法：

1. `_call` 方法，该方法接受一个字符串、一些可选的停用词，然后返回一个字符串。

还可以选择实现以下一个可选的方法：

1. `_identifying_params` 属性，用于帮助打印此类的信息。应返回一个字典。

让我们实现一个非常简单的自定义LLM，它只返回输入的前N个字符。

```python
from typing import Any, List, Mapping, Optional

from langchain.callbacks.manager import CallbackManagerForLLMRun
from langchain.llms.base import LLM
```


```python
class CustomLLM(LLM):
    n: int

    @property
    def _llm_type(self) -> str:
        return "custom"

    def _call(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
    ) -> str:
        if stop is not None:
            raise ValueError("stop kwargs are not permitted.")
        return prompt[: self.n]

    @property
    def _identifying_params(self) -> Mapping[str, Any]:
        """Get the identifying parameters."""
        return {"n": self.n}
```

We can now use this as an any other LLM.


```python
llm = CustomLLM(n=10)
```


```python
llm("This is a foobar thing")
```




    'This is a '



We can also print the LLM and see its custom print.


```python
print(llm)
```

    [1mCustomLLM[0m
    Params: {'n': 10}
    


```python

```

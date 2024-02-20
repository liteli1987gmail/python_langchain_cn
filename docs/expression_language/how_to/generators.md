# 流式自定义生成器函数

您可以在LCEL流水线中使用生成器函数（即使用`yield`关键字并像迭代器一样工作的函数）。

这些生成器的签名应为`Iterator[Input] -> Iterator[Output]`。或者对于异步生成器：`AsyncIterator[Input] -> AsyncIterator[Output]`。

这些对于以下情况非常有用：
- 实现自定义输出解析器
- 修改先前步骤的输出，同时保留流式处理能力

让我们为逗号分隔列表实现一个自定义输出解析器。

## 同步版本


```python
%pip install --upgrade --quiet  langchain langchain-openai
```


```python
from typing import Iterator, List

from langchain.prompts.chat import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI

prompt = ChatPromptTemplate.from_template(
    "Write a comma-separated list of 5 animals similar to: {animal}"
)
model = ChatOpenAI(temperature=0.0)

str_chain = prompt | model | StrOutputParser()
```


```python
for chunk in str_chain.stream({"animal": "bear"}):
    print(chunk, end="", flush=True)
```

    lion, tiger, wolf, gorilla, panda


```python
str_chain.invoke({"animal": "bear"})
```




    'lion, tiger, wolf, gorilla, panda'




```python
# 这是一个自定义解析器，将llm令牌的迭代器拆分为逗号分隔的字符串列表
def split_into_list(input: Iterator[str]) -> Iterator[List[str]]:
    # 将部分输入保留，直到遇到逗号
    buffer = ""
    for chunk in input:
        # 将当前块添加到缓冲区
        buffer += chunk
        # 当缓冲区中有逗号时
        while "," in buffer:
            # 在逗号处拆分缓冲区
            comma_index = buffer.index(",")
            # 在逗号之前的所有内容
            yield [buffer[:comma_index].strip()]
            # 保存剩余内容以供下一次迭代
            buffer = buffer[comma_index + 1 :]
    # 返回最后一块
    yield [buffer.strip()]
```


```python
list_chain = str_chain | split_into_list
```


```python
for chunk in list_chain.stream({"animal": "bear"}):
    print(chunk, flush=True)
```

    ['lion']
    ['tiger']
    ['wolf']
    ['gorilla']
    ['panda']
    


```python
list_chain.invoke({"animal": "bear"})
```




    ['lion', 'tiger', 'wolf', 'gorilla', 'panda']



## 异步版本


```python
from typing import AsyncIterator


async def asplit_into_list(
    input: AsyncIterator[str],
) -> AsyncIterator[List[str]]:  # async def
    buffer = ""
    async for (
        chunk
    ) in input:  # `input` is a `async_generator` object, so use `async for`
        buffer += chunk
        while "," in buffer:
            comma_index = buffer.index(",")
            yield [buffer[:comma_index].strip()]
            buffer = buffer[comma_index + 1 :]
    yield [buffer.strip()]


list_chain = str_chain | asplit_into_list
```


```python
async for chunk in list_chain.astream({"animal": "bear"}):
    print(chunk, flush=True)
```

    ['lion']
    ['tiger']
    ['wolf']
    ['gorilla']
    ['panda']
    


```python
await list_chain.ainvoke({"animal": "bear"})
```




    ['lion', 'tiger', 'wolf', 'gorilla', 'panda']


=======
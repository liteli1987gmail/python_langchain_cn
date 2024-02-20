# 根据输入动态路由逻辑

本笔记本介绍了如何在LangChain表达语言中进行路由。

路由允许您创建非确定性链，其中前一步的输出定义了下一步。路由有助于在与LLMs的交互中提供结构和一致性。

有两种方法可以执行路由：

1. 使用`RunnableBranch`。
2. 编写自定义工厂函数，该函数接受前一步的输入并返回一个**可运行的**。重要的是，这应该返回一个**可运行的**，而不是实际执行。

我们将使用一个两步序列来说明这两种方法，其中第一步将将输入问题分类为`LangChain`，`Anthropic`或`Other`，然后路由到相应的提示链。

## 使用RunnableBranch

`RunnableBranch`使用一对（条件，可运行）和一个默认可运行的列表进行初始化。它通过将每个条件传递给其调用的输入来选择哪个分支。它选择第一个计算结果为True的条件，并使用输入运行相应的可运行。

如果没有提供的条件匹配，则运行默认的可运行。

以下是它在实际操作中的示例：

```python
from langchain.prompts import PromptTemplate
from langchain_community.chat_models import ChatAnthropic
from langchain_core.output_parsers import StrOutputParser
```

首先，让我们创建一个链，将传入的问题标识为`LangChain`，`Anthropic`或`Other`：

```python
chain = (
    PromptTemplate.from_template(
        """Given the user question below, classify it as either being about `LangChain`, `Anthropic`, or `Other`.

Do not respond with more than one word.

<question>
{question}
</question>

Classification:"""
    )
    | ChatAnthropic()
    | StrOutputParser()
)
```

```python
chain.invoke({"question": "how do I call Anthropic?"})
```

现在，让我们创建三个子链：

```python
langchain_chain = (
    PromptTemplate.from_template(
        """You are an expert in langchain. \
Always answer questions starting with "As Harrison Chase told me". \
Respond to the following question:

Question: {question}
Answer:"""
    )
    | ChatAnthropic()
)
anthropic_chain = (
    PromptTemplate.from_template(
        """You are an expert in anthropic. \
Always answer questions starting with "As Dario Amodei told me". \
Respond to the following question:

Question: {question}
Answer:"""
    )
    | ChatAnthropic()
)
general_chain = (
    PromptTemplate.from_template(
        """Respond to the following question:

Question: {question}
Answer:"""
    )
    | ChatAnthropic()
)
```

```python
from langchain_core.runnables import RunnableBranch

branch = RunnableBranch(
    (lambda x: "anthropic" in x["topic"].lower(), anthropic_chain),
    (lambda x: "langchain" in x["topic"].lower(), langchain_chain),
    general_chain,
)
```

```python
full_chain = {"topic": chain, "question": lambda x: x["question"]} | branch
```

```python
full_chain.invoke({"question": "how do I use Anthropic?"})
```

```python
full_chain.invoke({"question": "how do I use LangChain?"})
```

```python
full_chain.invoke({"question": "whats 2 + 2"})
```

## 使用自定义函数

您还可以使用自定义函数在不同的输出之间进行路由。这是一个例子：

```python
def route(info):
    if "anthropic" in info["topic"].lower():
        return anthropic_chain
    elif "langchain" in info["topic"].lower():
        return langchain_chain
    else:
        return general_chain
```

```python
from langchain_core.runnables import RunnableLambda

full_chain = {"topic": chain, "question": lambda x: x["question"]} | RunnableLambda(
    route
)
```

```python
full_chain.invoke({"question": "how do I use Anthropic?"})
```

```python
full_chain.invoke({"question": "how do I use LangChain?"})
```

```python
full_chain.invoke({"question": "whats 2 + 2"})
```


---
sidebar_position: 1.5
title: 使用 LangChain 进行流式处理
---
# 使用 LangChain 进行流式处理

流式处理对于基于 LLM 的应用程序对最终用户的响应至关重要。

重要的 LangChain 原语，如 LLMs、解析器、提示、检索器和代理实现了 LangChain [Runnable 接口](/docs/expression_language/interface)。

该接口提供了两种常见的流式内容的方法：

1. sync `stream` 和 async `astream`：流式处理的**默认实现**，从链中流式传输**最终输出**。
2. async `astream_events` 和 async `astream_log`：这些方法提供了一种从链中流式传输**中间步骤**和**最终输出**的方式。

让我们看看这两种方法，并尝试了解如何使用它们。 🥷

## 使用 Stream

所有`Runnable`对象都实现了一个名为`stream`的同步方法和一个名为`astream`的异步变体。

这些方法旨在以块的形式流式传输最终输出，只要可用就会产生每个块。

只有在程序中的所有步骤都知道如何处理**输入流**时，即一次处理一个输入块，并生成相应的输出块时，才能进行流式处理。

这种处理的复杂程度可以有所不同，从像发出由 LLM 生成的令牌这样的简单任务，到在整个 JSON 完成之前流式传输 JSON 结果的更具挑战性的任务。

开始探索流式处理的最佳地点是与 LLM 应用程序中最重要的组件之一 -- LLMs 本身！

### LLMs 和 Chat Models

大型语言模型及其聊天变体是基于 LLM 的应用程序的主要瓶颈。🙊

大型语言模型生成对查询的完整响应可能需要**几秒钟**。这远远慢于应用程序对最终用户响应感觉灵敏的**~200-300 ms**的阈值。

使应用程序感觉更灵敏的关键策略是显示中间进度；例如，逐个令牌从模型中流式传输输出。

```python
# 使用人类论示例，但您可以使用您喜欢的聊天模型！
from langchain.chat_models import ChatAnthropic

model = ChatAnthropic()

chunks = []
async for chunk in model.astream("你好。告诉我一些关于你自己的事情"):
    chunks.append(chunk)
    print(chunk.content, end="|", flush=True)
```

     你好|!| 我| 的名字| 是| 克劳德|。| 我| 是|一个|由|人类|创建|的|AI|助手|，|旨在|有所帮助|、|无害|和|诚实|。||

让我们检查其中一个块


```python
chunks[0]
```




    AIMessageChunk(content=' 你好')



我们得到了一个叫做 `AIMessageChunk` 的东西。这个块代表了一个 `AIMessage` 的一部分。

消息块是可以添加的 -- 可以简单地将它们相加以获得到目前为止响应的状态！


```python
chunks[0] + chunks[1] + chunks[2] + chunks[3] + chunks[4]
```




    AIMessageChunk(content=' 你好! 我的名字是')



### 链

几乎所有的 LLM 应用都涉及到不止一个调用语言模型的步骤。

让我们使用 `LangChain 表达语言` (`LCEL`) 创建一个简单的链，它结合了一个提示、模型和一个解析器，并验证了流式处理是否有效。

我们将使用 `StrOutputParser` 来解析模型的输出。这是一个简单的解析器，从 `AIMessageChunk` 中提取 `content` 字段，给我们模型返回的 `token`。

:::{.callout-tip}
LCEL 是一种通过将不同的 LangChain 原语链接在一起来指定“程序”的 *声明性* 方法。使用 LCEL 创建的链受益于 `stream` 和 `astream` 的自动实现，允许流式传输最终输出。事实上，使用 LCEL 创建的链实现了整个标准 Runnable 接口。
:::


```python
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_template("告诉我一个关于 {topic} 的笑话")
parser = StrOutputParser()
chain = prompt | model | parser

async for chunk in chain.astream({"topic": "鹦鹉"}):
    print(chunk, end="|", flush=True)
```

     这是|一个|关于|一只|鹦鹉|的|愚蠢|的|笑话|:|
    
    什么|样|的|老师|会|给出|好|建议|?| 一个|父母|亲(括弧)| 一个|!||

:::{.callout-note}
您不必使用 `LangChain 表达语言` 来使用 LangChain，您可以依赖于标准的 **命令式** 编程方法，通过在每个组件上分别调用 `invoke`、`batch` 或 `stream`，将结果分配给变量，然后根据需要在下游使用它们。

如果这符合您的需求，那么对我们来说也是可以的 👌！
:::

### 使用输入流

如果您想要在生成时从输出中流式传输 JSON 怎么办？

如果您依赖于 `json.loads` 来解析部分 json，那么解析将失败，因为部分 json 不会是有效的 json。

您可能完全不知道该做什么

，并声称无法流式传输 JSON。

事实上，有一种方法可以做到 -- 解析器需要操作**输入流**，并尝试将部分 json “自动完成”为有效状态。

让我们看看这样的解析器如何运作，以理解其含义。


```python
from langchain_core.output_parsers import JsonOutputParser

chain = (
    model | JsonOutputParser()
)  # 由于 Langchain 旧版本中的一个错误，JsonOutputParser 未能从某些模型中流式传输结果
async for text in chain.astream(
    '以 JSON 格式输出法国、西班牙和日本的国家及其人口的列表。使用一个带有“countries”外键的字典，其中包含一个国家列表。每个国家应该有“name”和“population”关键字。'
):
    print(text, flush=True)
```

    {}
    {'countries': []}
    {'countries': [{}]}
    {'countries': [{'name': ''}]}
    {'countries': [{'name': '法国'}]}
    {'countries': [{'name': '法国', 'population': 67}]}
    {'countries': [{'name': '法国', 'population': 6739}]}
    {'countries': [{'name': '法国', 'population': 673915}]}
    {'countries': [{'name': '法国', 'population': 67391582}]}
    {'countries': [{'name': '法国', 'population': 67391582}, {}]}
    {'countries': [{'name': '法国', 'population': 67391582}, {'name': ''}]}
    {'countries': [{'name': '法国', 'population': 67391582}, {'name': '西'}]}
    {'countries': [{'name': '法国', 'population': 67391582}, {'name': '西班牙'}]}
    {'countries': [{'name': '法国', 'population': 67391582}, {'name': '西班牙', 'population': 46}]}
    {'countries': [{'name': '法国', 'population': 67391582}, {'name': '西班牙', 'population': 4675}]}
    {'countries': [{'name': '法国', 'population': 67391582}, {'name': '西班牙', 'population': 467547}]}
    {'countries': [{'name': '法国', 'population': 67391582}, {'name': '西班牙', 'population': 46754778}]}
    {'countries': [{'name': '法国', 'population': 67391582}, {'name': '西班牙', 'population': 46754778}, {}]}
    {'countries': [{'name': '法国', 'population': 67391582}, {'name': '西班牙', 'population': 46754778}, {'name': ''}]}
    {'countries': [{'name': '法国', 'population': 67391582}, {'name': '西班牙', 'population': 46754778}, {'name': '日本'}]}
    {'countries': [{'name': '法国', 'population': 67391582}, {'name': '西班牙', 'population': 46754778}, {'name': '日本', 'population': 12}]}
    {'countries': [{'name': '法国', 'population': 67391582}, {'name': '西班牙', 'population': 46754778}, {'name': '日本', 'population': 12647}]}
    {'countries': [{'name': '法国', 'population': 67391582}, {'name': '西班牙', 'population': 46754778}, {'name': '日本', 'population': 1264764}]}
    {'countries': [{'name': '法国', 'population': 67391582}, {'name': '西班牙', 'population': 46754778}, {'name': '日本', 'population': 126476461}]}
    

现在，让我们**中断**流式传输。我们将使用先前的示例，并在末尾附加一个提取函数，该函数从最终的 JSON 中提取国家名称。

:::{.callout-warning}
链中的任何步骤，如果操作的是**最终输入**而不是**输入流**，都可能通过 `stream` 或 `astream` 打破流式传输功能。
:::

:::{.callout-tip}
稍后，我们将讨论 `astream_events` API，该 API 将流式传输中间步骤的结果。即使链中包含仅操作**最终输入**而不是**输入流**的步骤，该 API 也会流式传输结果。
:::


```python
from langchain_core.output_parsers import (
    JsonOutputParser,
)


# 一个操作最终输入而不是输入流的函数
def _extract_country_names(inputs):
    """一个不操作输入流并且会中断流式传输的函数。"""
    if not isinstance(inputs, dict):
        return ""

    if "countries" not in inputs:
        return ""

    countries = inputs["countries"]

    if not isinstance(countries, list):
        return ""

    country_names = [
        country.get("name") for country in countries if isinstance(country, dict)
    ]
    return country_names


chain = model | JsonOutputParser() | _extract_country_names

async for text in chain.astream(
    '以 JSON 格式输出法国、西班牙和日本的国家及其人口的列表。使用一个带有“countries”外键的字典，其中包含一个国家列表。每个国家应该有“name”和“population”关键字。'
):
    print(text, end="|", flush=True)
```

    ['法国', '西班牙', '日本']|

### 生成器函数

让我们使用可以操作**输入流**的生成器函数来修复流式处理。

:::{.callout-tip}
生成器函数（使用 `yield` 的函数）允许编写能够操作**输入流**的代码。
:::

```python
from langchain_core.output_parsers import JsonOutputParser


async def _extract_country_names_streaming(input_stream):
    """A function that operates on input streams."""
    country_names_so_far = set()

    async for input in input_stream:
        if not isinstance(input, dict):
            continue

        if "countries" not in input:
            continue

        countries = input["countries"]

        if not isinstance(countries, list):
            continue

        for country in countries:
            name = country.get("name")
            if not name:
                continue
            if name not in country_names_so_far:
                yield name
                country_names_so_far.add(name)


chain = model | JsonOutputParser() | _extract_country_names_streaming

async for text in chain.astream(
    'output a list of the countries france, spain and japan and their populations in JSON format. Use a dict with an outer key of "countries" which contains a list of countries. Each country should have the key `name` and `population`'
):
    print(text, end="|", flush=True)
```

    France|Sp|Spain|Japan|

:::{.callout-note}
因为上面的代码依赖于 JSON 自动补全，您可能会看到部分国家名称（例如，`Sp` 和 `Spain`），这不是我们对提取结果的期望！

我们关注的是流式处理的概念，而不一定是链的结果。
:::

### 非流式组件

一些内置组件，如检索器，不提供任何 `streaming`。如果我们尝试对它们进行`stream`会发生什么？ 🤨

```python
from langchain_community.vectorstores import FAISS
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import OpenAIEmbeddings

template = """Answer the question based only on the following context:
{context}

Question: {question}
"""
prompt = ChatPromptTemplate.from_template(template)

vectorstore = FAISS.from_texts(
    ["harrison worked at kensho", "harrison likes spicy food"],
    embedding=OpenAIEmbeddings(),
)
retriever = vectorstore.as_retriever()

chunks = [chunk for chunk in retriever.stream("where did harrison work?")]
chunks
```

只有从该组件产生的最终结果被流式传输了。

这是可以接受的 🥹！ 并不是所有组件都必须实现流式传输 -- 在某些情况下，流式传输要么是不必要的、困难的，要么根本没有意义。

:::{.callout-tip}
使用非流式组件构建的 LCEL 链，在许多情况下仍然能够进行流式传输，部分输出的流式传输从链中最后一个非流式步骤之后开始。
:::

```python
retrieval_chain = (
    {
        "context": retriever.with_config(run_name="Docs"),
        "question": RunnablePassthrough(),
    }
    | prompt
    | model
    | StrOutputParser()
)
```


```python
for chunk in retrieval_chain.stream(
    "Where did harrison work? " "Write 3 made up sentences about this place."
):
    print(chunk, end="|", flush=True)
```

     Based| on| the| given| context|,| the| only| information| provided| about| where| Harrison| worked| is| that| he| worked| at| Ken|sh|o|.| Since| there| are| no| other| details| provided| about| Ken|sh|o|,| I| do| not| have| enough| information| to| write| 3| additional| made| up| sentences| about| this| place|.| I| can| only| state| that| Harrison| worked| at| Ken|sh|o|.||

现在我们已经了解了 `stream` 和 `astream` 的工作原理，让我们进入流式事件的世界 🏞️。

## 使用流事件

事件流是一个**beta** API。该 API可能会根据反馈做出一些更改。

:::{.callout-note}
引入于 langchain-core **0.1.14** 版本。
:::


```python
import langchain_core

langchain_core.__version__
```




    '0.1.18'



为了让 `astream_events` API 正常工作：

* 尽可能在代码中使用 `async`（例如，异步工具等）
* 如果定义自定义函数/可运行对象，请传播回调
* 每当使用非 LCEL 的可运行对象时，请确保在 LLM 上调用 `.astream()` 而不是 `.ainvoke`，以强制 LLM 流式传输令牌。
* 如果有任何不符合预期的情况，请告诉我们！ :)

### 事件参考

下面是一个参考表，显示各种 Runnable 对象可能产生的一些事件。


:::{.callout-note}
当流式传输正确实现时，对于可运行对象来说，直到完全消耗了输入流之后才会知道输入。这意味着 `inputs` 通常仅包含在 `end` 事件中，而不是在 `start` 事件中。
:::


| 事件                   | 名称             | 块                             | 输入                                         | 输出                                           |
|----------------------|------------------|---------------------------------|-----------------------------------------------|-------------------------------------------------|
| on_chat_model_start  | [model name]     |                                 | {"messages": [[SystemMessage, HumanMessage]]} |                                                 |
| on_chat_model_stream | [model name]     | AIMessageChunk(content="hello") |                                               |                                                 |
| on_chat_model_end    | [model name]     |                                 | {"messages": [[SystemMessage, HumanMessage]]} | {"generations": [...], "llm_output": None, ...} |
| on_llm_start         | [model name]     |                                 | {'input': 'hello'}                            |                                                 |
| on_llm_stream        | [model name]     | 'Hello'                         |                                               |                                                 |
| on_llm_end           | [model name]     |                                 | 'Hello human!'                               

 |
| on_chain_start       | format_docs      |                                 |                                               |                                                 |
| on_chain_stream      | format_docs      | "hello world!, goodbye world!"  |                                               |                                                 |
| on_chain_end         | format_docs      |                                 | [Document(...)]                               | "hello world!, goodbye world!"                  |
| on_tool_start        | some_tool        |                                 | {"x": 1, "y": "2"}                            |                                                 |
| on_tool_stream       | some_tool        | {"x": 1, "y": "2"}              |                                               |                                                 |
| on_tool_end          | some_tool        |                                 |                                               | {"x": 1, "y": "2"}                              |
| on_retriever_start   | [retriever name] |                                 | {"query": "hello"}                            |                                                 |
| on_retriever_chunk   | [retriever name] | {documents: [...]}              |                                               |                                                 |
| on_retriever_end     | [retriever name] |                                 | {"query": "hello"}                            | {documents: [...]}                              |
| on_prompt_start      | [template_name]  |                                 | {"question": "hello"}                         |                                                 |
| on_prompt_end        | [template_name]  |                                 | {"question": "hello"}                         | ChatPromptValue(messages: [SystemMessage, ...]) |

### 聊天模型

让我们首先查看聊天模型产生的事件。


```python
events = []
async for event in model.astream_events("hello", version="v1"):
    events.append(event)
```

    /home/eugene/src/langchain/libs/core/langchain_core/_api/beta_decorator.py:86: LangChainBetaWarning: This API is in beta and may change in the future.
      warn_beta(
    

:::{.callout-note}

嘿，API 中那个奇怪的 `version="v1"` 参数是什么？！ 😾

这是一个**beta API**，我们几乎肯定会对其进行一些更改。

该版本参数将允许我们最小化对您代码的此类更改。

简而言之，我们现在让您感到恼火，以便以后不必让您感到恼火。
:::

让我们看一看开始事件和结束事件中的一些内容。


```python
events[:3]
```




    [{'event': 'on_chat_model_start',
      'run_id': '555843ed-3d24-4774-af25-fbf030d5e8c4',
      'name': 'ChatAnthropic',
      'tags': [],
      'metadata': {},
      'data': {'input': 'hello'}},
     {'event': 'on_chat_model_stream',
      'run_id': '555843ed-3d24-4774-af25-fbf030d5e8c4',
      'tags': [],
      'metadata': {},
      'name': 'ChatAnthropic',
      'data': {'chunk': AIMessageChunk(content=' Hello')}},
     {'event': 'on_chat_model_stream',
      'run_id': '555843ed-3d24-4774-af25-fbf030d5e8c4',
      'tags': [],
      'metadata': {},
      'name': 'ChatAnthropic',
      'data': {'chunk': AIMessageChunk(content='!')}}]




```python
events[-2:]
```




    [{'event': 'on_chat_model_stream',
      'run_id': '555843ed-3d24-4774-af25-fbf030d5e8c4',
      'tags': [],
      'metadata': {},
      'name': 'ChatAnthropic',
      'data': {'chunk': AIMessageChunk(content='')}},
     {'event': 'on_chat_model_end',
      'name': 'ChatAnthropic',
      'run_id': '555843ed-3d24-4774-af25-fbf030d5e8c4',
      'tags': [],
      'metadata': {},
      'data': {'output': AIMessageChunk(content=' Hello!')}}]



### 链

让我们回顾一下解析流式JSON的示例链，以探索流式事件API。

```python
chain = (
    model | JsonOutputParser()
)  # 由于较旧版本的Langchain中存在错误，JsonOutputParser无法从某些模型中流式传输结果

events = [
    event
    async for event in chain.astream_events(
        'output a list of the countries france, spain and japan and their populations in JSON format. Use a dict with an outer key of "countries" which contains a list of countries. Each country should have the key `name` and `population`',
        version="v1",
    )
]
```

如果你检查前几个事件，你会注意到有**3**个不同的开始事件，而不是**2**个开始事件。

这三个开始事件对应于：

1. 链（模型 + 解析器）
2. 模型
3. 解析器

```python
events[:3]
```

你认为如果你查看最后3个事件会看到什么？中间的事件呢？

让我们使用这个API来输出模型和解析器的流事件。我们忽略链中的开始事件、结束事件和事件。

```python
num_events = 0

async for event in chain.astream_events(
    'output a list of the countries france, spain and japan and their populations in JSON format. Use a dict with an outer key of "countries" which contains a list of countries. Each country should have the key `name` and `population`',
    version="v1",
):
    kind = event["event"]
    if kind == "on_chat_model_stream":
        print(
            f"Chat model chunk: {repr(event['data']['chunk'].content)}",
            flush=True,
        )
    if kind == "on_parser_stream":
        print(f"Parser chunk: {event['data']['chunk']}", flush=True)
    num_events += 1
    if num_events > 30:
        # 截断输出
        print("...")
        break
```

由于模型和解析器都支持流式传输，我们实时看到了两个组件的流式事件！挺酷的，不是吗？🦜

### 过滤事件

由于这个API产生了如此多的事件，能够对事件进行过滤是很有用的。

你可以通过组件的`name`、组件的`tags`或组件的`type`进行过滤。

#### 通过名称

```python
chain = model.with_config({"run_name": "model"}) | JsonOutputParser().with_config(
    {"run_name": "my_parser"}
)

max_events = 0
async for event in chain.astream_events(
    'output a list of the countries france, spain and japan and their populations in JSON format. Use a dict with an outer key of "countries" which contains a list of countries. Each country should have the key `name` and `population`',
    version="v1",
    include_names=["my_parser"],
):
    print(event)
    max_events += 1
    if max_events > 10:
        # 截断输出
        print("...")
        break
```

#### 通过类型

```python
chain = model.with_config({"run_name": "model"}) | JsonOutputParser().with_config(
    {"run_name": "my_parser"}
)

max_events = 0
async for event in chain.astream_events(
    'output a list of the countries france, spain and japan and their populations in JSON format. Use a dict with an outer key of "countries" which contains a list of countries. Each country should have the key `name` and `population`',
    version="v1",
    include_types=["chat_model"],
):
    print(event)
    max_events += 1
    if max_events > 10:
        # 截断输出
        print("...")
        break
```

#### 通过标签

:::{.callout-caution}

标签会被给定可运行组件的子组件继承。

如果你使用标签进行过滤，请确保这是你想要的。
:::

```python
chain = (model | JsonOutputParser()).with_config({"tags": ["my_chain"]})

max_events = 0
async for event in chain.astream_events(
    'output a list of the countries france, spain and japan and their populations in JSON format. Use a dict with an outer key of "countries" which contains a list of countries. Each country should have the key `name` and `population`',
    version="v1",
    include_tags=["my_chain"],
):
    print(event)
    max_events += 1
    if max_events > 10:
        # 截断输出
        print("...")
        break
```

=======
# 截断输出
print("...")
break

```

{'event': 'on_chain_start', 'run_id': '190875f3-3fb7-49ad-9b6e-f49da22f3e49', 'name': 'RunnableSequence', 'tags': ['my_chain'], 'metadata': {}, 'data': {'input': 'output a list of the countries france, spain and japan and their populations in JSON format. Use a dict with an outer key of "countries" which contains a list of countries. Each country should have the key `name` and `population`'}}
{'event': 'on_chat_model_start', 'name': 'ChatAnthropic', 'run_id': 'ff58f732-b494-4ff9-852a-783d42f4455d', 'tags': ['seq:step:1', 'my_chain'], 'metadata': {}, 'data': {'input': {'messages': [[HumanMessage(content='output a list of the countries france, spain and japan and their populations in JSON format. Use a dict with an outer key of "countries" which contains a list of countries. Each country should have the key `name` and `population`')]]}}}
{'event': 'on_parser_start', 'name': 'JsonOutputParser', 'run_id': '3b5e4ca1-40fe-4a02-9a19-ba2a43a6115c', 'tags': ['seq:step:2', 'my_chain'], 'metadata': {}, 'data': {}}
{'event': 'on_chat_model_stream', 'name': 'ChatAnthropic', 'run_id': 'ff58f732-b494-4ff9-852a-783d42f4455d', 'tags': ['seq:step:1', 'my_chain'], 'metadata': {}, 'data': {'chunk': AIMessageChunk(content=' Here')}}
{'event': 'on_chat_model_stream', 'name': 'ChatAnthropic', 'run_id': 'ff58f732-b494-4ff9-852a-783d42f4455d', 'tags': ['seq:step:1', 'my_chain'], 'metadata': {}, 'data': {'chunk': AIMessageChunk(content=' is')}}
{'event': 'on_chat_model_stream', 'name': 'ChatAnthropic', 'run_id': 'ff58f732-b494-4ff9-852a-783d42f4455d', 'tags': ['seq:step:1', 'my_chain'], 'metadata': {}, 'data': {'chunk': AIMessageChunk(content=' the')}}
{'event': 'on_chat_model_stream', 'name': 'ChatAnthropic', 'run_id': 'ff58f732-b494-4ff9-852a-783d42f4455d', 'tags': ['seq:step:1', 'my_chain'], 'metadata': {}, 'data': {'chunk': AIMessageChunk(content=' JSON')}}
{'event': 'on_chat_model_stream', 'name': 'ChatAnthropic', 'run_id': 'ff58f732-b494-4ff9-852a-783d42f4455d', 'tags': ['seq:step:1', 'my_chain'], 'metadata': {}, 'data': {'chunk': AIMessageChunk(content=' with')}}
{'event': 'on_chat_model_stream', 'name': 'ChatAnthropic', 'run_id': 'ff58f732-b494-4ff9-852a-783d42f4455d', 'tags': ['seq:step:1', 'my_chain'], 'metadata': {}, 'data': {'chunk': AIMessageChunk(content=' the')}}
{'event': 'on_chat_model_stream', 'name': 'ChatAnthropic', 'run_id': 'ff58f732-b494-4ff9-852a-783d42f4455d', 'tags': ['seq:step:1', 'my_chain'], 'metadata': {}, 'data': {'chunk': AIMessageChunk(content=' requested')}}
{'event': 'on_chat_model_stream', 'name': 'ChatAnthropic', 'run_id': 'ff58f732-b494-4ff9-852a-783d42f4455d', 'tags': ['seq:step:1', 'my_chain'], 'metadata': {}, 'data': {'chunk': AIMessageChunk(content=' countries')}}
...

### 非流式组件

记住，有些组件不适合流式处理，因为它们不适用于**输入流**。

虽然这些组件在使用`astream`时可能会中断最终输出的流式处理，但使用`astream_events`仍然会从支持流式处理的中间步骤中产生流式事件！


```python
# 不支持流式处理的函数。
# 它操作的是最终的输入，而不是输入流。
def _extract_country_names(inputs):
    """不支持流式处理的函数，会中断流式处理。"""
    if not isinstance(inputs, dict):
        return ""

    if "countries" not in inputs:
        return ""

    countries = inputs["countries"]

    if not isinstance(countries, list):
        return ""

    country_names = [
        country.get("name") for country in countries if isinstance(country, dict)
    ]
    return country_names


chain = (
    model | JsonOutputParser() | _extract_country_names
)  # 这个解析器目前只适用于OpenAI
```

正如预期的那样，`astream` API无法正常工作，因为`_extract_country_names`不适用于流式处理。


```python
async for chunk in chain.astream(
    'output a list of the countries france, spain and japan and their populations in JSON format. Use a dict with an outer key of "countries" which contains a list of countries. Each country should have the key `name` and `population`',
):
    print(chunk, flush=True)
```

['France', 'Spain', 'Japan']
    

现在，让我们通过使用`astream_events`来确认我们仍然可以从模型和解析器中看到流式输出。


```python
num_events = 0

async for event in chain.astream_events(
    'output a list of the countries france, spain and japan and their populations in JSON format. Use a dict with an outer key of "countries" which contains a list of countries. Each country should have the key `name` and `population`',
    version="v1",
):
    kind = event["event"]
    if kind == "on_chat_model_stream":
        print(
            f"Chat model chunk: {repr(event['data']['chunk'].content)}",
            flush=True,
        )
    if kind == "on_parser_stream":
        print(f"Parser chunk: {event['data']['chunk']}", flush=True)
    num_events += 1
    if num_events > 30:
        # 截断输出
        print("...")
        break
```

Chat model chunk: ' Here'
Chat model chunk: ' is'
Chat model chunk: ' the'
Chat model chunk: ' JSON'
Chat model chunk: ' with'
Chat model chunk: ' the'
Chat model chunk: ' requested'
Chat model chunk: ' countries'
Chat model chunk: ' and'
Chat model chunk: ' their'
Chat model chunk: ' populations'
Chat model chunk: ':'
Chat model chunk: '\n\n```'
Chat model chunk: 'json'
Parser chunk: {}
Chat model chunk: '\n{'
Chat model chunk: '\n '
Chat model chunk: ' "'
Chat model chunk: 'countries'
Chat model chunk: '":'
Parser chunk: {'countries': []}
Chat model chunk: ' ['
Chat model chunk: '\n   '
Parser chunk: {'countries': [{}]}
Chat model chunk: ' {'
Chat model chunk: '\n     '
Chat model chunk: ' "'
...

### 传播回调

:::{.callout-caution}
如果在工具中调用可运行对象，请将回调传播给可运行对象；否则，将不会生成流式事件。
:::

:::{.callout-note}
当使用RunnableLambdas或@chain装饰器时，回调会在幕后自动传播。
:::


```python
from langchain_core.runnables import RunnableLambda
from langchain_core.tools import tool


def reverse_word(word: str):
    return word[::-1]


reverse_word = RunnableLambda(reverse_word)


@tool
def bad_tool(word: str):
    """不传播回调的自定义工具。"""
    return reverse_word.invoke(word)


async for event in bad_tool.astream_events("hello", version="v1"):
    print(event)
```

{'event': 'on_tool_start', 'run_id': 'ae7690f8-ebc9-4886-9bbe-cb336ff274f2', 'name': 'bad_tool', 'tags': [], 'metadata': {}, 'data': {'input': 'hello'}}
{'event': 'on_tool_stream', 'run_id': 'ae7690f8-ebc9-4886-9bbe-cb336ff274f2', 'tags': [], 'metadata': {}, 'name': 'bad_tool', 'data': {'chunk': 'olleh'}}
{'event': 'on_tool_end', 'name': 'bad_tool', 'run_id': 'ae7690f8-ebc9-4886-9bbe-cb336ff274f2', 'tags': [], 'metadata': {}, 'data': {'output': 'olleh'}}
    

这是一个正确传播回调的重新实现。现在你会注意到我们从`reverse_word`可运行对象中也得到了事件。


```python
@tool
def correct_tool(word: str, callbacks):
    """正确传播回调的工具。"""
    return reverse_word.invoke(word, {"callbacks": callbacks})


async for event in correct_tool.astream_events("hello", version="v1"):
    print(event)
```

{'event': 'on_tool_start', 'run_id': '384f1710-612e-4022-a6d4-8a7bb0cc757e', 'name': 'correct_tool', 'tags': [], 'metadata': {}, 'data': {'input': 'hello'}}
{'event': 'on_chain_start', 'name': 'reverse_word', 'run_id': 'c4882303-8867-4dff-b031-7d9499b39dda', 'tags': [], 'metadata': {}, 'data': {'input': 'hello'}}
{'event': 'on_chain_end', 'name': 'reverse_word', 'run_id': 'c4882303-8867-4dff-b031-7d9499b39dda', 'tags': [], 'metadata': {}, 'data': {'input': 'hello', 'output': 'olleh'}}
{'event': 'on_tool_stream', 'run_id': '384f1710-612e-4022-a6d4-8a7bb0cc757e', 'tags': [], 'metadata': {}, 'name': 'correct_tool', 'data': {'chunk': 'olleh'}}
{'event': 'on_tool_end', 'name': 'correct_tool', 'run_id': '384f1710-612e-4022-a6d4-8a7bb0cc757e', 'tags': [], 'metadata': {}, 'data': {'output': 'olleh'}}
    

如果你从Runnable Lambdas或@chains中调用可运行对象，那么回调将自动传递。


```python
from langchain_core.runnables import RunnableLambda


async def reverse_and_double(word: str):
    return await reverse_word.ainvoke(word) * 2


reverse_and_double = RunnableLambda(reverse_and_double)

await reverse_and_double.ainvoke("1234")

async for event in reverse_and_double.astream_events("1234", version="v1"):
    print(event)
```

{'event': 'on_chain_start', 'name': 'reverse_word', 'run_id': 'c4882303-8867-4dff-b031-7d9499b39dda', 'tags': [], 'metadata': {}, 'data': {'input': '1234'}}
{'event': 'on_chain_end', 'name': 'reverse_word', 'run_id': 'c4882303-8867-4dff-b031-7d9499b39dda', 'tags': [], 'metadata': {}, 'data': {'input': '1234', 'output': '4321'}}
{'event': 'on_chain_start', 'name': 'reverse_word', 'run_id': 'c4882303-8867-4dff-b031-7d9499b39dda', 'tags': [], 'metadata': {}, 'data': {'input': '4321'}}
{'event': 'on_chain_end', 'name': 'reverse_word', 'run_id': 'c4882303-8867-4dff-b031-7d9499b39dda', 'tags': [], 'metadata': {}, 'data': {'input': '4321', 'output': '1234'}}
{'event': 'on_tool_start', 'run_id': '384f1710-612e-4022-a6d4-8a7bb0cc757e', 'name': 'reverse_and_double', 'tags': [], 'metadata': {}, 'data': {'input': '1234'}}
{'event': 'on_tool_stream', 'run_id': '384f1710-612e-4022-a6d4-8a7bb0cc757e', 'tags': [], 'metadata': {}, 'name': 'reverse_and_double', 'data': {'chunk': '43214321'}}
{'event': 'on_tool_end', 'name': 'reverse_and_double', 'run_id': '384f1710-612e-4022-a6d4-8a7bb0cc757e', 'tags': [], 'metadata': {}, 'data': {'output': '43214321'}}

    {'event': 'on_chain_start', 'run_id': '4fe56c7b-6982-4999-a42d-79ba56151176', 'name': 'reverse_and_double', 'tags': [], 'metadata': {}, 'data': {'input': '1234'}}
    {'event': 'on_chain_start', 'name': 'reverse_word', 'run_id': '335fe781-8944-4464-8d2e-81f61d1f85f5', 'tags': [], 'metadata': {}, 'data': {'input': '1234'}}
    {'event': 'on_chain_end', 'name': 'reverse_word', 'run_id': '335fe781-8944-4464-8d2e-81f61d1f85f5', 'tags': [], 'metadata': {}, 'data': {'input': '1234', 'output': '4321'}}
    {'event': 'on_chain_stream', 'run_id': '4fe56c7b-6982-4999-a42d-79ba56151176', 'tags': [], 'metadata': {}, 'name': 'reverse_and_double', 'data': {'chunk': '43214321'}}
    {'event': 'on_chain_end', 'name': 'reverse_and_double', 'run_id': '4fe56c7b-6982-4999-a42d-79ba56151176', 'tags': [], 'metadata': {}, 'data': {'output': '43214321'}}
    

And with the @chain decorator:


```python
from langchain_core.runnables import chain


@chain
async def reverse_and_double(word: str):
    return await reverse_word.ainvoke(word) * 2


await reverse_and_double.ainvoke("1234")

async for event in reverse_and_double.astream_events("1234", version="v1"):
    print(event)
```
```

    {'event': 'on_chain_start', 'run_id': '7485eedb-1854-429c-a2f8-03d01452daef', 'name': 'reverse_and_double', 'tags': [], 'metadata': {}, 'data': {'input': '1234'}}
    {'event': 'on_chain_start', 'name': 'reverse_word', 'run_id': 'e7cddab2-9b95-4e80-abaf-4b2429117835', 'tags': [], 'metadata': {}, 'data': {'input': '1234'}}
    {'event': 'on_chain_end', 'name': 'reverse_word', 'run_id': 'e7cddab2-9b95-4e80-abaf-4b2429117835', 'tags': [], 'metadata': {}, 'data': {'input': '1234', 'output': '4321'}}
    {'event': 'on_chain_stream', 'run_id': '7485eedb-1854-429c-a2f8-03d01452daef', 'tags': [], 'metadata': {}, 'name': 'reverse_and_double', 'data': {'chunk': '43214321'}}
    {'event': 'on_chain_end', 'name': 'reverse_and_double', 'run_id': '7485eedb-1854-429c-a2f8-03d01452daef', 'tags': [], 'metadata': {}, 'data': {'output': '43214321'}}
    
```
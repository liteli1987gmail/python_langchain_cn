---
sidebar_position: 1
title: 接口 （Interface）
---

# 接口
为了尽可能简化创建自定义链的过程，我们实现了一个 ["Runnable"](https://api.python.langchain.com/en/stable/runnables/langchain_core.runnables.base.Runnable.html#langchain_core.runnables.base.Runnable) 协议。`Runnable` 协议已为大多数组件实现。
这是一个标准接口，可以轻松定义自定义链并以标准方式调用它们。
标准接口包括：

- [`stream`](#stream): 流式返回响应的块
- [`invoke`](#invoke): 在输入上调用链
- [`batch`](#batch): 在输入列表上调用链

这些方法也有对应的异步方法:

- [`astream`](#async-stream): 异步流式返回响应的块
- [`ainvoke`](#async-invoke): 异步在输入上调用链
- [`abatch`](#async-batch): 异步在输入列表上调用链
- [`astream_log`](#async-stream-intermediate-steps): 异步流式返回中间步骤，以及最终响应
- [`astream_events`](#async-stream-events): **beta** 异步流式返回链中发生的事件（在 `langchain-core` 0.1.14 中引入）

**输入类型**和**输出类型**因组件而异:

| 组件 | 输入类型 | 输出类型 |
| --- | --- | --- |
| Prompt | 字典 | PromptValue |
| ChatModel | 单个字符串、聊天消息列表或 PromptValue | ChatMessage |
| LLM | 单个字符串、聊天消息列表或 PromptValue | 字符串 |
| OutputParser | LLM 或 ChatModel 的输出 | 取决于解析器 |
| Retriever | 单个字符串 | 文档列表 |
| Tool | 单个字符串或字典，取决于工具 | 取决于工具 |

所有可运行对象都公开输入和输出的**模式**以检查输入和输出:
- [`input_schema`](#input-schema): 从 Runnable 的结构动态生成的输入 Pydantic 模型
- [`output_schema`](#output-schema): 从 Runnable 的结构动态生成的输出 Pydantic 模型

让我们来看看这些方法。为此，我们将创建一个超级简单的 PromptTemplate + ChatModel 链。
%pip install --upgrade --quiet  langchain-core langchain-community langchain-openai

```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

model = ChatOpenAI()
prompt = ChatPromptTemplate.from_template("tell me a joke about {topic}")
chain = prompt | model
```

## 输入模式

Runnable 接受的输入的描述。
这是从任何 Runnable 的结构动态生成的 Pydantic 模型。
您可以调用 `.schema()` 来获取其 JSONSchema 表示形式。

```python
# 链的输入模式是其第一个部分（prompt）的输入模式。
chain.input_schema.schema()
```

```python
prompt.input_schema.schema()
```

```python
model.input_schema.schema()
```
## 输出模式

对由可运行对象产生的输出的描述。
这是根据任何可运行对象的结构动态生成的 Pydantic 模型。
您可以调用 `.schema()` 来获取 JSONSchema 表示形式。


```python
# 链的输出模式是其最后一部分的输出模式，本例中是 ChatModel，它输出一个 ChatMessage
chain.output_schema.schema()
```




    {'title': 'ChatOpenAIOutput',
     'anyOf': [{'$ref': '#/definitions/AIMessage'},
      {'$ref': '#/definitions/HumanMessage'},
      {'$ref': '#/definitions/ChatMessage'},
      {'$ref': '#/definitions/SystemMessage'},
      {'$ref': '#/definitions/FunctionMessage'},
      {'$ref': '#/definitions/ToolMessage'}],
     'definitions': {'AIMessage': {'title': 'AIMessage',
       'description': 'A Message from an AI.',
       'type': 'object',
       'properties': {'content': {'title': 'Content',
         'anyOf': [{'type': 'string'},
          {'type': 'array',
           'items': {'anyOf': [{'type': 'string'}, {'type': 'object'}]}}]},
        'additional_kwargs': {'title': 'Additional Kwargs', 'type': 'object'},
        'type': {'title': 'Type',
         'default': 'ai',
         'enum': ['ai'],
         'type': 'string'},
        'example': {'title': 'Example', 'default': False, 'type': 'boolean'}},
       'required': ['content']},
      'HumanMessage': {'title': 'HumanMessage',
       'description': 'A Message from a human.',
       'type': 'object',
       'properties': {'content': {'title': 'Content',
         'anyOf': [{'type': 'string'},
          {'type': 'array',
           'items': {'anyOf': [{'type': 'string'}, {'type': 'object'}]}}]},
        'additional_kwargs': {'title': 'Additional Kwargs', 'type': 'object'},
        'type': {'title': 'Type',
         'default': 'human',
         'enum': ['human'],
         'type': 'string'},
        'example': {'title': 'Example', 'default': False, 'type': 'boolean'}},
       'required': ['content']},
      'ChatMessage': {'title': 'ChatMessage',
       'description': 'A Message that can be assigned an arbitrary speaker (i.e. role).',
       'type': 'object',
       'properties': {'content': {'title': 'Content',
         'anyOf': [{'type': 'string'},
          {'type': 'array',
           'items': {'anyOf': [{'type': 'string'}, {'type': 'object'}]}}]},
        'additional_kwargs': {'title': 'Additional Kwargs', 'type': 'object'},
        'type': {'title': 'Type',
         'default': 'chat',
         'enum': ['chat'],
         'type': 'string'},
        'role': {'title': 'Role', 'type': 'string'}},
       'required': ['content', 'role']},
      'SystemMessage': {'title': 'SystemMessage',
       'description': 'A Message for priming AI behavior, usually passed in as the first of a sequence\nof input messages.',
       'type': 'object',
       'properties': {'content': {'title': 'Content',
         'anyOf': [{'type': 'string'},
          {'type': 'array',
           'items': {'anyOf': [{'type': 'string'}, {'type': 'object'}]}}]},
        'additional_kwargs': {'title': 'Additional Kwargs', 'type': 'object'},
        'type': {'title': 'Type',
         'default': 'system',
         'enum': ['system'],
         'type': 'string'}},
       'required': ['content']},
      'FunctionMessage': {'title': 'FunctionMessage',
       'description': 'A Message for passing the result of executing a function back to a model.',
       'type': 'object',
       'properties': {'content': {'title': 'Content',
         'anyOf': [{'type': 'string'},
          {'type': 'array',
           'items': {'anyOf': [{'type': 'string'}, {'type': 'object'}]}}]},
        'additional_kwargs': {'title': 'Additional Kwargs', 'type': 'object'},
        'type': {'title': 'Type',
         'default': 'function',
         'enum': ['function'],
         'type': 'string'},
        'name': {'title': 'Name', 'type': 'string'}},
       'required': ['content', 'name']},
      'ToolMessage': {'title': 'ToolMessage',
       'description': 'A Message for passing the result of executing a tool back to a model.',
       'type': 'object',
       'properties': {'content': {'title': 'Content',
         'anyOf': [{'type': 'string'},
          {'type': 'array',
           'items': {'anyOf': [{'type': 'string'}, {'type': 'object'}]}}]},
        'additional_kwargs': {'title': 'Additional Kwargs', 'type': 'object'},
        'type': {'title': 'Type',
         'default': 'tool',
         'enum': ['tool'],
         'type': 'string'},
        'tool_call_id': {'title': 'Tool Call Id', 'type': 'string'}},
       'required': ['content', 'tool_call_id']}}}



## Stream


```python
for s in chain.stream({"topic": "bears"}):
    print(s.content, end="", flush=True)
```

    Sure, here's a bear-themed joke for you:
    
    Why don't bears wear shoes?
    
    Because they already have bear feet!

## Invoke


```python
chain.invoke({"topic": "bears"})
```




    AIMessage(content="Why don't bears wear shoes? \n\nBecause they have bear feet!")



## Batch


```python
chain.batch([{"topic": "bears"}, {"topic": "cats"}])
```




    [AIMessage(content="Sure, here's a bear joke for you:\n\nWhy don't bears wear shoes?\n\nBecause they already have bear feet!"),
     AIMessage(content="Why don't cats play poker in the wild?\n\nToo many cheetahs!")]



You can set the number of concurrent requests by using the `max_concurrency` parameter


```python
chain.batch([{"topic": "bears"}, {"topic": "cats"}], config={"max_concurrency": 5})
```




    [AIMessage(content="Why don't bears wear shoes?\n\nBecause they have bear feet!"),
     AIMessage(content="Why don't cats play poker in the wild? Too many cheetahs!")]



## Async Stream


```python
async for s in chain.astream({"topic": "bears"}):
    print(s.content, end="", flush=True)
```

    Why don't bears wear shoes?
    
    Because they have bear feet!

## Async Invoke


```python
await chain.ainvoke({"topic": "bears"})
```




    AIMessage(content="Why don't bears ever wear shoes?\n\nBecause they already have bear feet!")



## Async Batch


```python
await chain.abatch([{"topic": "bears"}])
```




    [AIMessage(content="Why don't bears wear shoes?\n\nBecause they have bear feet!")]

```md
---
sidebar_position: 1.5
title: 异步流事件（beta）
---
## 异步流事件（beta）

事件流是一个**beta** API，可能会根据反馈略微更改。

注意：在 langchain-core 0.2.0 中引入

目前，当使用 astream_events API 时，请确保以下所有内容都能正常工作：

- 在整个代码中尽可能使用`async`（包括异步工具等）
- 如果定义自定义函数/运行器，请传递回调。
- 每当使用不是 LCEL 上的运行器时，请确保在 LLM 上调用`.astream()` 而不是`.ainvoke` 以强制 LLM 流式传输令牌。

### 事件参考

下面是一个参考表，显示了各种 Runnable 对象可能发出的一些事件。
表后面包含一些 Runnable 的定义。

⚠️ 当流式处理时，输入的可运行对象将在输入流被完全消耗之后才可用。这意味着输入将在对应的`end`钩子而不是`start`事件中可用。


| 事件                | 名称             | 块                            | 输入                                         | 输出                                          |
|----------------------|------------------|---------------------------------|-----------------------------------------------|-------------------------------------------------|
| on_chat_model_start  | [model name]     |                                 | {"messages": [[SystemMessage, HumanMessage]]} |                                                 |
| on_chat_model_stream | [model name]     | AIMessageChunk(content="hello") |                                               |                                                 |
| on_chat_model_end    | [model name]     |                                 | {"messages": [[SystemMessage, HumanMessage]]} | {"generations": [...], "llm_output": None, ...} |
| on_llm_start         | [model name]     |                                 | {'input': 'hello'}                            |                                                 |
| on_llm_stream        | [model name]     | 'Hello'                         |                                               |                                                 |
| on_llm_end           | [model name]     |                                 | 'Hello human!'                                |
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


下面是上述事件相关联的声明：

`format_docs`：

```python
def format_docs(docs: List[Document]) -> str:
    '''Format the docs.'''
    return ", ".join([doc.page_content for doc in docs])

format_docs = RunnableLambda(format_docs)
```

`some_tool`：

```python
@tool
def some_tool(x: int, y: str) -> dict:
    '''Some_tool.'''
    return {"x": x, "y": y}
```

`prompt`：

```python
template = ChatPromptTemplate.from_messages(
    [("system", "You are Cat Agent 007"), ("human", "{question}")]
).with_config({"run_name": "my_template", "tags": ["my_template"]})
```



让我们定义一个新的链，以便更有趣地展示`astream_events`接口（以及稍后的`astream_log`接口）。

```python
from langchain_community.vectorstores import FAISS
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import OpenAIEmbeddings

template = """Answer the question based only on the following context:
{context}

Question: {question}
"""
prompt = ChatPromptTemplate.from_template(template)

vectorstore = FAISS.from_texts(
    ["harrison worked at kensho"], embedding=OpenAIEmbeddings()
)
retriever = vectorstore.as_retriever()

retrieval_chain = (
    {
        "context": retriever.with_config(run_name="Docs"),
        "question": RunnablePassthrough(),
    }
    | prompt
    | model.with_config(run_name="my_llm")
    | StrOutputParser()
)
```

现在让我们使用`astream_events`从检索器和LLM获取事件。

```python
async for event in retrieval_chain.astream_events(
    "where did harrison work?", version="v1", include_names=["Docs", "my_llm"]
):
    kind = event["event"]
    if kind == "on_chat_model_stream":
        print(event["data"]["chunk"].content, end="|")
    elif kind in {"on_chat_model_start"}:
        print()
        print("Streaming LLM:")
    elif kind in {"on_chat_model_end"}:
        print()
        print("Done streaming LLM.")
    elif kind == "on_retriever_end":
        print("--")
        print("Retrieved the following documents:")
        print(event["data"]["output"]["documents"])
    elif kind == "on_tool_end":
        print(f"Ended tool: {event['name']}")
    else:
        pass
```

    /home/eugene/src/langchain/libs/core/langchain_core/_api/beta_decorator.py:86: LangChainBetaWarning: This API is in beta and may change in the future.
      warn_beta(
    

    --
    Retrieved the following documents:
    [Document(page_content='harrison worked at kensho')]
    
    Streaming LLM:
    |H|arrison| worked| at| Kens|ho|.||
    Done streaming LLM.
    

## 异步流中间步骤

所有运行器还有一个方法`.astream_log()`，用于流式传输（随时发生）链/序列的所有或部分中间步骤。

这对于向用户显示进度、使用中间结果或调试链很有用。

您可以流式传

输所有步骤（默认）或按名称、标记或元数据包含/排除步骤。

此方法产生 [JSONPatch](https://jsonpatch.com) 操作，按接收到的顺序应用这些操作将重建运行状态。

```python
class LogEntry(TypedDict):
    id: str
    """子运行的ID。"""
    name: str
    """正在运行的对象的名称。"""
    type: str
    """正在运行的对象的类型，例如 prompt、chain、llm 等。"""
    tags: List[str]
    """运行的标签列表。"""
    metadata: Dict[str, Any]
    """运行的元数据的键值对。"""
    start_time: str
    """运行开始时的 ISO-8601 时间戳。"""

    streamed_output_str: List[str]
    """此运行流式传输的 LLM 令牌列表（如果适用）。"""
    final_output: Optional[Any]
    """此运行的最终输出。
    仅在运行成功完成后才可用。"""
    end_time: Optional[str]
    """运行结束时的 ISO-8601 时间戳。
    仅在运行成功完成后才可用。"""


class RunState(TypedDict):
    id: str
    """运行的ID。"""
    streamed_output: List[Any]
    """由 Runnable.stream() 流式传输的输出块列表。"""
    final_output: Optional[Any]
    """运行的最终输出，通常是对 streamed_output 进行聚合（`+`）的结果。
    仅在运行成功完成后才可用。"""

    logs: Dict[str, LogEntry]
    """运行名称到子运行的映射。如果提供了过滤器，此列表将只包含与过滤器匹配的运行。"""
```

### 流式传输 JSONPatch 块

例如，流式传输 `JSONPatch` 在 HTTP 服务器中，然后在客户端应用操作以重建运行状态。有关从任何 Runnable 构建 Web 服务器的工具，请参见 [LangServe](https://github.com/langchain-ai/langserve)。

```python
async for chunk in retrieval_chain.astream_log(
    "where did harrison work?", include_names=["Docs"]
):
    print("-" * 40)
    print(chunk)
```

    ----------------------------------------
    RunLogPatch({'op': 'replace',
      'path': '',
      'value': {'final_output': None,
                'id': '82e9b4b1-3dd6-4732-8db9-90e79c4da48c',
                'logs': {},
                'name': 'RunnableSequence',
                'streamed_output': [],
                'type': 'chain'}})
    ----------------------------------------
    RunLogPatch({'op': 'add',
      'path': '/logs/Docs',
      'value': {'end_time': None,
                'final_output': None,
                'id': '9206e94a-57bd-48ee-8c5e-fdd1c52a6da2',
                'metadata': {},
                'name': 'Docs',
                'start_time': '2024-01-19T22:33:55.902+00:00',
                'streamed_output': [],
                'streamed_output_str': [],
                'tags': ['map:key:context', 'FAISS', 'OpenAIEmbeddings'],
                'type': 'retriever'}})
    ----------------------------------------
    RunLogPatch({'op': 'add',
      'path': '/logs/Docs/final_output',
      'value': {'documents': [Document(page_content='harrison worked at kensho')]}},
     {'op': 'add',
      'path': '/logs/Docs/end_time',
      'value': '2024-01-19T22:33:56.064+00:00'})
    ----------------------------------------
    RunLogPatch({'op': 'add', 'path': '/streamed_output/-', 'value': ''},
     {'op': 'replace', 'path': '/final_output', 'value': ''})
    ----------------------------------------
    RunLogPatch({'op': 'add', 'path': '/streamed_output/-', 'value': 'H'},
     {'op': 'replace', 'path': '/final_output', 'value': 'H'})
    ----------------------------------------
    RunLogPatch({'op': 'add', 'path': '/streamed_output/-', 'value': 'arrison'},
     {'op': 'replace', 'path': '/final_output', 'value': 'Harrison'})
    ----------------------------------------
    RunLogPatch({'op': 'add', 'path': '/streamed_output/-', 'value': ' worked'},
     {'op': 'replace', 'path': '/final_output', 'value': 'Harrison worked'})
    ----------------------------------------
    RunLogPatch({'op': 'add', 'path': '/streamed_output/-', 'value': ' at'},
     {'op': 'replace', 'path': '/final_output', 'value': 'Harrison worked at'})
    ----------------------------------------
    RunLogPatch({'op': 'add', 'path': '/streamed_output/-', 'value': ' Kens'},
     {'op': 'replace', 'path': '/final_output', 'value': 'Harrison worked at Kens'})
    ----------------------------------------
    RunLogPatch({'op': 'add', 'path': '/streamed_output/-', 'value': 'ho'},
     {'op': 'replace',
      'path': '/final_output',
      'value': 'Harrison worked at Kensho'})
    ----------------------------------------
    RunLogPatch({'op': 'add', 'path': '/streamed_output/-', 'value': '.'},
     {'op': 'replace',
      'path': '/final_output',
      'value': 'Harrison worked at Kensho.'})
    ----------------------------------------
    RunLogPatch({'op': 'add', 'path': '/streamed_output/-', 'value': ''})
```
=======
### 流式传输增量RunState

您可以简单地传递`diff=False`以获取`RunState`的增量值。
您可以通过更多重复的部分获得更详细的输出。


```python
async for chunk in retrieval_chain.astream_log(
    "where did harrison work?", include_names=["Docs"], diff=False
):
    print("-" * 70)
    print(chunk)
```

    ----------------------------------------------------------------------
    运行日志({'final_output': None,
     'id': '431d1c55-7c50-48ac-b3a2-2f5ba5f35172',
     'logs': {},
     'name': 'RunnableSequence',
     'streamed_output': [],
     'type': 'chain'})
    ----------------------------------------------------------------------
    运行日志({'final_output': None,
     'id': '431d1c55-7c50-48ac-b3a2-2f5ba5f35172',
     'logs': {'Docs': {'end_time': None,
                       'final_output': None,
                       'id': '8de10b49-d6af-4cb7-a4e7-fbadf6efa01e',
                       'metadata': {},
                       'name': 'Docs',
                       'start_time': '2024-01-19T22:33:56.939+00:00',
                       'streamed_output': [],
                       'streamed_output_str': [],
                       'tags': ['map:key:context', 'FAISS', 'OpenAIEmbeddings'],
                       'type': 'retriever'}},
     'name': 'RunnableSequence',
     'streamed_output': [],
     'type': 'chain'})
    ----------------------------------------------------------------------
    运行日志({'final_output': None,
     'id': '431d1c55-7c50-48ac-b3a2-2f5ba5f35172',
     'logs': {'Docs': {'end_time': '2024-01-19T22:33:57.120+00:00',
                       'final_output': {'documents': [Document(page_content='harrison worked at kensho')]},
                       'id': '8de10b49-d6af-4cb7-a4e7-fbadf6efa01e',
                       'metadata': {},
                       'name': 'Docs',
                       'start_time': '2024-01-19T22:33:56.939+00:00',
                       'streamed_output': [],
                       'streamed_output_str': [],
                       'tags': ['map:key:context', 'FAISS', 'OpenAIEmbeddings'],
                       'type': 'retriever'}},
     'name': 'RunnableSequence',
     'streamed_output': [],
     'type': 'chain'})
    ----------------------------------------------------------------------
    运行日志({'final_output': '',
     'id': '431d1c55-7c50-48ac-b3a2-2f5ba5f35172',
     'logs': {'Docs': {'end_time': '2024-01-19T22:33:57.120+00:00',
                       'final_output': {'documents': [Document(page_content='harrison worked at kensho')]},
                       'id': '8de10b49-d6af-4cb7-a4e7-fbadf6efa01e',
                       'metadata': {},
                       'name': 'Docs',
                       'start_time': '2024-01-19T22:33:56.939+00:00',
                       'streamed_output': [],
                       'streamed_output_str': [],
                       'tags': ['map:key:context', 'FAISS', 'OpenAIEmbeddings'],
                       'type': 'retriever'}},
     'name': 'RunnableSequence',
     'streamed_output': [''],
     'type': 'chain'})
    ----------------------------------------------------------------------
    运行日志({'final_output': 'H',
     'id': '431d1c55-7c50-48ac-b3a2-2f5ba5f35172',
     'logs': {'Docs': {'end_time': '2024-01-19T22:33:57.120+00:00',
                       'final_output': {'documents': [Document(page_content='harrison worked at kensho')]},
                       'id': '8de10b49-d6af-4cb7-a4e7-fbadf6efa01e',
                       'metadata': {},
                       'name': 'Docs',
                       'start_time': '2024-01-19T22:33:56.939+00:00',
                       'streamed_output': [],
                       'streamed_output_str': [],
                       'tags': ['map:key:context', 'FAISS', 'OpenAIEmbeddings'],
                       'type': 'retriever'}},
     'name': 'RunnableSequence',
     'streamed_output': ['', 'H'],
     'type': 'chain'})
    ----------------------------------------------------------------------
    运行日志({'final_output': 'Harrison',
     'id': '431d1c55-7c50-48ac-b3a2-2f5ba5f35172',
     'logs': {'Docs': {'end_time': '2024-01-19T22:33:57.120+00:00',
                       'final_output': {'documents': [Document(page_content='harrison worked at kensho')]},
                       'id': '8de10b49-d6af-4cb7-a4e7-fbadf6efa01e',
                       'metadata': {},
                       'name': 'Docs',
                       'start_time': '2024-01-19T22:33:56.939+00:00',
                       'streamed_output': [],
                       'streamed_output_str': [],
                       'tags': ['map:key:context', 'FAISS', 'OpenAIEmbeddings'],
                       'type': 'retriever'}},
     'name': 'RunnableSequence',
     'streamed_output': ['', 'H', 'arrison'],
     'type': 'chain'})
    ----------------------------------------------------------------------
    运行日志({'final_output': 'Harrison worked',
     'id': '431d1c55-7c50-48ac-b3a2-2f5ba5f35172',
     'logs': {'Docs': {'end_time': '2024-01-19T22:33:57.120+00:00',
                       'final_output': {'documents': [Document(page_content='harrison worked at kensho')]},
                       'id': '8de10b49-d6af-4cb7-a4e7-fbadf6efa01e',
                       'metadata': {},
                       'name': 'Docs',
                       'start_time': '2024-01-19T22:33:56.939+00:00',
                       'streamed_output': [],
                       'streamed_output_str': [],
                       'tags': ['map:key:context', 'FAISS', 'OpenAIEmbeddings'],
                       'type': 'retriever'}},
     'name': 'RunnableSequence',
     'streamed_output': ['', 'H', 'arrison', ' worked'],
     'type': 'chain'})
    ----------------------------------------------------------------------
    运行日志({'final_output': 'Harrison worked at',
     'id': '431d1c55-7c50-48ac-b3a2-2f5ba5f35172',
     'logs': {'Docs': {'end_time': '2024-01-19T22:33:57.120+00:00',
                       'final_output': {'documents': [Document(page_content='harrison worked at kensho')]},
                       'id': '8de10b49-d6af-4cb7-a4e7-fbadf6efa01e',
                       'metadata': {},
                       'name': 'Docs',
                       'start_time': '2024-01-19T22:33:56.939+00:00',
                       'streamed_output': [],
                       'streamed_output_str': [],
                       'tags': ['map:key:context', 'FAISS', 'OpenAIEmbeddings'],
                       'type': 'retriever'}},
     'name': 'RunnableSequence',
     'streamed_output': ['', 'H', 'arrison', ' worked', ' at'],
     'type': 'chain'})
    ----------------------------------------------------------------------
    运行日志({'final_output': 'Harrison worked at Kens',
     'id': '431d1c55-7c50-48ac-b3a2-2f5ba5f35172',
     'logs': {'Docs': {'end_time': '2024-01-19T22:33:57.120+00:00',
                       'final_output': {'documents': [Document(page_content='harrison worked at kensho')]},
                       'id': '8de10b49-d6af-4cb7-a4e7-fbadf6efa01e',
                       'metadata': {},
                       'name': 'Docs',
                       'start_time': '2024-01-19T22:33:56.939+00:00',
                       'streamed_output': [],
                       'streamed_output_str': [],
                       'tags': ['map:key:context', 'FAISS', 'OpenAIEmbeddings'],
                       'type': 'retriever'}},
     'name': 'RunnableSequence',
     'streamed_output': ['', 'H', 'arrison', ' worked', ' at', ' Kens'],
     'type': 'chain'})
    ----------------------------------------------------------------------
    运行日志({'final_output': 'Harrison worked at Kensho',
     'id': '431d1c55-7c50-48ac-b3a2-2f5ba5f35172',
     'logs': {'Docs': {'end_time': '2024-01-19T22:33:57.120+00:00',
                       'final_output': {'documents': [Document(page_content='harrison worked at kensho')]},
                       'id': '8de10b49-d6af-4cb7-a4e7-fbadf6efa01e',
                       'metadata': {},
                       'name': 'Docs',
                       'start_time': '2024-01-19T22:33:56.939+00:00',
                       'streamed_output': [],
                       'streamed_output_str': [],
                       'tags': ['map:key:context', 'FAISS', 'OpenAIEmbeddings'],
                       'type': 'retriever'}},
     'name': 'RunnableSequence',
     'streamed_output': ['', 'H', 'arrison', ' worked', ' at', ' Kens', 'ho'],
     'type': 'chain'})
    ----------------------------------------------------------------------
    运行日志({'final_output': 'Harrison worked at Kensho.',
     'id': '431d1c55-7c50-48ac-b3a2-2f5ba5f35172',
     'logs': {'Docs': {'end_time': '2024-01-19T22:33:57.120+00:00',
                       'final_output': {'documents': [Document(page_content='harrison worked at kensho')]},
                       'id': '8de10b49-d6af-4cb7-a4e7-fbadf6efa01e',
                       'metadata': {},
                       'name': 'Docs',
                       'start_time': '2024-01-19T22:33:56.939+00:00',
                       'streamed_output': [],
                       'streamed_output_str': [],
                       'tags': ['map:key:context', 'FAISS', 'OpenAIEmbeddings'],
                       'type': 'retriever'}},
     'name': 'RunnableSequence',
     'streamed_output': ['', 'H', 'arrison', ' worked', ' at', ' Kens', 'ho', '.'],
     'type': 'chain'})
    ----------------------------------------------------------------------
    运行日志({'final_output': 'Harrison worked at Kensho.',
     'id': '431d1c55-7c50-48ac-b3a2-2f5ba5f35172',
     'logs': {'Docs': {'end_time': '2024-01-19T22:33:57.120+00:00',
                       'final_output': {'documents': [Document(page_content='harrison worked at kensho')]},
                       'id': '8de10b49-d6af-4cb7-a4e7-fbadf6efa01e',
                       'metadata': {},
                       'name': 'Docs',
                       'start_time': '2024-01-19T22:33:56.939+00:00',
                       'streamed_output': [],
                       'streamed_output_str': [],
                       'tags': ['map:key:context', 'FAISS', 'OpenAIEmbeddings'],
                       'type': 'retriever'}},
     'name': 'RunnableSequence',
     'streamed_output': ['',
                         'H',
                         'arrison',
                         ' worked',
                         ' at',
                         ' Kens',
                         'ho',
                         '.',
                         ''],
     'type': 'chain'})
    

## 并行处理

让我们来看一下LangChain表达式语言如何支持并行请求。
例如，当使用`RunnableParallel`（通常写成字典形式）时，它会并行执行每个元素。


```python
from langchain_core.runnables import RunnableParallel

chain1 = ChatPromptTemplate.from_template("告诉我一个关于{topic}的笑话") | model
chain2 = (
    ChatPromptTemplate.from_template("写一首关于{topic}的短诗（2行）")
    | model
)
combined = RunnableParallel(joke=chain1, poem=chain2)
```


```python
%%time
chain1.invoke({"topic": "熊"})
```

    CPU times: user 18 ms, sys: 1.27 ms, total: 19.3 ms
    Wall time: 692 ms
    




    AIMessage(content="为什么熊不穿鞋子？\n\n因为它们已经有熊脚了！")




```python
%%time
chain2.invoke({"topic": "熊"})
```

    CPU times: user 10.5 ms, sys: 166 µs, total: 10.7 ms
    Wall time: 579 ms
    




    AIMessage(content="在森林的怀抱中，\n雄伟的熊步行。")




```python
%%time
combined.invoke({"topic": "熊"})
```

    CPU times: user 32 ms, sys: 2.59 ms, total: 34.6 ms
    Wall time: 816 ms
    




    {'joke': AIMessage(content="好的，这是一个关于熊的笑话：\n\n为什么熊带着梯子去酒吧？\n\n因为它听说酒水是免费的！"),
     'poem': AIMessage(content="在荒野中漫游，\n雄伟的力量，大自然的王座。")}



### 批处理中的并行处理

并行处理可以与其他可运行对象结合使用。
让我们尝试将并行处理与批处理结合使用。


```python
%%time
chain1.batch([{"topic": "熊"}, {"topic": "猫"}])
```

    CPU times: user 17.3 ms, sys: 4.84 ms, total: 22.2 ms
    Wall time: 628 ms
    




    [AIMessage(content="为什么熊不穿鞋子？\n\n因为它们有熊脚！"),
     AIMessage(content="为什么猫不在野外玩扑克牌？\n\n因为有太多的猎豹！")]




```python
%%time
chain2.batch([{"topic": "熊"}, {"topic": "猫"}])
```

    CPU times: user 15.8 ms, sys: 3.83 ms, total: 19.7 ms
    Wall time: 718 ms
    




    [AIMessage(content='在野外，熊漫游，\n宏伟的古老家园的守护者。'),
     AIMessage(content='胡须优雅，眼神闪烁，\n猫儿在月光中起舞。')]




```python
%%time
combined.batch([{"topic": "熊"}, {"topic": "猫"}])
```

    CPU times: user 44.8 ms, sys: 3.17 ms, total: 48 ms
    Wall time: 721 ms
    




    [{'joke': AIMessage(content="好的，这是一个关于熊的笑话：\n\n为什么熊不穿鞋子？\n\n因为它们有熊脚！"),
      'poem': AIMessage(content="雄伟的熊漫游，\n大自然的力量，展现美丽。")},
     {'joke': AIMessage(content="为什么猫不在野外玩扑克牌？\n\n因为有太多的猎豹！"),
      'poem': AIMessage(content="胡须起舞，眼神闪烁，\n猫儿拥抱夜晚的柔和流动。")}]

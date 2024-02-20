# 添加消息历史记录（内存）

`RunnableWithMessageHistory` 允许我们为某些类型的链添加消息历史记录。它包装另一个 Runnable 并管理其聊天消息历史记录。

具体来说，它可用于以下任何输入类型的 Runnable：

* 一个 `BaseMessage` 序列
* 一个以序列 `BaseMessage` 为值的字典
* 一个以字符串或序列 `BaseMessage` 为最新消息的键和以历史消息为值的键的字典

并且返回以下任何输出类型之一：

* 一个可以作为 `AIMessage` 内容处理的字符串
* 一个 `BaseMessage` 序列
* 一个包含 `BaseMessage` 序列的字典

让我们通过一些示例来看看它是如何工作的。首先，我们构建一个 Runnable（在这里接受字典作为输入并返回消息作为输出）：


```python
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai.chat_models import ChatOpenAI

model = ChatOpenAI()
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "你是一个擅长{ability}的助手。回答不超过20个字",
        ),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{input}"),
    ]
)
runnable = prompt | model
```

为了管理消息历史记录，我们需要：
1. 这个 Runnable；
2. 一个可调用对象，返回一个 `BaseChatMessageHistory` 实例。

请查看 [memory integrations](https://integrations.langchain.com/memory) 页面，了解使用 Redis 和其他提供者实现聊天消息历史记录的方法。这里我们演示如何使用内存中的 `ChatMessageHistory`，以及使用 `RedisChatMessageHistory` 进行更持久的存储。

## 内存中的存储

下面是一个简单的示例，其中聊天历史记录保存在内存中，这里使用全局 Python 字典。

我们构建一个可调用的 `get_session_history`，它引用这个字典来返回一个 `ChatMessageHistory` 实例。可以通过在运行时向 `RunnableWithMessageHistory` 传递一个配置来指定可调用对象的参数。默认情况下，配置参数应该是一个单个字符串 `session_id`。可以通过 `history_factory_config` 关键字参数进行调整。

使用单参数默认值：


```python
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

store = {}


def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]


with_message_history = RunnableWithMessageHistory(
    runnable,
    get_session_history,
    input_messages_key="input",
    history_messages_key="history",
)
```

请注意，我们指定了 `input_messages_key`（要作为最新输入消息处理的键）和 `history_messages_key`（要添加历史消息的键）。

在调用这个新的 Runnable 时，我们通过配置参数指定相应的聊天历史记录：


```python
with_message_history.invoke(
    {"ability": "数学", "input": "余弦函数是什么意思？"},
    config={"configurable": {"session_id": "abc123"}},
)
```




    AIMessage(content='余弦函数是三角函数的一种，它计算的是直角三角形的邻边与斜边的比值。')




```python
# 记住
with_message_history.invoke(
    {"ability": "数学", "input": "什么？"},
    config={"configurable": {"session_id": "abc123"}},
)
```




    AIMessage(content='余弦是一种用于计算直角三角形中一条边的长度的数学函数。')




```python
# 新的 session_id --> 不记住。
with_message_history.invoke(
    {"ability": "数学", "input": "什么？"},
    config={"configurable": {"session_id": "def234"}},
)
```




    AIMessage(content='我可以帮助解决数学问题。你需要什么帮助？')



我们跟踪消息历史记录的配置参数可以通过将 `ConfigurableFieldSpec` 对象列表传递给 `history_factory_config` 参数来自定义。下面，我们使用了两个参数：`user_id` 和 `conversation_id`。


```python
from langchain_core.runnables import ConfigurableFieldSpec

store = {}


def get_session_history(user_id: str, conversation_id: str) -> BaseChatMessageHistory:
    if (user_id, conversation_id) not in store:
        store[(user_id, conversation_id)] = ChatMessageHistory()
    return store[(user_id, conversation_id)]


with_message_history = RunnableWithMessageHistory(
    runnable,
    get_session_history,
    input_messages_key="input",
    history_messages_key="history",
    history_factory_config=[
        ConfigurableFieldSpec(
            id="user_id",
            annotation=str,
            name="用户 ID",
            description="用户的唯一标识符。",
            default="",
            is_shared=True,
        ),
        ConfigurableFieldSpec(
            id="conversation_id",
            annotation=str,
            name="对话 ID",
            description="对话的唯一标识符。",
            default="",
            is_shared=True,
        ),
    ],
)
```


```python
with_message_history.invoke(
    {"ability": "数学", "input": "你好"},
    config={"configurable": {"user_id": "123", "conversation_id": "1"}},
)
```

### 具有不同签名的 Runnable 的示例

上述的 Runnable 接受字典作为输入并返回 BaseMessage。下面我们展示一些替代方案。

#### 输入为消息，输出为字典


```python
from langchain_core.messages import HumanMessage
from langchain_core.runnables import RunnableParallel

chain = RunnableParallel({"output_message": ChatOpenAI()})


def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]


with_message_history = RunnableWithMessageHistory(
    chain,
    get_session_history,
    output_messages_key="output_message",
)

with_message_history.invoke(
    [HumanMessage(content="Simone de Beauvoir 对自由意志的看法是什么")],
    config={"configurable": {"session_id": "baz"}},
)
```




    {'output_message': AIMessage(content="Simone de Beauvoir 相信自由意志的存在。她认为个体有能力做出选择并决定自己的行动，即使面对社会和文化的限制。她反对个体完全是环境的产物或被生物学或命运所决定的观点。相反，她强调个人责任的重要性，以及个体积极参与创造自己的生活和定义自己存在的需要。De Beauvoir 认为自由和行动能力来自于认识到自己的自由并积极行使它以追求个人和集体的解放。")}




```python
with_message_history.invoke(
    [HumanMessage(content="这与萨特的观点有何不同")],
    config={"configurable": {"session_id": "baz"}},
)
```




    {'output_message': AIMessage(content='Simone de Beauvoir 对自由意志的看法与她的同时代人兼伴侣让-保罗·萨特的观点非常相似。De Beauvoir 和萨特都是存在主义哲学家，强调个体自由的重要性和对决定论的拒绝。他们认为人类有能力超越自己的环境，创造自己的意义和价值。\n\n萨特在他的著名作品《存在与虚无》中认为，人类被注定是自由的，这意味着我们承担着在一个缺乏固有意义的世界中做出选择和定义自己的责任。与 De Beauvoir 一样，萨特认为个体有能力在外部和内部的限制下行使自由，做出选择。\n\n虽然他们的哲学著作中可能存在一些微妙的差异，但总体而言，De Beauvoir 和萨特都相信自由意志的存在以及个体行动在塑造自己的生活中的重要性。'})}



#### 输入为消息，输出为消息


```python
RunnableWithMessageHistory(
    ChatOpenAI(),
    get_session_history,
)
```

#### 字典，所有消息输入为单个键，消息输出


```python
from operator import itemgetter

RunnableWithMessageHistory(
    itemgetter("input_messages") | ChatOpenAI(),
    get_session_history,
    input_messages_key="input_messages",
)
```

## 持久化存储

在许多情况下，持久化对话历史记录是更好的选择。`RunnableWithMessageHistory` 对于 `get_session_history` 可调用对象如何检索其聊天消息历史记录是不可知的。请参阅 [这里](https://github.com/langchain-ai/langserve/blob/main/examples/chat_with_persistence_and_user/server.py) 以了解如何使用本地文件系统的示例。下面我们演示如何使用 Redis。请查看 [memory integrations](https://integrations.langchain.com/memory) 页面，了解使用其他提供者实现聊天消息历史记录的方法。

### 设置

如果尚未安装 Redis，请安装它：


```python
%pip install --upgrade --quiet redis
```

如果没有现有的 Redis 部署可供连接，启动一个本地 Redis Stack 服务器：
```bash
docker run -d -p 6379:6379 -p 8001:8001 redis/redis-stack:latest
```


```python
REDIS_URL = "redis://localhost:6379/0"
```

### [LangSmith](/docs/langsmith)

LangSmith 对于诸如消息历史记录注入之类的操作非常有用，否则很难理解链的各个部分的输入是什么。

请注意，LangSmith 不是必需的，但它很有帮助。
如果您想使用 LangSmith，在上面的链接中注册后，请确保取消下面的注释并设置您的环境变量以开始记录跟踪：


```python
# os.environ["LANGCHAIN_TRACING_V2"] = "true"
# os.environ["LANGCHAIN_API_KEY"] = getpass.getpass()
```

更新消息历史记录实现只需要定义一个新的可调用对象，这次返回一个 `RedisChatMessageHistory` 实例：


```python
from langchain_community.chat_message_histories import RedisChatMessageHistory


def get_message_history(session_id: str) -> RedisChatMessageHistory:
    return RedisChatMessageHistory(session_id, url=REDIS_URL)


with_message_history = RunnableWithMessageHistory(
    runnable,
    get_message_history,
    input_messages_key="input",
    history_messages_key="history",
)
```

我们可以像以前一样调用：


```python
with_message_history.invoke(
    {"ability": "数学", "input": "余弦函数是什么意思？"},
    config={"configurable": {"session_id": "foobar"}},
)
```




    AIMessage(content='余弦函数是三角函数的一种，它计算的是直角三角形的邻边与斜边的比值。')




```python
with_message_history.invoke(
    {"ability": "数学", "input": "它的反函数是什么"},
    config={"configurable": {"session_id": "foobar"}},
)
```




    AIMessage(content='余弦的反函数是反余弦函数，表示为 acos 或 cos^-1，它给出与给定余弦值对应的角度。')



:::tip

[Langsmith trace](https://smith.langchain.com/public/bd73e122-6ec1-48b2-82df-e6483dc9cb63/r)

:::

查看第二次调用的 Langsmith 跟踪，我们可以看到在构建提示时，已注入了一个名为 "history" 的变量，它是一个包含两个消息（我们的第一个输入和第一个输出）的列表。
=======
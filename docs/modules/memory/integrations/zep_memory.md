# Zep Memory

## 使用 Zep 的 REACT Agent 聊天消息记录 - 一种用于 LLM 应用程序的长期记忆存储。

本笔记本演示如何将 [Zep 长期记忆存储](https://docs.getzep.com/) 用作您的聊天机器人的记忆。

我们将演示以下内容：

1. 将对话历史添加到 Zep 记忆存储中。
2. 运行一个 Agent 并自动将消息添加到存储中。
3. 查看丰富的消息。
4. 在对话历史中进行矢量搜索。

### 关于 Zep 更多信息：

Zep 存储、摘要、嵌入、索引和丰富化对话式 AI 聊天历史，通过简单、低延迟的 API 进行访问。

主要功能：

- **快速！** Zep 的异步提取程序独立于聊天循环，确保用户体验流畅。
- **长期记忆持久性**，可以访问与摘要策略无关的历史消息。
- 基于可配置的消息窗口自动汇总存储消息。一系列摘要被存储，为将来的摘要策略提供灵活性。
- 对记忆和元数据的**混合搜索**，消息在创建时自动嵌入。
- **实体提取器**，自动从消息中提取命名实体，并将它们存储在消息的元数据中。
- 记忆和摘要的**自动令牌计数**，允许对提示组合进行更精细的控制。
- 提供 Python 和 JavaScript SDK。

Zep project: [https://github.com/getzep/zep](https://github.com/getzep/zep)
Docs: [https://docs.getzep.com/](https://docs.getzep.com/)



```python
from langchain.memory.chat_message_histories import ZepChatMessageHistory
from langchain.memory import ConversationBufferMemory
from langchain import OpenAI
from langchain.schema import HumanMessage, AIMessage
from langchain.tools import DuckDuckGoSearchRun
from langchain.agents import initialize_agent, AgentType
from uuid import uuid4


# Set this to your Zep server URL
ZEP_API_URL = "http://localhost:8000"

session_id = str(uuid4())  # This is a unique identifier for the user
```


```python
# Load your OpenAI key from a .env file
from dotenv import load_dotenv

load_dotenv()
```




    True



### Initialize the Zep Chat Message History Class and initialize the Agent



```python
ddg = DuckDuckGoSearchRun()
tools = [ddg]

# Set up Zep Chat History
zep_chat_history = ZepChatMessageHistory(
    session_id=session_id,
    url=ZEP_API_URL,
)

# Use a standard ConversationBufferMemory to encapsulate the Zep chat history
memory = ConversationBufferMemory(
    memory_key="chat_history", chat_memory=zep_chat_history
)

# Initialize the agent
llm = OpenAI(temperature=0)
agent_chain = initialize_agent(
    tools,
    llm,
    agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
    verbose=True,
    memory=memory,
)
```

### Add some history data



```python
# Preload some messages into the memory. The default message window is 12 messages. We want to push beyond this to demonstrate auto-summarization.
test_history = [
    {"role": "human", "content": "Who was Octavia Butler?"},
    {
        "role": "ai",
        "content": (
            "Octavia Estelle Butler (June 22, 1947 – February 24, 2006) was an American"
            " science fiction author."
        ),
    },
    {"role": "human", "content": "Which books of hers were made into movies?"},
    {
        "role": "ai",
        "content": (
            "The most well-known adaptation of Octavia Butler's work is the FX series"
            " Kindred, based on her novel of the same name."
        ),
    },
    {"role": "human", "content": "Who were her contemporaries?"},
    {
        "role": "ai",
        "content": (
            "Octavia Butler's contemporaries included Ursula K. Le Guin, Samuel R."
            " Delany, and Joanna Russ."
        ),
    },
    {"role": "human", "content": "What awards did she win?"},
    {
        "role": "ai",
        "content": (
            "Octavia Butler won the Hugo Award, the Nebula Award, and the MacArthur"
            " Fellowship."
        ),
    },
    {
        "role": "human",
        "content": "Which other women sci-fi writers might I want to read?",
    },
    {
        "role": "ai",
        "content": "You might want to read Ursula K. Le Guin or Joanna Russ.",
    },
    {
        "role": "human",
        "content": (
            "Write a short synopsis of Butler's book, Parable of the Sower. What is it"
            " about?"
        ),
    },
    {
        "role": "ai",
        "content": (
            "Parable of the Sower is a science fiction novel by Octavia Butler,"
            " published in 1993. It follows the story of Lauren Olamina, a young woman"
            " living in a dystopian future where society has collapsed due to"
            " environmental disasters, poverty, and violence."
        ),
    },
]

for msg in test_history:
    zep_chat_history.append(
        HumanMessage(content=msg["content"])
        if msg["role"] == "human"
        else AIMessage(content=msg["content"])
    )
```

### Run the agent

Doing so will automatically add the input and response to the Zep memory.



```python
agent_chain.run(
    input="WWhat is the book's relevance to the challenges facing contemporary society?"
)
```

    
    
    [1m> Entering new AgentExecutor chain...[0m
    [32;1m[1;3mThought: Do I need to use a tool? No
    AI: Parable of the Sower is a prescient novel that speaks to the challenges facing contemporary society, such as climate change, economic inequality, and the rise of authoritarianism. It is a cautionary tale that warns of the dangers of ignoring these issues and the importance of taking action to address them.[0m
    
    [1m> Finished chain.[0m
    




    'Parable of the Sower is a prescient novel that speaks to the challenges facing contemporary society, such as climate change, economic inequality, and the rise of authoritarianism. It is a cautionary tale that warns of the dangers of ignoring these issues and the importance of taking action to address them.'



### Inspect the Zep memory

Note the summary, and that the history has been enriched with token counts, UUIDs, and timestamps.

Summaries are biased towards the most recent messages.



```python
def print_messages(messages):
    for m in messages:
        print(m.to_dict())


print(zep_chat_history.zep_summary)
print("\n")
print_messages(zep_chat_history.zep_messages)
```

    The conversation is about Octavia Butler. The AI describes her as an American science fiction author and mentions the
    FX series Kindred as a well-known adaptation of her work. The human then asks about her contemporaries, and the AI lists 
    Ursula K. Le Guin, Samuel R. Delany, and Joanna Russ.
    
    
    {'role': 'human', 'content': 'What awards did she win?', 'uuid': '9fa75c3c-edae-41e3-b9bc-9fcf16b523c9', 'created_at': '2023-05-25T15:09:41.91662Z', 'token_count': 8}
    {'role': 'ai', 'content': 'Octavia Butler won the Hugo Award, the Nebula Award, and the MacArthur Fellowship.', 'uuid': 'def4636c-32cb-49ed-b671-32035a034712', 'created_at': '2023-05-25T15:09:41.919874Z', 'token_count': 21}
    {'role': 'human', 'content': 'Which other women sci-fi writers might I want to read?', 'uuid': '6e87bd4a-bc23-451e-ae36-05a140415270', 'created_at': '2023-05-25T15:09:41.923771Z', 'token_count': 14}
    {'role': 'ai', 'content': 'You might want to read Ursula K. Le Guin or Joanna Russ.', 'uuid': 'f65d8dde-9ee8-4983-9da6-ba789b7e8aa4', 'created_at': '2023-05-25T15:09:41.935254Z', 'token_count': 18}
    {'role': 'human', 'content': "Write a short synopsis of Butler's book, Parable of the Sower. What is it about?", 'uuid': '5678d056-7f05-4e70-b8e5-f85efa56db01', 'created_at': '2023-05-25T15:09:41.938974Z', 'token_count': 23}
    {'role': 'ai', 'content': 'Parable of the Sower is a science fiction novel by Octavia Butler, published in 1993. It follows the story of Lauren Olamina, a young woman living in a dystopian future where society has collapsed due to environmental disasters, poverty, and violence.', 'uuid': '50d64946-9239-4327-83e6-71dcbdd16198', 'created_at': '2023-05-25T15:09:41.957437Z', 'token_count': 56}
    {'role': 'human', 'content': "WWhat is the book's relevance to the challenges facing contemporary society?", 'uuid': 'a39cfc07-8858-480a-9026-fc47a8ef7001', 'created_at': '2023-05-25T15:09:50.469533Z', 'token_count': 16}
    {'role': 'ai', 'content': 'Parable of the Sower is a prescient novel that speaks to the challenges facing contemporary society, such as climate change, economic inequality, and the rise of authoritarianism. It is a cautionary tale that warns of the dangers of ignoring these issues and the importance of taking action to address them.', 'uuid': 'a4ecf0fe-fdd0-4aad-b72b-efde2e6830cc', 'created_at': '2023-05-25T15:09:50.473793Z', 'token_count': 62}
    

### Vector search over the Zep memory

Zep provides native vector search over historical conversation memory. Embedding happens automatically.



```python
search_results = zep_chat_history.search("who are some famous women sci-fi authors?")
for r in search_results:
    print(r.message, r.dist)
```

    {'uuid': '6e87bd4a-bc23-451e-ae36-05a140415270', 'created_at': '2023-05-25T15:09:41.923771Z', 'role': 'human', 'content': 'Which other women sci-fi writers might I want to read?', 'token_count': 14} 0.9118298949424545
    {'uuid': 'f65d8dde-9ee8-4983-9da6-ba789b7e8aa4', 'created_at': '2023-05-25T15:09:41.935254Z', 'role': 'ai', 'content': 'You might want to read Ursula K. Le Guin or Joanna Russ.', 'token_count': 18} 0.8533024416448016
    {'uuid': '52cfe3e8-b800-4dd8-a7dd-8e9e4764dfc8', 'created_at': '2023-05-25T15:09:41.913856Z', 'role': 'ai', 'content': "Octavia Butler's contemporaries included Ursula K. Le Guin, Samuel R. Delany, and Joanna Russ.", 'token_count': 27} 0.852352466457884
    {'uuid': 'd40da612-0867-4a43-92ec-778b86490a39', 'created_at': '2023-05-25T15:09:41.858543Z', 'role': 'human', 'content': 'Who was Octavia Butler?', 'token_count': 8} 0.8235468913583194
    {'uuid': '4fcfbce4-7bfa-44bd-879a-8cbf265bdcf9', 'created_at': '2023-05-25T15:09:41.893848Z', 'role': 'ai', 'content': 'Octavia Estelle Butler (June 22, 1947 – February 24, 2006) was an American science fiction author.', 'token_count': 31} 0.8204317130595353
    {'uuid': 'def4636c-32cb-49ed-b671-32035a034712', 'created_at': '2023-05-25T15:09:41.919874Z', 'role': 'ai', 'content': 'Octavia Butler won the Hugo Award, the Nebula Award, and the MacArthur Fellowship.', 'token_count': 21} 0.8196714827228725
    {'uuid': '862107de-8f6f-43c0-91fa-4441f01b2b3a', 'created_at': '2023-05-25T15:09:41.898149Z', 'role': 'human', 'content': 'Which books of hers were made into movies?', 'token_count': 11} 0.7954322970428519
    {'uuid': '97164506-90fe-4c71-9539-69ebcd1d90a2', 'created_at': '2023-05-25T15:09:41.90887Z', 'role': 'human', 'content': 'Who were her contemporaries?', 'token_count': 8} 0.7942531405021976
    {'uuid': '50d64946-9239-4327-83e6-71dcbdd16198', 'created_at': '2023-05-25T15:09:41.957437Z', 'role': 'ai', 'content': 'Parable of the Sower is a science fiction novel by Octavia Butler, published in 1993. It follows the story of Lauren Olamina, a young woman living in a dystopian future where society has collapsed due to environmental disasters, poverty, and violence.', 'token_count': 56} 0.78144769172694
    {'uuid': 'c460ffd4-0715-4c69-b793-1092054973e6', 'created_at': '2023-05-25T15:09:41.903082Z', 'role': 'ai', 'content': "The most well-known adaptation of Octavia Butler's work is the FX series Kindred, based on her novel of the same name.", 'token_count': 29} 0.7811962820699464
    

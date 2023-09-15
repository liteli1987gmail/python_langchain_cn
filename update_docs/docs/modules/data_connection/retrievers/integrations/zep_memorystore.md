# Zep
## Retriever Example for [Zep](https://docs.getzep.com/) - A long-term memory store for LLM applications.

### More on Zep:

Zep stores, summarizes, embeds, indexes, and enriches conversational AI chat histories, and exposes them via simple, low-latency APIs.

Key Features:

- **Fast!** Zep’s async extractors operate independently of the your chat loop, ensuring a snappy user experience.
- **Long-term memory persistence**, with access to historical messages irrespective of your summarization strategy.
- **Auto-summarization** of memory messages based on a configurable message window. A series of summaries are stored, providing flexibility for future summarization strategies.
- **Hybrid search** over memories and metadata, with messages automatically embedded on creation.
- **Entity Extractor** that automatically extracts named entities from messages and stores them in the message metadata.
- **Auto-token counting** of memories and summaries, allowing finer-grained control over prompt assembly.
- Python and JavaScript SDKs.

Zep project: [https://github.com/getzep/zep](https://github.com/getzep/zep)
Docs: [https://docs.getzep.com/](https://docs.getzep.com/)


## Retriever Example

This notebook demonstrates how to search historical chat message histories using the [Zep Long-term Memory Store](https://getzep.github.io/).

We'll demonstrate:

1. Adding conversation history to the Zep memory store.
2. Vector search over the conversation history.




```python
from langchain.memory.chat_message_histories import ZepChatMessageHistory
from langchain.schema import HumanMessage, AIMessage
from uuid import uuid4

# Set this to your Zep server URL
ZEP_API_URL = "http://localhost:8000"
```

### Initialize the Zep Chat Message History Class and add a chat message history to the memory store

**NOTE:** Unlike other Retrievers, the content returned by the Zep Retriever is session/user specific. A `session_id` is required when instantiating the Retriever.


```python
session_id = str(uuid4())  # This is a unique identifier for the user/session

# Set up Zep Chat History. We'll use this to add chat histories to the memory store
zep_chat_history = ZepChatMessageHistory(
    session_id=session_id,
    url=ZEP_API_URL,
)
```


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

### Use the Zep Retriever to vector search over the Zep memory

Zep provides native vector search over historical conversation memory. Embedding happens automatically.

NOTE: Embedding of messages occurs asynchronously, so the first query may not return results. Subsequent queries will return results as the embeddings are generated.


```python
from langchain.retrievers import ZepRetriever

zep_retriever = ZepRetriever(
    session_id=session_id,  # Ensure that you provide the session_id when instantiating the Retriever
    url=ZEP_API_URL,
    top_k=5,
)

await zep_retriever.aget_relevant_documents("Who wrote Parable of the Sower?")
```




    [Document(page_content='Who was Octavia Butler?', metadata={'score': 0.7759001673780126, 'uuid': '3a82a02f-056e-4c6a-b960-67ebdf3b2b93', 'created_at': '2023-05-25T15:03:30.2041Z', 'role': 'human', 'token_count': 8}),
     Document(page_content="Octavia Butler's contemporaries included Ursula K. Le Guin, Samuel R. Delany, and Joanna Russ.", metadata={'score': 0.7602262941130749, 'uuid': 'a2fc9c21-0897-46c8-bef7-6f5c0f71b04a', 'created_at': '2023-05-25T15:03:30.248065Z', 'role': 'ai', 'token_count': 27}),
     Document(page_content='Who were her contemporaries?', metadata={'score': 0.757553366415519, 'uuid': '41f9c41a-a205-41e1-b48b-a0a4cd943fc8', 'created_at': '2023-05-25T15:03:30.243995Z', 'role': 'human', 'token_count': 8}),
     Document(page_content='Octavia Estelle Butler (June 22, 1947 – February 24, 2006) was an American science fiction author.', metadata={'score': 0.7546211059317948, 'uuid': '34678311-0098-4f1a-8fd4-5615ac692deb', 'created_at': '2023-05-25T15:03:30.231427Z', 'role': 'ai', 'token_count': 31}),
     Document(page_content='Which books of hers were made into movies?', metadata={'score': 0.7496714959247069, 'uuid': '18046c3a-9666-4d3e-b4f0-43d1394732b7', 'created_at': '2023-05-25T15:03:30.236837Z', 'role': 'human', 'token_count': 11})]



We can also use the Zep sync API to retrieve results:


```python
zep_retriever.get_relevant_documents("Who wrote Parable of the Sower?")
```




    [Document(page_content='Parable of the Sower is a science fiction novel by Octavia Butler, published in 1993. It follows the story of Lauren Olamina, a young woman living in a dystopian future where society has collapsed due to environmental disasters, poverty, and violence.', metadata={'score': 0.8897321402776546, 'uuid': '1c09603a-52c1-40d7-9d69-29f26256029c', 'created_at': '2023-05-25T15:03:30.268257Z', 'role': 'ai', 'token_count': 56}),
     Document(page_content="Write a short synopsis of Butler's book, Parable of the Sower. What is it about?", metadata={'score': 0.8857628682610436, 'uuid': 'f6706e8c-6c91-452f-8c1b-9559fd924657', 'created_at': '2023-05-25T15:03:30.265302Z', 'role': 'human', 'token_count': 23}),
     Document(page_content='Who was Octavia Butler?', metadata={'score': 0.7759670375149477, 'uuid': '3a82a02f-056e-4c6a-b960-67ebdf3b2b93', 'created_at': '2023-05-25T15:03:30.2041Z', 'role': 'human', 'token_count': 8}),
     Document(page_content="Octavia Butler's contemporaries included Ursula K. Le Guin, Samuel R. Delany, and Joanna Russ.", metadata={'score': 0.7602854653476563, 'uuid': 'a2fc9c21-0897-46c8-bef7-6f5c0f71b04a', 'created_at': '2023-05-25T15:03:30.248065Z', 'role': 'ai', 'token_count': 27}),
     Document(page_content='You might want to read Ursula K. Le Guin or Joanna Russ.', metadata={'score': 0.7595293992240313, 'uuid': 'f22f2498-6118-4c74-8718-aa89ccd7e3d6', 'created_at': '2023-05-25T15:03:30.261198Z', 'role': 'ai', 'token_count': 18})]




```python

```

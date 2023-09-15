# AutoGPT

Implementation of https://github.com/Significant-Gravitas/Auto-GPT but with LangChain primitives (LLMs, PromptTemplates, VectorStores, Embeddings, Tools)

## Set up tools

We'll set up an AutoGPT with a search tool, and write-file tool, and a read-file tool


```python
from langchain.utilities import SerpAPIWrapper
from langchain.agents import Tool
from langchain.tools.file_management.write import WriteFileTool
from langchain.tools.file_management.read import ReadFileTool

search = SerpAPIWrapper()
tools = [
    Tool(
        name="search",
        func=search.run,
        description="useful for when you need to answer questions about current events. You should ask targeted questions",
    ),
    WriteFileTool(),
    ReadFileTool(),
]
```

## Set up memory

The memory here is used for the agents intermediate steps


```python
from langchain.vectorstores import FAISS
from langchain.docstore import InMemoryDocstore
from langchain.embeddings import OpenAIEmbeddings
```


```python
# Define your embedding model
embeddings_model = OpenAIEmbeddings()
# Initialize the vectorstore as empty
import faiss

embedding_size = 1536
index = faiss.IndexFlatL2(embedding_size)
vectorstore = FAISS(embeddings_model.embed_query, index, InMemoryDocstore({}), {})
```

## Setup model and AutoGPT

Initialize everything! We will use ChatOpenAI model


```python
from langchain.experimental import AutoGPT
from langchain.chat_models import ChatOpenAI
```


```python
agent = AutoGPT.from_llm_and_tools(
    ai_name="Tom",
    ai_role="Assistant",
    tools=tools,
    llm=ChatOpenAI(temperature=0),
    memory=vectorstore.as_retriever(),
)
# Set verbose to be true
agent.chain.verbose = True
```

## Run an example

Here we will make it write a weather report for SF


```python
agent.run(["write a weather report for SF today"])
```

## Chat History Memory

In addition to the memory that holds the agent immediate steps, we also have a chat history memory. By default, the agent will use 'ChatMessageHistory' and it can be changed. This is useful when you want to use a different type of memory for example 'FileChatHistoryMemory'


```python
from langchain.memory.chat_message_histories import FileChatMessageHistory

agent = AutoGPT.from_llm_and_tools(
    ai_name="Tom",
    ai_role="Assistant",
    tools=tools,
    llm=ChatOpenAI(temperature=0),
    memory=vectorstore.as_retriever(),
    chat_history_memory=FileChatMessageHistory("chat_history.txt"),
)
```



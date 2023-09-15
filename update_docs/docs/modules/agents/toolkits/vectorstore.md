# Vectorstore Agent

This notebook showcases an agent designed to retrieve information from one or more vectorstores, either with or without sources.

## Create the Vectorstores


```python
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.text_splitter import CharacterTextSplitter
from langchain import OpenAI, VectorDBQA

llm = OpenAI(temperature=0)
```


```python
from langchain.document_loaders import TextLoader

loader = TextLoader("../../../state_of_the_union.txt")
documents = loader.load()
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
texts = text_splitter.split_documents(documents)

embeddings = OpenAIEmbeddings()
state_of_union_store = Chroma.from_documents(
    texts, embeddings, collection_name="state-of-union"
)
```

    Running Chroma using direct local API.
    Using DuckDB in-memory for database. Data will be transient.
    


```python
from langchain.document_loaders import WebBaseLoader

loader = WebBaseLoader("https://beta.ruff.rs/docs/faq/")
docs = loader.load()
ruff_texts = text_splitter.split_documents(docs)
ruff_store = Chroma.from_documents(ruff_texts, embeddings, collection_name="ruff")
```

    Running Chroma using direct local API.
    Using DuckDB in-memory for database. Data will be transient.
    

## Initialize Toolkit and Agent

First, we'll create an agent with a single vectorstore.


```python
from langchain.agents.agent_toolkits import (
    create_vectorstore_agent,
    VectorStoreToolkit,
    VectorStoreInfo,
)

vectorstore_info = VectorStoreInfo(
    name="state_of_union_address",
    description="the most recent state of the Union adress",
    vectorstore=state_of_union_store,
)
toolkit = VectorStoreToolkit(vectorstore_info=vectorstore_info)
agent_executor = create_vectorstore_agent(llm=llm, toolkit=toolkit, verbose=True)
```

## Examples


```python
agent_executor.run(
    "What did biden say about ketanji brown jackson in the state of the union address?"
)
```

    
    
    [1m> Entering new AgentExecutor chain...[0m
    [32;1m[1;3m I need to find the answer in the state of the union address
    Action: state_of_union_address
    Action Input: What did biden say about ketanji brown jackson[0m
    Observation: [36;1m[1;3m Biden said that Ketanji Brown Jackson is one of the nation's top legal minds and that she will continue Justice Breyer's legacy of excellence.[0m
    Thought:[32;1m[1;3m I now know the final answer
    Final Answer: Biden said that Ketanji Brown Jackson is one of the nation's top legal minds and that she will continue Justice Breyer's legacy of excellence.[0m
    
    [1m> Finished chain.[0m
    




    "Biden said that Ketanji Brown Jackson is one of the nation's top legal minds and that she will continue Justice Breyer's legacy of excellence."




```python
agent_executor.run(
    "What did biden say about ketanji brown jackson in the state of the union address? List the source."
)
```

    
    
    [1m> Entering new AgentExecutor chain...[0m
    [32;1m[1;3m I need to use the state_of_union_address_with_sources tool to answer this question.
    Action: state_of_union_address_with_sources
    Action Input: What did biden say about ketanji brown jackson[0m
    Observation: [33;1m[1;3m{"answer": " Biden said that he nominated Circuit Court of Appeals Judge Ketanji Brown Jackson to the United States Supreme Court, and that she is one of the nation's top legal minds who will continue Justice Breyer's legacy of excellence.\n", "sources": "../../state_of_the_union.txt"}[0m
    Thought:[32;1m[1;3m I now know the final answer
    Final Answer: Biden said that he nominated Circuit Court of Appeals Judge Ketanji Brown Jackson to the United States Supreme Court, and that she is one of the nation's top legal minds who will continue Justice Breyer's legacy of excellence. Sources: ../../state_of_the_union.txt[0m
    
    [1m> Finished chain.[0m
    




    "Biden said that he nominated Circuit Court of Appeals Judge Ketanji Brown Jackson to the United States Supreme Court, and that she is one of the nation's top legal minds who will continue Justice Breyer's legacy of excellence. Sources: ../../state_of_the_union.txt"



## Multiple Vectorstores
We can also easily use this initialize an agent with multiple vectorstores and use the agent to route between them. To do this. This agent is optimized for routing, so it is a different toolkit and initializer.


```python
from langchain.agents.agent_toolkits import (
    create_vectorstore_router_agent,
    VectorStoreRouterToolkit,
    VectorStoreInfo,
)
```


```python
ruff_vectorstore_info = VectorStoreInfo(
    name="ruff",
    description="Information about the Ruff python linting library",
    vectorstore=ruff_store,
)
router_toolkit = VectorStoreRouterToolkit(
    vectorstores=[vectorstore_info, ruff_vectorstore_info], llm=llm
)
agent_executor = create_vectorstore_router_agent(
    llm=llm, toolkit=router_toolkit, verbose=True
)
```

## Examples


```python
agent_executor.run(
    "What did biden say about ketanji brown jackson in the state of the union address?"
)
```

    
    
    [1m> Entering new AgentExecutor chain...[0m
    [32;1m[1;3m I need to use the state_of_union_address tool to answer this question.
    Action: state_of_union_address
    Action Input: What did biden say about ketanji brown jackson[0m
    Observation: [36;1m[1;3m Biden said that Ketanji Brown Jackson is one of the nation's top legal minds and that she will continue Justice Breyer's legacy of excellence.[0m
    Thought:[32;1m[1;3m I now know the final answer
    Final Answer: Biden said that Ketanji Brown Jackson is one of the nation's top legal minds and that she will continue Justice Breyer's legacy of excellence.[0m
    
    [1m> Finished chain.[0m
    




    "Biden said that Ketanji Brown Jackson is one of the nation's top legal minds and that she will continue Justice Breyer's legacy of excellence."




```python
agent_executor.run("What tool does ruff use to run over Jupyter Notebooks?")
```

    
    
    [1m> Entering new AgentExecutor chain...[0m
    [32;1m[1;3m I need to find out what tool ruff uses to run over Jupyter Notebooks
    Action: ruff
    Action Input: What tool does ruff use to run over Jupyter Notebooks?[0m
    Observation: [33;1m[1;3m Ruff is integrated into nbQA, a tool for running linters and code formatters over Jupyter Notebooks. After installing ruff and nbqa, you can run Ruff over a notebook like so: > nbqa ruff Untitled.html[0m
    Thought:[32;1m[1;3m I now know the final answer
    Final Answer: Ruff is integrated into nbQA, a tool for running linters and code formatters over Jupyter Notebooks. After installing ruff and nbqa, you can run Ruff over a notebook like so: > nbqa ruff Untitled.html[0m
    
    [1m> Finished chain.[0m
    




    'Ruff is integrated into nbQA, a tool for running linters and code formatters over Jupyter Notebooks. After installing ruff and nbqa, you can run Ruff over a notebook like so: > nbqa ruff Untitled.html'




```python
agent_executor.run(
    "What tool does ruff use to run over Jupyter Notebooks? Did the president mention that tool in the state of the union?"
)
```

    
    
    [1m> Entering new AgentExecutor chain...[0m
    [32;1m[1;3m I need to find out what tool ruff uses and if the president mentioned it in the state of the union.
    Action: ruff
    Action Input: What tool does ruff use to run over Jupyter Notebooks?[0m
    Observation: [33;1m[1;3m Ruff is integrated into nbQA, a tool for running linters and code formatters over Jupyter Notebooks. After installing ruff and nbqa, you can run Ruff over a notebook like so: > nbqa ruff Untitled.html[0m
    Thought:[32;1m[1;3m I need to find out if the president mentioned nbQA in the state of the union.
    Action: state_of_union_address
    Action Input: Did the president mention nbQA in the state of the union?[0m
    Observation: [36;1m[1;3m No, the president did not mention nbQA in the state of the union.[0m
    Thought:[32;1m[1;3m I now know the final answer.
    Final Answer: No, the president did not mention nbQA in the state of the union.[0m
    
    [1m> Finished chain.[0m
    




    'No, the president did not mention nbQA in the state of the union.'




```python

```

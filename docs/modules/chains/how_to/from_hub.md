# Loading from LangChainHub

This notebook covers how to load chains from [LangChainHub](https://github.com/hwchase17/langchain-hub).


```python
from langchain.chains import load_chain

chain = load_chain("lc://chains/llm-math/chain.json")
```


```python
chain.run("whats 2 raised to .12")
```

    
    
    [1m> Entering new LLMMathChain chain...[0m
    whats 2 raised to .12[32;1m[1;3m
    Answer: 1.0791812460476249[0m
    [1m> Finished chain.[0m
    




    'Answer: 1.0791812460476249'



Sometimes chains will require extra arguments that were not serialized with the chain. For example, a chain that does question answering over a vector database will require a vector database.


```python
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.text_splitter import CharacterTextSplitter
from langchain import OpenAI, VectorDBQA
```


```python
from langchain.document_loaders import TextLoader

loader = TextLoader("../../state_of_the_union.txt")
documents = loader.load()
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
texts = text_splitter.split_documents(documents)

embeddings = OpenAIEmbeddings()
vectorstore = Chroma.from_documents(texts, embeddings)
```

    Running Chroma using direct local API.
    Using DuckDB in-memory for database. Data will be transient.
    


```python
chain = load_chain("lc://chains/vector-db-qa/stuff/chain.json", vectorstore=vectorstore)
```


```python
query = "What did the president say about Ketanji Brown Jackson"
chain.run(query)
```




    " The president said that Ketanji Brown Jackson is a Circuit Court of Appeals Judge, one of the nation's top legal minds, a former top litigator in private practice, a former federal public defender, has received a broad range of support from the Fraternal Order of Police to former judges appointed by Democrats and Republicans, and will continue Justice Breyer's legacy of excellence."




```python

```

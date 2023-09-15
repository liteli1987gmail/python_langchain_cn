# DocArrayInMemorySearch

>[DocArrayInMemorySearch](https://docs.docarray.org/user_guide/storing/index_in_memory/) is a document index provided by [Docarray](https://docs.docarray.org/) that stores documents in memory. It is a great starting point for small datasets, where you may not want to launch a database server.

This notebook shows how to use functionality related to the `DocArrayInMemorySearch`.

## Setup

Uncomment the below cells to install docarray and get/set your OpenAI api key if you haven't already done so.


```python
# !pip install "docarray"
```


```python
# Get an OpenAI token: https://platform.openai.com/account/api-keys

# import os
# from getpass import getpass

# OPENAI_API_KEY = getpass()

# os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
```

## Using DocArrayInMemorySearch


```python
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import DocArrayInMemorySearch
from langchain.document_loaders import TextLoader
```


```python
documents = TextLoader("../../../state_of_the_union.txt").load()
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
docs = text_splitter.split_documents(documents)

embeddings = OpenAIEmbeddings()

db = DocArrayInMemorySearch.from_documents(docs, embeddings)
```

### Similarity search


```python
query = "What did the president say about Ketanji Brown Jackson"
docs = db.similarity_search(query)
```


```python
print(docs[0].page_content)
```

    Tonight. I call on the Senate to: Pass the Freedom to Vote Act. Pass the John Lewis Voting Rights Act. And while you’re at it, pass the Disclose Act so Americans can know who is funding our elections. 
    
    Tonight, I’d like to honor someone who has dedicated his life to serve this country: Justice Stephen Breyer—an Army veteran, Constitutional scholar, and retiring Justice of the United States Supreme Court. Justice Breyer, thank you for your service. 
    
    One of the most serious constitutional responsibilities a President has is nominating someone to serve on the United States Supreme Court. 
    
    And I did that 4 days ago, when I nominated Circuit Court of Appeals Judge Ketanji Brown Jackson. One of our nation’s top legal minds, who will continue Justice Breyer’s legacy of excellence.
    

### Similarity search with score

The returned distance score is cosine distance. Therefore, a lower score is better.


```python
docs = db.similarity_search_with_score(query)
```


```python
docs[0]
```




    (Document(page_content='Tonight. I call on the Senate to: Pass the Freedom to Vote Act. Pass the John Lewis Voting Rights Act. And while you’re at it, pass the Disclose Act so Americans can know who is funding our elections. \n\nTonight, I’d like to honor someone who has dedicated his life to serve this country: Justice Stephen Breyer—an Army veteran, Constitutional scholar, and retiring Justice of the United States Supreme Court. Justice Breyer, thank you for your service. \n\nOne of the most serious constitutional responsibilities a President has is nominating someone to serve on the United States Supreme Court. \n\nAnd I did that 4 days ago, when I nominated Circuit Court of Appeals Judge Ketanji Brown Jackson. One of our nation’s top legal minds, who will continue Justice Breyer’s legacy of excellence.', metadata={}),
     0.8154190158347903)




```python

```

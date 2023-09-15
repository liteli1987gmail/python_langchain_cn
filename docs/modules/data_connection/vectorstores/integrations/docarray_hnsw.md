# DocArrayHnswSearch

>[DocArrayHnswSearch](https://docs.docarray.org/user_guide/storing/index_hnswlib/) is a lightweight Document Index implementation provided by [Docarray](https://docs.docarray.org/) that runs fully locally and is best suited for small- to medium-sized datasets. It stores vectors on disk in [hnswlib](https://github.com/nmslib/hnswlib), and stores all other data in [SQLite](https://www.sqlite.org/index.html).

This notebook shows how to use functionality related to the `DocArrayHnswSearch`.

## Setup

Uncomment the below cells to install docarray and get/set your OpenAI api key if you haven't already done so.


```python
# !pip install "docarray[hnswlib]"
```


```python
# Get an OpenAI token: https://platform.openai.com/account/api-keys

# import os
# from getpass import getpass

# OPENAI_API_KEY = getpass()

# os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
```

## Using DocArrayHnswSearch


```python
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import DocArrayHnswSearch
from langchain.document_loaders import TextLoader
```


```python
documents = TextLoader("../../../state_of_the_union.txt").load()
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
docs = text_splitter.split_documents(documents)

embeddings = OpenAIEmbeddings()

db = DocArrayHnswSearch.from_documents(
    docs, embeddings, work_dir="hnswlib_store/", n_dim=1536
)
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
     0.36962226)




```python
import shutil

# delete the dir
shutil.rmtree("hnswlib_store")
```

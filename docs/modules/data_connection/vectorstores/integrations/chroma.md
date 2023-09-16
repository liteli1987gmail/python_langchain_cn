# Chroma

[Chroma](https://docs.trychroma.com/getting-started)是一个用于构建具有嵌入向量的AI应用程序的数据库。

这个笔记本展示了如何使用与`Chroma`向量数据库相关的功能。

```python
!pip install chromadb
```


```python
from getpass import getpass

OPENAI_API_KEY = getpass()
```


········


```python
import os

os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
```


```python
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.document_loaders import TextLoader
```


```python
loader = TextLoader("../../../state_of_the_union.txt")
documents = loader.load()
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
docs = text_splitter.split_documents(documents)

embeddings = OpenAIEmbeddings()
```


```python
db = Chroma.from_documents(docs, embeddings)
query = "What did the president say about Ketanji Brown Jackson"
docs = db.similarity_search(query)
```


Using embedded DuckDB without persistence: data will be transient


```python
print(docs[0].page_content)
```


Tonight. I call on the Senate to: Pass the Freedom to Vote Act. Pass the John Lewis Voting Rights Act. And while you're at it, pass the Disclose Act so Americans can know who is funding our elections. 

Tonight, I'd like to honor someone who has dedicated his life to serve this country: Justice Stephen Breyer—an Army veteran, Constitutional scholar, and retiring Justice of the United States Supreme Court. Justice Breyer, thank you for your service. 

One of the most serious constitutional responsibilities a President has is nominating someone to serve on the United States Supreme Court. 

And I did that 4 days ago, when I nominated Circuit Court of Appeals Judge Ketanji Brown Jackson. One of our nation's top legal minds, who will continue Justice Breyer's legacy of excellence.


## Similarity search with score

The returned distance score is cosine distance. Therefore, a lower score is better.


```python
docs = db.similarity_search_with_score(query)
```


```python
docs[0]
```




(Document(page_content='Tonight. I call on the Senate to: Pass the Freedom to Vote Act. Pass the John Lewis Voting Rights Act. And while you're at it, pass the Disclose Act so Americans can know who is funding our elections. 

Tonight, I'd like to honor someone who has dedicated his life to serve this country: Justice Stephen Breyer—an Army veteran, Constitutional scholar, and retiring Justice of the United States Supreme Court. Justice Breyer, thank you for your service. 

One of the most serious constitutional responsibilities a President has is nominating someone to serve on the United States Supreme Court. 

And I did that 4 days ago, when I nominated Circuit Court of Appeals Judge Ketanji Brown Jackson. One of our nation's top legal minds, who will continue Justice Breyer's legacy of excellence.', metadata={'source': '../../../state_of_the_union.txt'}),
 0.3949805498123169)



## Persistance

The below steps cover how to persist a ChromaDB instance

### Initialize PeristedChromaDB
Create embeddings for each chunk and insert into the Chroma vector database. The persist_directory argument tells ChromaDB where to store the database when it's persisted.


```python
# Embed and store the texts
# Supplying a persist_directory will store the embeddings on disk
persist_directory = "db"

embedding = OpenAIEmbeddings()
vectordb = Chroma.from_documents(
    documents=docs, embedding=embedding, persist_directory=persist_directory
)
```


Running Chroma using direct local API.
No existing DB found in db, skipping load
No existing DB found in db, skipping load


### Persist the Database
We should call persist() to ensure the embeddings are written to disk.


```python
vectordb.persist()
vectordb = None
```


Persisting DB to disk, putting it in the save folder db
PersistentDuckDB del, about to run persist
Persisting DB to disk, putting it in the save folder db


### Load the Database from disk, and create the chain
Be sure to pass the same persist_directory and embedding_function as you did when you instantiated the database. Initialize the chain we will use for question answering.


```python
# Now we can load the persisted database from disk, and use it as normal.
vectordb = Chroma(persist_directory=persist_directory, embedding_function=embedding)
```


Running Chroma using direct local API.
loaded in 4 embeddings
loaded in 1 collections


## Retriever options

This section goes over different options for how to use Chroma as a retriever.

### MMR

In addition to using similarity search in the retriever object, you can also use `mmr`.


```python
retriever = db.as_retriever(search_type="mmr")
```


```python
retriever.get_relevant_documents(query)[0]
```




(Document(page_content='Tonight. I call on the Senate to: Pass the Freedom to Vote Act. Pass the John Lewis Voting Rights Act. And while you're at it, pass the Disclose Act so Americans can know who is funding our elections. 

Tonight, I'd like to honor someone who has dedicated his life to serve this country: Justice Stephen Breyer—an Army veteran, Constitutional scholar, and retiring Justice of the United States Supreme Court. Justice Breyer, thank you for your service. 

One of the most serious constitutional responsibilities a President has is nominating someone to serve on the United States Supreme Court. 

And I did that 4 days ago, when I nominated Circuit Court of Appeals Judge Ketanji Brown Jackson. One of our nation's top legal minds, who will continue Justice Breyer's legacy of excellence.', metadata={'source': '../../../state_of_the_union.txt'})




## Updating a Document

The `update_document` function allows you to modify the content of a document in the Chroma instance after it has been added. Let's see an example of how to use this function.


```python
# Import Document class
from langchain.docstore.document import Document

# Initial document content and id
initial_content = "This is an initial document content"
document_id = "doc1"

# Create an instance of Document with initial content and metadata
original_doc = Document(page_content=initial_content, metadata={"page": "0"})

# Initialize a Chroma instance with the original document
new_db = Chroma.from_documents(
    collection_name="test_collection",
    documents=[original_doc],
    embedding=OpenAIEmbeddings(),  # using the same embeddings as before
    ids=[document_id],
)
```


At this point, we have a new Chroma instance with a single document "This is an initial document content" with id "doc1". Now, let's update the content of the document.


```python
# Updated document content
updated_content = "This is the updated document content"

# Create a new Document instance with the updated content
updated_doc = Document(page_content=updated_content, metadata={"page": "1"})

# Update the document in the Chroma instance by passing the document id and the updated document
new_db.update_document(document_id=document_id, document=updated_doc)

# Now, let's retrieve the updated document using similarity search
output = new_db.similarity_search(updated_content, k=1)

# Print the content of the retrieved document
print(output[0].page_content, output[0].metadata)
```


    This is the updated document content {'page': '1'}
    

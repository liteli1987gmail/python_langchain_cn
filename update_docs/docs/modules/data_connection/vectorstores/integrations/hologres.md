# Hologres

>[Hologres](https://www.alibabacloud.com/help/en/hologres/latest/introduction) is a unified real-time data warehousing service developed by Alibaba Cloud. You can use Hologres to write, update, process, and analyze large amounts of data in real time. 
>Hologres supports standard SQL syntax, is compatible with PostgreSQL, and supports most PostgreSQL functions. Hologres supports online analytical processing (OLAP) and ad hoc analysis for up to petabytes of data, and provides high-concurrency and low-latency online data services. 

>Hologres provides **vector database** functionality by adopting [Proxima](https://www.alibabacloud.com/help/en/hologres/latest/vector-processing).
>Proxima is a high-performance software library developed by Alibaba DAMO Academy. It allows you to search for the nearest neighbors of vectors. Proxima provides higher stability and performance than similar open source software such as Faiss. Proxima allows you to search for similar text or image embeddings with high throughput and low latency. Hologres is deeply integrated with Proxima to provide a high-performance vector search service.

This notebook shows how to use functionality related to the `Hologres Proxima` vector database.
Click [here](https://www.alibabacloud.com/zh/product/hologres) to fast deploy a Hologres cloud instance.


```python
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Hologres
```

Split documents and get embeddings by call OpenAI API


```python
from langchain.document_loaders import TextLoader

loader = TextLoader("../../../state_of_the_union.txt")
documents = loader.load()
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
docs = text_splitter.split_documents(documents)

embeddings = OpenAIEmbeddings()
```

Connect to Hologres by setting related ENVIRONMENTS.
```
export PG_HOST={host}
export PG_PORT={port} # Optional, default is 80
export PG_DATABASE={db_name} # Optional, default is postgres
export PG_USER={username}
export PG_PASSWORD={password}
```

Then store your embeddings and documents into Hologres


```python
import os

connection_string = Hologres.connection_string_from_db_params(
    host=os.environ.get("PGHOST", "localhost"),
    port=int(os.environ.get("PGPORT", "80")),
    database=os.environ.get("PGDATABASE", "postgres"),
    user=os.environ.get("PGUSER", "postgres"),
    password=os.environ.get("PGPASSWORD", "postgres"),
)

vector_db = Hologres.from_documents(
    docs,
    embeddings,
    connection_string=connection_string,
    table_name="langchain_example_embeddings",
)
```

Query and retrieve data


```python
query = "What did the president say about Ketanji Brown Jackson"
docs = vector_db.similarity_search(query)
```


```python
print(docs[0].page_content)
```

    Tonight. I call on the Senate to: Pass the Freedom to Vote Act. Pass the John Lewis Voting Rights Act. And while you’re at it, pass the Disclose Act so Americans can know who is funding our elections. 
    
    Tonight, I’d like to honor someone who has dedicated his life to serve this country: Justice Stephen Breyer—an Army veteran, Constitutional scholar, and retiring Justice of the United States Supreme Court. Justice Breyer, thank you for your service. 
    
    One of the most serious constitutional responsibilities a President has is nominating someone to serve on the United States Supreme Court. 
    
    And I did that 4 days ago, when I nominated Circuit Court of Appeals Judge Ketanji Brown Jackson. One of our nation’s top legal minds, who will continue Justice Breyer’s legacy of excellence.
    

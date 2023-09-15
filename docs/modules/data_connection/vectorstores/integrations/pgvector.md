# PGVector

>[PGVector](https://github.com/pgvector/pgvector) is an open-source vector similarity search for `Postgres`

It supports:
- exact and approximate nearest neighbor search
- L2 distance, inner product, and cosine distance

This notebook shows how to use the Postgres vector database (`PGVector`).

See the [installation instruction](https://github.com/pgvector/pgvector).


```python
# Pip install necessary package
!pip install pgvector
!pip install openai
!pip install psycopg2-binary
!pip install tiktoken
```

    Requirement already satisfied: pgvector in /Users/joyeed/langchain/langchain/.venv/lib/python3.9/site-packages (0.1.8)
    Requirement already satisfied: numpy in /Users/joyeed/langchain/langchain/.venv/lib/python3.9/site-packages (from pgvector) (1.24.3)
    Requirement already satisfied: openai in /Users/joyeed/langchain/langchain/.venv/lib/python3.9/site-packages (0.27.7)
    Requirement already satisfied: requests>=2.20 in /Users/joyeed/langchain/langchain/.venv/lib/python3.9/site-packages (from openai) (2.28.2)
    Requirement already satisfied: tqdm in /Users/joyeed/langchain/langchain/.venv/lib/python3.9/site-packages (from openai) (4.65.0)
    Requirement already satisfied: aiohttp in /Users/joyeed/langchain/langchain/.venv/lib/python3.9/site-packages (from openai) (3.8.4)
    Requirement already satisfied: charset-normalizer<4,>=2 in /Users/joyeed/langchain/langchain/.venv/lib/python3.9/site-packages (from requests>=2.20->openai) (3.1.0)
    Requirement already satisfied: idna<4,>=2.5 in /Users/joyeed/langchain/langchain/.venv/lib/python3.9/site-packages (from requests>=2.20->openai) (3.4)
    Requirement already satisfied: urllib3<1.27,>=1.21.1 in /Users/joyeed/langchain/langchain/.venv/lib/python3.9/site-packages (from requests>=2.20->openai) (1.26.15)
    Requirement already satisfied: certifi>=2017.4.17 in /Users/joyeed/langchain/langchain/.venv/lib/python3.9/site-packages (from requests>=2.20->openai) (2023.5.7)
    Requirement already satisfied: attrs>=17.3.0 in /Users/joyeed/langchain/langchain/.venv/lib/python3.9/site-packages (from aiohttp->openai) (23.1.0)
    Requirement already satisfied: multidict<7.0,>=4.5 in /Users/joyeed/langchain/langchain/.venv/lib/python3.9/site-packages (from aiohttp->openai) (6.0.4)
    Requirement already satisfied: async-timeout<5.0,>=4.0.0a3 in /Users/joyeed/langchain/langchain/.venv/lib/python3.9/site-packages (from aiohttp->openai) (4.0.2)
    Requirement already satisfied: yarl<2.0,>=1.0 in /Users/joyeed/langchain/langchain/.venv/lib/python3.9/site-packages (from aiohttp->openai) (1.9.2)
    Requirement already satisfied: frozenlist>=1.1.1 in /Users/joyeed/langchain/langchain/.venv/lib/python3.9/site-packages (from aiohttp->openai) (1.3.3)
    Requirement already satisfied: aiosignal>=1.1.2 in /Users/joyeed/langchain/langchain/.venv/lib/python3.9/site-packages (from aiohttp->openai) (1.3.1)
    Requirement already satisfied: psycopg2-binary in /Users/joyeed/langchain/langchain/.venv/lib/python3.9/site-packages (2.9.6)
    Requirement already satisfied: tiktoken in /Users/joyeed/langchain/langchain/.venv/lib/python3.9/site-packages (0.4.0)
    Requirement already satisfied: regex>=2022.1.18 in /Users/joyeed/langchain/langchain/.venv/lib/python3.9/site-packages (from tiktoken) (2023.5.5)
    Requirement already satisfied: requests>=2.26.0 in /Users/joyeed/langchain/langchain/.venv/lib/python3.9/site-packages (from tiktoken) (2.28.2)
    Requirement already satisfied: charset-normalizer<4,>=2 in /Users/joyeed/langchain/langchain/.venv/lib/python3.9/site-packages (from requests>=2.26.0->tiktoken) (3.1.0)
    Requirement already satisfied: idna<4,>=2.5 in /Users/joyeed/langchain/langchain/.venv/lib/python3.9/site-packages (from requests>=2.26.0->tiktoken) (3.4)
    Requirement already satisfied: urllib3<1.27,>=1.21.1 in /Users/joyeed/langchain/langchain/.venv/lib/python3.9/site-packages (from requests>=2.26.0->tiktoken) (1.26.15)
    Requirement already satisfied: certifi>=2017.4.17 in /Users/joyeed/langchain/langchain/.venv/lib/python3.9/site-packages (from requests>=2.26.0->tiktoken) (2023.5.7)
    

We want to use `OpenAIEmbeddings` so we have to get the OpenAI API Key.


```python
import os
import getpass

os.environ["OPENAI_API_KEY"] = getpass.getpass("OpenAI API Key:")
```

    OpenAI API Key:········
    


```python
## Loading Environment Variables
from typing import List, Tuple
from dotenv import load_dotenv

load_dotenv()
```




    False




```python
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores.pgvector import PGVector
from langchain.document_loaders import TextLoader
from langchain.docstore.document import Document
```


```python
loader = TextLoader("../../../state_of_the_union.txt")
documents = loader.load()
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
docs = text_splitter.split_documents(documents)

embeddings = OpenAIEmbeddings()
```


```python
## PGVector needs the connection string to the database.
## We will load it from the environment variables.
import os

CONNECTION_STRING = PGVector.connection_string_from_db_params(
    driver=os.environ.get("PGVECTOR_DRIVER", "psycopg2"),
    host=os.environ.get("PGVECTOR_HOST", "localhost"),
    port=int(os.environ.get("PGVECTOR_PORT", "5432")),
    database=os.environ.get("PGVECTOR_DATABASE", "postgres"),
    user=os.environ.get("PGVECTOR_USER", "postgres"),
    password=os.environ.get("PGVECTOR_PASSWORD", "postgres"),
)


## Example
# postgresql+psycopg2://username:password@localhost:5432/database_name
```


```python
# ## PGVector needs the connection string to the database.
# ## We will load it from the environment variables.
# import os
# CONNECTION_STRING = PGVector.connection_string_from_db_params(
#     driver=os.environ.get("PGVECTOR_DRIVER", "psycopg2"),
#     host=os.environ.get("PGVECTOR_HOST", "localhost"),
#     port=int(os.environ.get("PGVECTOR_PORT", "5432")),
#     database=os.environ.get("PGVECTOR_DATABASE", "rd-embeddings"),
#     user=os.environ.get("PGVECTOR_USER", "admin"),
#     password=os.environ.get("PGVECTOR_PASSWORD", "password"),
# )


# ## Example
# # postgresql+psycopg2://username:password@localhost:5432/database_name
```

## Similarity search with score

### Similarity Search with Euclidean Distance (Default)


```python
# The PGVector Module will try to create a table with the name of the collection. So, make sure that the collection name is unique and the user has the
# permission to create a table.

db = PGVector.from_documents(
    embedding=embeddings,
    documents=docs,
    collection_name="state_of_the_union",
    connection_string=CONNECTION_STRING,
)

query = "What did the president say about Ketanji Brown Jackson"
docs_with_score: List[Tuple[Document, float]] = db.similarity_search_with_score(query)
```


```python
for doc, score in docs_with_score:
    print("-" * 80)
    print("Score: ", score)
    print(doc.page_content)
    print("-" * 80)
```

    --------------------------------------------------------------------------------
    Score:  0.6076804864602984
    Tonight. I call on the Senate to: Pass the Freedom to Vote Act. Pass the John Lewis Voting Rights Act. And while you’re at it, pass the Disclose Act so Americans can know who is funding our elections. 
    
    Tonight, I’d like to honor someone who has dedicated his life to serve this country: Justice Stephen Breyer—an Army veteran, Constitutional scholar, and retiring Justice of the United States Supreme Court. Justice Breyer, thank you for your service. 
    
    One of the most serious constitutional responsibilities a President has is nominating someone to serve on the United States Supreme Court. 
    
    And I did that 4 days ago, when I nominated Circuit Court of Appeals Judge Ketanji Brown Jackson. One of our nation’s top legal minds, who will continue Justice Breyer’s legacy of excellence.
    --------------------------------------------------------------------------------
    --------------------------------------------------------------------------------
    Score:  0.6076804864602984
    Tonight. I call on the Senate to: Pass the Freedom to Vote Act. Pass the John Lewis Voting Rights Act. And while you’re at it, pass the Disclose Act so Americans can know who is funding our elections. 
    
    Tonight, I’d like to honor someone who has dedicated his life to serve this country: Justice Stephen Breyer—an Army veteran, Constitutional scholar, and retiring Justice of the United States Supreme Court. Justice Breyer, thank you for your service. 
    
    One of the most serious constitutional responsibilities a President has is nominating someone to serve on the United States Supreme Court. 
    
    And I did that 4 days ago, when I nominated Circuit Court of Appeals Judge Ketanji Brown Jackson. One of our nation’s top legal minds, who will continue Justice Breyer’s legacy of excellence.
    --------------------------------------------------------------------------------
    --------------------------------------------------------------------------------
    Score:  0.659062774389974
    A former top litigator in private practice. A former federal public defender. And from a family of public school educators and police officers. A consensus builder. Since she’s been nominated, she’s received a broad range of support—from the Fraternal Order of Police to former judges appointed by Democrats and Republicans. 
    
    And if we are to advance liberty and justice, we need to secure the Border and fix the immigration system. 
    
    We can do both. At our border, we’ve installed new technology like cutting-edge scanners to better detect drug smuggling.  
    
    We’ve set up joint patrols with Mexico and Guatemala to catch more human traffickers.  
    
    We’re putting in place dedicated immigration judges so families fleeing persecution and violence can have their cases heard faster. 
    
    We’re securing commitments and supporting partners in South and Central America to host more refugees and secure their own borders.
    --------------------------------------------------------------------------------
    --------------------------------------------------------------------------------
    Score:  0.659062774389974
    A former top litigator in private practice. A former federal public defender. And from a family of public school educators and police officers. A consensus builder. Since she’s been nominated, she’s received a broad range of support—from the Fraternal Order of Police to former judges appointed by Democrats and Republicans. 
    
    And if we are to advance liberty and justice, we need to secure the Border and fix the immigration system. 
    
    We can do both. At our border, we’ve installed new technology like cutting-edge scanners to better detect drug smuggling.  
    
    We’ve set up joint patrols with Mexico and Guatemala to catch more human traffickers.  
    
    We’re putting in place dedicated immigration judges so families fleeing persecution and violence can have their cases heard faster. 
    
    We’re securing commitments and supporting partners in South and Central America to host more refugees and secure their own borders.
    --------------------------------------------------------------------------------
    

## Working with vectorstore in PG

### Uploading a vectorstore in PG 


```python
data = docs
api_key = os.environ["OPENAI_API_KEY"]
db = PGVector.from_documents(
    documents=docs,
    embedding=embeddings,
    collection_name=collection_name,
    connection_string=connection_string,
    distance_strategy=DistanceStrategy.COSINE,
    openai_api_key=api_key,
    pre_delete_collection=False,
)
```

### Retrieving a vectorstore in PG


```python
connection_string = CONNECTION_STRING
embedding = embeddings
collection_name = "state_of_the_union"
from langchain.vectorstores.pgvector import DistanceStrategy

store = PGVector(
    connection_string=connection_string,
    embedding_function=embedding,
    collection_name=collection_name,
    distance_strategy=DistanceStrategy.COSINE,
)

retriever = store.as_retriever()
```


```python
print(retriever)
```

    vectorstore=<langchain.vectorstores.pgvector.PGVector object at 0x7fe9a1b1c670> search_type='similarity' search_kwargs={}
    


```python
# When we have an existing PG VEctor
DEFAULT_DISTANCE_STRATEGY = DistanceStrategy.EUCLIDEAN
db1 = PGVector.from_existing_index(
    embedding=embeddings,
    collection_name="state_of_the_union",
    distance_strategy=DEFAULT_DISTANCE_STRATEGY,
    pre_delete_collection=False,
    connection_string=CONNECTION_STRING,
)

query = "What did the president say about Ketanji Brown Jackson"
docs_with_score: List[Tuple[Document, float]] = db1.similarity_search_with_score(query)
print(docs_with_score)
```

    [(Document(page_content='Tonight. I call on the Senate to: Pass the Freedom to Vote Act. Pass the John Lewis Voting Rights Act. And while you’re at it, pass the Disclose Act so Americans can know who is funding our elections. \n\nTonight, I’d like to honor someone who has dedicated his life to serve this country: Justice Stephen Breyer—an Army veteran, Constitutional scholar, and retiring Justice of the United States Supreme Court. Justice Breyer, thank you for your service. \n\nOne of the most serious constitutional responsibilities a President has is nominating someone to serve on the United States Supreme Court. \n\nAnd I did that 4 days ago, when I nominated Circuit Court of Appeals Judge Ketanji Brown Jackson. One of our nation’s top legal minds, who will continue Justice Breyer’s legacy of excellence.', metadata={'source': '../../../state_of_the_union.txt'}), 0.6075870262188066), (Document(page_content='Tonight. I call on the Senate to: Pass the Freedom to Vote Act. Pass the John Lewis Voting Rights Act. And while you’re at it, pass the Disclose Act so Americans can know who is funding our elections. \n\nTonight, I’d like to honor someone who has dedicated his life to serve this country: Justice Stephen Breyer—an Army veteran, Constitutional scholar, and retiring Justice of the United States Supreme Court. Justice Breyer, thank you for your service. \n\nOne of the most serious constitutional responsibilities a President has is nominating someone to serve on the United States Supreme Court. \n\nAnd I did that 4 days ago, when I nominated Circuit Court of Appeals Judge Ketanji Brown Jackson. One of our nation’s top legal minds, who will continue Justice Breyer’s legacy of excellence.', metadata={'source': '../../../state_of_the_union.txt'}), 0.6075870262188066), (Document(page_content='A former top litigator in private practice. A former federal public defender. And from a family of public school educators and police officers. A consensus builder. Since she’s been nominated, she’s received a broad range of support—from the Fraternal Order of Police to former judges appointed by Democrats and Republicans. \n\nAnd if we are to advance liberty and justice, we need to secure the Border and fix the immigration system. \n\nWe can do both. At our border, we’ve installed new technology like cutting-edge scanners to better detect drug smuggling.  \n\nWe’ve set up joint patrols with Mexico and Guatemala to catch more human traffickers.  \n\nWe’re putting in place dedicated immigration judges so families fleeing persecution and violence can have their cases heard faster. \n\nWe’re securing commitments and supporting partners in South and Central America to host more refugees and secure their own borders.', metadata={'source': '../../../state_of_the_union.txt'}), 0.6589478388546668), (Document(page_content='A former top litigator in private practice. A former federal public defender. And from a family of public school educators and police officers. A consensus builder. Since she’s been nominated, she’s received a broad range of support—from the Fraternal Order of Police to former judges appointed by Democrats and Republicans. \n\nAnd if we are to advance liberty and justice, we need to secure the Border and fix the immigration system. \n\nWe can do both. At our border, we’ve installed new technology like cutting-edge scanners to better detect drug smuggling.  \n\nWe’ve set up joint patrols with Mexico and Guatemala to catch more human traffickers.  \n\nWe’re putting in place dedicated immigration judges so families fleeing persecution and violence can have their cases heard faster. \n\nWe’re securing commitments and supporting partners in South and Central America to host more refugees and secure their own borders.', metadata={'source': '../../../state_of_the_union.txt'}), 0.6589478388546668)]
    


```python
for doc, score in docs_with_score:
    print("-" * 80)
    print("Score: ", score)
    print(doc.page_content)
    print("-" * 80)
```

    --------------------------------------------------------------------------------
    Score:  0.6075870262188066
    Tonight. I call on the Senate to: Pass the Freedom to Vote Act. Pass the John Lewis Voting Rights Act. And while you’re at it, pass the Disclose Act so Americans can know who is funding our elections. 
    
    Tonight, I’d like to honor someone who has dedicated his life to serve this country: Justice Stephen Breyer—an Army veteran, Constitutional scholar, and retiring Justice of the United States Supreme Court. Justice Breyer, thank you for your service. 
    
    One of the most serious constitutional responsibilities a President has is nominating someone to serve on the United States Supreme Court. 
    
    And I did that 4 days ago, when I nominated Circuit Court of Appeals Judge Ketanji Brown Jackson. One of our nation’s top legal minds, who will continue Justice Breyer’s legacy of excellence.
    --------------------------------------------------------------------------------
    --------------------------------------------------------------------------------
    Score:  0.6075870262188066
    Tonight. I call on the Senate to: Pass the Freedom to Vote Act. Pass the John Lewis Voting Rights Act. And while you’re at it, pass the Disclose Act so Americans can know who is funding our elections. 
    
    Tonight, I’d like to honor someone who has dedicated his life to serve this country: Justice Stephen Breyer—an Army veteran, Constitutional scholar, and retiring Justice of the United States Supreme Court. Justice Breyer, thank you for your service. 
    
    One of the most serious constitutional responsibilities a President has is nominating someone to serve on the United States Supreme Court. 
    
    And I did that 4 days ago, when I nominated Circuit Court of Appeals Judge Ketanji Brown Jackson. One of our nation’s top legal minds, who will continue Justice Breyer’s legacy of excellence.
    --------------------------------------------------------------------------------
    --------------------------------------------------------------------------------
    Score:  0.6589478388546668
    A former top litigator in private practice. A former federal public defender. And from a family of public school educators and police officers. A consensus builder. Since she’s been nominated, she’s received a broad range of support—from the Fraternal Order of Police to former judges appointed by Democrats and Republicans. 
    
    And if we are to advance liberty and justice, we need to secure the Border and fix the immigration system. 
    
    We can do both. At our border, we’ve installed new technology like cutting-edge scanners to better detect drug smuggling.  
    
    We’ve set up joint patrols with Mexico and Guatemala to catch more human traffickers.  
    
    We’re putting in place dedicated immigration judges so families fleeing persecution and violence can have their cases heard faster. 
    
    We’re securing commitments and supporting partners in South and Central America to host more refugees and secure their own borders.
    --------------------------------------------------------------------------------
    --------------------------------------------------------------------------------
    Score:  0.6589478388546668
    A former top litigator in private practice. A former federal public defender. And from a family of public school educators and police officers. A consensus builder. Since she’s been nominated, she’s received a broad range of support—from the Fraternal Order of Police to former judges appointed by Democrats and Republicans. 
    
    And if we are to advance liberty and justice, we need to secure the Border and fix the immigration system. 
    
    We can do both. At our border, we’ve installed new technology like cutting-edge scanners to better detect drug smuggling.  
    
    We’ve set up joint patrols with Mexico and Guatemala to catch more human traffickers.  
    
    We’re putting in place dedicated immigration judges so families fleeing persecution and violence can have their cases heard faster. 
    
    We’re securing commitments and supporting partners in South and Central America to host more refugees and secure their own borders.
    --------------------------------------------------------------------------------
    


```python

```

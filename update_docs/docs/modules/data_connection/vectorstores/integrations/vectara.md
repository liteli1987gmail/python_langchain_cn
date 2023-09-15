# Vectara

>[Vectara](https://vectara.com/) is a API platform for building LLM-powered applications. It provides a simple to use API for document indexing and query that is managed by Vectara and is optimized for performance and accuracy. 


This notebook shows how to use functionality related to the `Vectara` vector database. 

See the [Vectara API documentation ](https://docs.vectara.com/docs/) for more information on how to use the API.

We want to use `OpenAIEmbeddings` so we have to get the OpenAI API Key.


```python
import os
import getpass

os.environ["OPENAI_API_KEY"] = getpass.getpass("OpenAI API Key:")
```

    OpenAI API Key:········
    


```python
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Vectara
from langchain.document_loaders import TextLoader
```


```python
loader = TextLoader("../../../state_of_the_union.txt")
documents = loader.load()
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
docs = text_splitter.split_documents(documents)

embeddings = OpenAIEmbeddings()
```

## Connecting to Vectara from LangChain

The Vectara API provides simple API endpoints for indexing and querying.


```python
vectara = Vectara.from_documents(docs, embedding=None)
```

## Similarity search

The simplest scenario for using Vectara is to perform a similarity search. 


```python
query = "What did the president say about Ketanji Brown Jackson"
found_docs = vectara.similarity_search(query, n_sentence_context=0)
```


```python
print(found_docs[0].page_content)
```

    Tonight. I call on the Senate to: Pass the Freedom to Vote Act. Pass the John Lewis Voting Rights Act. And while you’re at it, pass the Disclose Act so Americans can know who is funding our elections. 
    
    Tonight, I’d like to honor someone who has dedicated his life to serve this country: Justice Stephen Breyer—an Army veteran, Constitutional scholar, and retiring Justice of the United States Supreme Court. Justice Breyer, thank you for your service. 
    
    One of the most serious constitutional responsibilities a President has is nominating someone to serve on the United States Supreme Court. 
    
    And I did that 4 days ago, when I nominated Circuit Court of Appeals Judge Ketanji Brown Jackson. One of our nation’s top legal minds, who will continue Justice Breyer’s legacy of excellence.
    

## Similarity search with score

Sometimes we might want to perform the search, but also obtain a relevancy score to know how good is a particular result.


```python
query = "What did the president say about Ketanji Brown Jackson"
found_docs = vectara.similarity_search_with_score(query)
```


```python
document, score = found_docs[0]
print(document.page_content)
print(f"\nScore: {score}")
```

    Tonight. I call on the Senate to: Pass the Freedom to Vote Act. Pass the John Lewis Voting Rights Act. And while you’re at it, pass the Disclose Act so Americans can know who is funding our elections. 
    
    Tonight, I’d like to honor someone who has dedicated his life to serve this country: Justice Stephen Breyer—an Army veteran, Constitutional scholar, and retiring Justice of the United States Supreme Court. Justice Breyer, thank you for your service. 
    
    One of the most serious constitutional responsibilities a President has is nominating someone to serve on the United States Supreme Court. 
    
    And I did that 4 days ago, when I nominated Circuit Court of Appeals Judge Ketanji Brown Jackson. One of our nation’s top legal minds, who will continue Justice Breyer’s legacy of excellence.
    
    Score: 0.7129974
    

## Vectara as a Retriever

Vectara, as all the other vector stores, is a LangChain Retriever, by using cosine similarity. 


```python
retriever = vectara.as_retriever()
retriever
```




    VectaraRetriever(vectorstore=<langchain.vectorstores.vectara.Vectara object at 0x122db2830>, search_type='similarity', search_kwargs={'lambda_val': 0.025, 'k': 5, 'filter': '', 'n_sentence_context': '0'})




```python
query = "What did the president say about Ketanji Brown Jackson"
retriever.get_relevant_documents(query)[0]
```




    Document(page_content='Tonight. I call on the Senate to: Pass the Freedom to Vote Act. Pass the John Lewis Voting Rights Act. And while you’re at it, pass the Disclose Act so Americans can know who is funding our elections. \n\nTonight, I’d like to honor someone who has dedicated his life to serve this country: Justice Stephen Breyer—an Army veteran, Constitutional scholar, and retiring Justice of the United States Supreme Court. Justice Breyer, thank you for your service. \n\nOne of the most serious constitutional responsibilities a President has is nominating someone to serve on the United States Supreme Court. \n\nAnd I did that 4 days ago, when I nominated Circuit Court of Appeals Judge Ketanji Brown Jackson. One of our nation’s top legal minds, who will continue Justice Breyer’s legacy of excellence.', metadata={'source': '../../../state_of_the_union.txt'})




```python

```

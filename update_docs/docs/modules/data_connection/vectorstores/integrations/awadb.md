# AwaDB
[AwaDB](https://github.com/awa-ai/awadb) is an AI Native database for the search and storage of embedding vectors used by LLM Applications.
This notebook shows how to use functionality related to the AwaDB.


```python
!pip install awadb
```


```python
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import AwaDB
from langchain.document_loaders import TextLoader
```


```python
loader = TextLoader('../../../state_of_the_union.txt')
documents = loader.load()
text_splitter = CharacterTextSplitter(chunk_size=100, chunk_overlap=0)
docs = text_splitter.split_documents(documents)
```


```python
db = AwaDB.from_documents(docs)
query = "What did the president say about Ketanji Brown Jackson"
docs = db.similarity_search(query)
```


```python
print(docs[0].page_content)
```

    And I did that 4 days ago, when I nominated Circuit Court of Appeals Judge Ketanji Brown Jackson. One of our nation’s top legal minds, who will continue Justice Breyer’s legacy of excellence.
    

## Similarity search with score

The returned distance score is between 0-1. 0 is dissimilar, 1 is the most similar


```python
docs = db.similarity_search_with_score(query)
```


```python
print(docs[0])
```

    (Document(page_content='And I did that 4 days ago, when I nominated Circuit Court of Appeals Judge Ketanji Brown Jackson. One of our nation’s top legal minds, who will continue Justice Breyer’s legacy of excellence.', metadata={'source': '../../../state_of_the_union.txt'}), 0.561813814013747)
    

## Restore the table created and added data before


```python
AwaDB automatically persists added document data
```

If you can restore the table you created and added before, you can just do this as below:


```python
awadb_client = awadb.Client()
ret = awadb_client.Load('langchain_awadb')
if ret : print('awadb load table success')
else:
    print('awadb load table failed')
```
awadb load table success
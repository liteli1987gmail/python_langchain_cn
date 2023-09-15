# Pinecone

>[Pinecone](https://docs.pinecone.io/docs/overview) is a vector database with broad functionality.

This notebook shows how to use functionality related to the `Pinecone` vector database.

To use Pinecone, you must have an API key. 
Here are the [installation instructions](https://docs.pinecone.io/docs/quickstart).


```python
!pip install pinecone-client openai tiktoken
```


```python
import os
import getpass

PINECONE_API_KEY = getpass.getpass("Pinecone API Key:")
```


```python
PINECONE_ENV = getpass.getpass("Pinecone Environment:")
```

We want to use `OpenAIEmbeddings` so we have to get the OpenAI API Key.


```python
os.environ["OPENAI_API_KEY"] = getpass.getpass("OpenAI API Key:")
```


```python
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Pinecone
from langchain.document_loaders import TextLoader
```


```python
from langchain.document_loaders import TextLoader

loader = TextLoader("../../../state_of_the_union.txt")
documents = loader.load()
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
docs = text_splitter.split_documents(documents)

embeddings = OpenAIEmbeddings()
```


```python
import pinecone

# initialize pinecone
pinecone.init(
    api_key=PINECONE_API_KEY,  # find at app.pinecone.io
    environment=PINECONE_ENV,  # next to api key in console
)

index_name = "langchain-demo"

docsearch = Pinecone.from_documents(docs, embeddings, index_name=index_name)

# if you already have an index, you can load it like this
# docsearch = Pinecone.from_existing_index(index_name, embeddings)

query = "What did the president say about Ketanji Brown Jackson"
docs = docsearch.similarity_search(query)
```


```python
print(docs[0].page_content)
```

### Maximal Marginal Relevance Searches

In addition to using similarity search in the retriever object, you can also use `mmr` as retriever.



```python
retriever = docsearch.as_retriever(search_type="mmr")
matched_docs = retriever.get_relevant_documents(query)
for i, d in enumerate(matched_docs):
    print(f"\n## Document {i}\n")
    print(d.page_content)
```

Or use `max_marginal_relevance_search` directly:


```python
found_docs = docsearch.max_marginal_relevance_search(query, k=2, fetch_k=10)
for i, doc in enumerate(found_docs):
    print(f"{i + 1}.", doc.page_content, "\n")
```

# SingleStoreDB
[SingleStoreDB](https://singlestore.com/) is a high-performance distributed SQL database that supports deployment both in the [cloud](https://www.singlestore.com/cloud/) and on-premises. It provides vector storage, and vector functions including [dot_product](https://docs.singlestore.com/managed-service/en/reference/sql-reference/vector-functions/dot_product.html) and [euclidean_distance](https://docs.singlestore.com/managed-service/en/reference/sql-reference/vector-functions/euclidean_distance.html), thereby supporting AI applications that require text similarity matching. This tutorial illustrates how to [work with vector data in SingleStoreDB](https://docs.singlestore.com/managed-service/en/developer-resources/functional-extensions/working-with-vector-data.html).


```python
# Establishing a connection to the database is facilitated through the singlestoredb Python connector.
# Please ensure that this connector is installed in your working environment.
!pip install singlestoredb
```


```python
import os
import getpass

# We want to use OpenAIEmbeddings so we have to get the OpenAI API Key.
os.environ["OPENAI_API_KEY"] = getpass.getpass("OpenAI API Key:")
```


```python
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import SingleStoreDB
from langchain.document_loaders import TextLoader
```


```python
# Load text samples 
loader = TextLoader('../../../state_of_the_union.txt')
documents = loader.load()
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
docs = text_splitter.split_documents(documents)

embeddings = OpenAIEmbeddings()
```

There are several ways to establish a [connection](https://singlestoredb-python.labs.singlestore.com/generated/singlestoredb.connect.html) to the database. You can either set up environment variables or pass named parameters to the `SingleStoreDB constructor`. Alternatively, you may provide these parameters to the `from_documents` and `from_texts` methods.


```python
# Setup connection url as environment variable
os.environ["SINGLESTOREDB_URL"] = "root:pass@localhost:3306/db"

# Load documents to the store
docsearch = SingleStoreDB.from_documents(
    docs,
    embeddings,
    table_name = "notebook", # use table with a custom name 
)
```


```python
query = "What did the president say about Ketanji Brown Jackson"
docs = docsearch.similarity_search(query)  # Find documents that correspond to the query
print(docs[0].page_content)
```


```python

```

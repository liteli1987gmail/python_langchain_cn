# Tair

>[Tair](https://www.alibabacloud.com/help/en/tair/latest/what-is-tair) is a cloud native in-memory database service developed by `Alibaba Cloud`. 
It provides rich data models and enterprise-grade capabilities to support your real-time online scenarios while maintaining full compatibility with open source `Redis`. `Tair` also introduces persistent memory-optimized instances that are based on the new non-volatile memory (NVM) storage medium.

This notebook shows how to use functionality related to the `Tair` vector database.

To run, you should have a `Tair` instance up and running.


```python
from langchain.embeddings.fake import FakeEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Tair
```


```python
from langchain.document_loaders import TextLoader

loader = TextLoader("../../../state_of_the_union.txt")
documents = loader.load()
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
docs = text_splitter.split_documents(documents)

embeddings = FakeEmbeddings(size=128)
```

Connect to Tair using the `TAIR_URL` environment variable 
```
export TAIR_URL="redis://{username}:{password}@{tair_address}:{tair_port}"
```

or the keyword argument `tair_url`.

Then store documents and embeddings into Tair.


```python
tair_url = "redis://localhost:6379"

# drop first if index already exists
Tair.drop_index(tair_url=tair_url)

vector_store = Tair.from_documents(docs, embeddings, tair_url=tair_url)
```

Query similar documents.


```python
query = "What did the president say about Ketanji Brown Jackson"
docs = vector_store.similarity_search(query)
docs[0]
```




    Document(page_content='We’re going after the criminals who stole billions in relief money meant for small businesses and millions of Americans.  \n\nAnd tonight, I’m announcing that the Justice Department will name a chief prosecutor for pandemic fraud. \n\nBy the end of this year, the deficit will be down to less than half what it was before I took office.  \n\nThe only president ever to cut the deficit by more than one trillion dollars in a single year. \n\nLowering your costs also means demanding more competition. \n\nI’m a capitalist, but capitalism without competition isn’t capitalism. \n\nIt’s exploitation—and it drives up prices. \n\nWhen corporations don’t have to compete, their profits go up, your prices go up, and small businesses and family farmers and ranchers go under. \n\nWe see it happening with ocean carriers moving goods in and out of America. \n\nDuring the pandemic, these foreign-owned companies raised prices by as much as 1,000% and made record profits.', metadata={'source': '../../../state_of_the_union.txt'})




```python

```

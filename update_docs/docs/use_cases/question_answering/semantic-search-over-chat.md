# Question answering over a group chat messages
In this tutorial, we are going to use Langchain + Deep Lake with GPT4 to semantically search and ask questions over a group chat.

View a working demo [here](https://twitter.com/thisissukh_/status/1647223328363679745)

## 1. Install required packages


```python
!python3 -m pip install --upgrade langchain deeplake openai tiktoken
```

## 2. Add API keys




```python
import os
import getpass
from langchain.document_loaders import PyPDFLoader, TextLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import (
    RecursiveCharacterTextSplitter,
    CharacterTextSplitter,
)
from langchain.vectorstores import DeepLake
from langchain.chains import ConversationalRetrievalChain, RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAI

os.environ["OPENAI_API_KEY"] = getpass.getpass("OpenAI API Key:")
os.environ["ACTIVELOOP_TOKEN"] = getpass.getpass("Activeloop Token:")
os.environ["ACTIVELOOP_ORG"] = getpass.getpass("Activeloop Org:")

org = os.environ["ACTIVELOOP_ORG"]
embeddings = OpenAIEmbeddings()

dataset_path = "hub://" + org + "/data"
```



## 2. Create sample data

You can generate a sample group chat conversation using ChatGPT with this prompt:

```
Generate a group chat conversation with three friends talking about their day, referencing real places and fictional names. Make it funny and as detailed as possible.
```

I've already generated such a chat in `messages.txt`. We can keep it simple and use this for our example.

## 3. Ingest chat embeddings

We load the messages in the text file, chunk and upload to ActiveLoop Vector store.


```python
with open("messages.txt") as f:
    state_of_the_union = f.read()
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
pages = text_splitter.split_text(state_of_the_union)

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
texts = text_splitter.create_documents(pages)

print(texts)

dataset_path = "hub://" + org + "/data"
embeddings = OpenAIEmbeddings()
db = DeepLake.from_documents(
    texts, embeddings, dataset_path=dataset_path, overwrite=True
)
```

## 4. Ask questions

Now we can ask a question and get an answer back with a semantic search:


```python
db = DeepLake(dataset_path=dataset_path, read_only=True, embedding_function=embeddings)

retriever = db.as_retriever()
retriever.search_kwargs["distance_metric"] = "cos"
retriever.search_kwargs["k"] = 4

qa = RetrievalQA.from_chain_type(
    llm=OpenAI(), chain_type="stuff", retriever=retriever, return_source_documents=False
)

# What was the restaurant the group was talking about called?
query = input("Enter query:")

# The Hungry Lobster
ans = qa({"query": query})

print(ans)
```


```python

```

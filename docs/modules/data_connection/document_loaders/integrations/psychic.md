# Psychic
This notebook covers how to load documents from `Psychic`. See [here](../../../../ecosystem/psychic.md) for more details.

## Prerequisites
1. Follow the Quick Start section in [this document](../../../../ecosystem/psychic.md)
2. Log into the [Psychic dashboard](https://dashboard.psychic.dev/) and get your secret key
3. Install the frontend react library into your web app and have a user authenticate a connection. The connection will be created using the connection id that you specify.

## Loading documents

Use the `PsychicLoader` class to load in documents from a connection. Each connection has a connector id (corresponding to the SaaS app that was connected) and a connection id (which you passed in to the frontend library).


```python
# Uncomment this to install psychicapi if you don't already have it installed
!poetry run pip -q install psychicapi
```

    
    [1m[[0m[34;49mnotice[0m[1;39;49m][0m[39;49m A new release of pip is available: [0m[31;49m23.0.1[0m[39;49m -> [0m[32;49m23.1.2[0m
    [1m[[0m[34;49mnotice[0m[1;39;49m][0m[39;49m To update, run: [0m[32;49mpip install --upgrade pip[0m
    


```python
from langchain.document_loaders import PsychicLoader
from psychicapi import ConnectorId

# Create a document loader for google drive. We can also load from other connectors by setting the connector_id to the appropriate value e.g. ConnectorId.notion.value
# This loader uses our test credentials
google_drive_loader = PsychicLoader(
    api_key="7ddb61c1-8b6a-4d31-a58e-30d1c9ea480e",
    connector_id=ConnectorId.gdrive.value,
    connection_id="google-test",
)

documents = google_drive_loader.load()
```

## Converting the docs to embeddings 

We can now convert these documents into embeddings and store them in a vector database like Chroma


```python
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.text_splitter import CharacterTextSplitter
from langchain.llms import OpenAI
from langchain.chains import RetrievalQAWithSourcesChain
```


```python
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
texts = text_splitter.split_documents(documents)

embeddings = OpenAIEmbeddings()
docsearch = Chroma.from_documents(texts, embeddings)
chain = RetrievalQAWithSourcesChain.from_chain_type(
    OpenAI(temperature=0), chain_type="stuff", retriever=docsearch.as_retriever()
)
chain({"question": "what is psychic?"}, return_only_outputs=True)
```

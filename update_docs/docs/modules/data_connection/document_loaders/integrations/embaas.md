# Embaas
[embaas](https://embaas.io) is a fully managed NLP API service that offers features like embedding generation, document text extraction, document to embeddings and more. You can choose a [variety of pre-trained models](https://embaas.io/docs/models/embeddings).

### Prerequisites
Create a free embaas account at [https://embaas.io/register](https://embaas.io/register) and generate an [API key](https://embaas.io/dashboard/api-keys)

### Document Text Extraction API
The document text extraction API allows you to extract the text from a given document. The API supports a variety of document formats, including PDF, mp3, mp4 and more. For a full list of supported formats, check out the API docs (link below).


```python
# Set API key
embaas_api_key = "YOUR_API_KEY"
# or set environment variable
os.environ["EMBAAS_API_KEY"] = "YOUR_API_KEY"
```

#### Using a blob (bytes)


```python
from langchain.document_loaders.embaas import EmbaasBlobLoader
from langchain.document_loaders.blob_loaders import Blob
```


```python
blob_loader = EmbaasBlobLoader()
blob = Blob.from_path("example.pdf")
documents = blob_loader.load(blob)
```


```python
# You can also directly create embeddings with your preferred embeddings model
blob_loader = EmbaasBlobLoader(params={"model": "e5-large-v2", "should_embed": True})
blob = Blob.from_path("example.pdf")
documents = blob_loader.load(blob)

print(documents[0]["metadata"]["embedding"])
```

#### Using a file


```python
from langchain.document_loaders.embaas import EmbaasLoader
```


```python
file_loader = EmbaasLoader(file_path="example.pdf")
documents = file_loader.load()
```


```python
# Disable automatic text splitting
file_loader = EmbaasLoader(file_path="example.mp3", params={"should_chunk": False})
documents = file_loader.load()
```

For more detailed information about the embaas document text extraction API, please refer to [the official embaas API documentation](https://embaas.io/api-reference).

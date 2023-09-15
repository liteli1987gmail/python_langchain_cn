# Elasticsearch
Walkthrough of how to generate embeddings using a hosted embedding model in Elasticsearch

The easiest way to instantiate the `ElasticsearchEmebddings` class it either
- using the `from_credentials` constructor if you are using Elastic Cloud
- or using the `from_es_connection` constructor with any Elasticsearch cluster


```python
!pip -q install elasticsearch langchain
```


```python
import elasticsearch
from langchain.embeddings.elasticsearch import ElasticsearchEmbeddings
```


```python
# Define the model ID
model_id = "your_model_id"
```

## Testing with `from_credentials`
This required an Elastic Cloud `cloud_id`


```python
# Instantiate ElasticsearchEmbeddings using credentials
embeddings = ElasticsearchEmbeddings.from_credentials(
    model_id,
    es_cloud_id="your_cloud_id",
    es_user="your_user",
    es_password="your_password",
)
```


```python
# Create embeddings for multiple documents
documents = [
    "This is an example document.",
    "Another example document to generate embeddings for.",
]
document_embeddings = embeddings.embed_documents(documents)
```


```python
# Print document embeddings
for i, embedding in enumerate(document_embeddings):
    print(f"Embedding for document {i+1}: {embedding}")
```


```python
# Create an embedding for a single query
query = "This is a single query."
query_embedding = embeddings.embed_query(query)
```


```python
# Print query embedding
print(f"Embedding for query: {query_embedding}")
```

## Testing with Existing Elasticsearch client connection
This can be used with any Elasticsearch deployment


```python
# Create Elasticsearch connection
es_connection = Elasticsearch(
    hosts=["https://es_cluster_url:port"], basic_auth=("user", "password")
)
```


```python
# Instantiate ElasticsearchEmbeddings using es_connection
embeddings = ElasticsearchEmbeddings.from_es_connection(
    model_id,
    es_connection,
)
```


```python
# Create embeddings for multiple documents
documents = [
    "This is an example document.",
    "Another example document to generate embeddings for.",
]
document_embeddings = embeddings.embed_documents(documents)
```


```python
# Print document embeddings
for i, embedding in enumerate(document_embeddings):
    print(f"Embedding for document {i+1}: {embedding}")
```


```python
# Create an embedding for a single query
query = "This is a single query."
query_embedding = embeddings.embed_query(query)
```


```python
# Print query embedding
print(f"Embedding for query: {query_embedding}")
```

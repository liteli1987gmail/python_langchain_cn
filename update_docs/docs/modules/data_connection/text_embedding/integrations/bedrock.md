# Bedrock Embeddings


```python
%pip install boto3
```


```python
from langchain.embeddings import BedrockEmbeddings

embeddings = BedrockEmbeddings(credentials_profile_name="bedrock-admin")
```


```python
embeddings.embed_query("This is a content of the document")
```


```python
embeddings.embed_documents(["This is a content of the document"])
```

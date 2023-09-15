# AWS Kendra

> AWS Kendra is an intelligent search service provided by Amazon Web Services (AWS). It utilizes advanced natural language processing (NLP) and machine learning algorithms to enable powerful search capabilities across various data sources within an organization. Kendra is designed to help users find the information they need quickly and accurately, improving productivity and decision-making.

> With Kendra, users can search across a wide range of content types, including documents, FAQs, knowledge bases, manuals, and websites. It supports multiple languages and can understand complex queries, synonyms, and contextual meanings to provide highly relevant search results.

## Using the AWS Kendra Index Retriever


```python
#!pip install boto3
```


```python
import boto3
from langchain.retrievers import AwsKendraIndexRetriever
```

Create New Retriever


```python
kclient = boto3.client("kendra", region_name="us-east-1")

retriever = AwsKendraIndexRetriever(
    kclient=kclient,
    kendraindex="kendraindex",
)
```

Now you can use retrieved documents from AWS Kendra Index


```python
retriever.get_relevant_documents("what is langchain")
```

# Weaviate Hybrid Search

>[Weaviate](https://weaviate.io/developers/weaviate) is an open source vector database.

>[Hybrid search](https://weaviate.io/blog/hybrid-search-explained) is a technique that combines multiple search algorithms to improve the accuracy and relevance of search results. It uses the best features of both keyword-based search algorithms with vector search techniques.

>The `Hybrid search in Weaviate` uses sparse and dense vectors to represent the meaning and context of search queries and documents.

This notebook shows how to use `Weaviate hybrid search` as a LangChain retriever.

Set up the retriever:


```python
#!pip install weaviate-client
```


```python
import weaviate
import os

WEAVIATE_URL = os.getenv("WEAVIATE_URL")
client = weaviate.Client(
    url=WEAVIATE_URL,
    auth_client_secret=weaviate.AuthApiKey(api_key=os.getenv("WEAVIATE_API_KEY")),
    additional_headers={
        "X-Openai-Api-Key": os.getenv("OPENAI_API_KEY"),
    },
)

# client.schema.delete_all()
```


```python
from langchain.retrievers.weaviate_hybrid_search import WeaviateHybridSearchRetriever
from langchain.schema import Document
```

    /workspaces/langchain/langchain/vectorstores/analyticdb.py:20: MovedIn20Warning: The ``declarative_base()`` function is now available as sqlalchemy.orm.declarative_base(). (deprecated since: 2.0) (Background on SQLAlchemy 2.0 at: https://sqlalche.me/e/b8d9)
      Base = declarative_base()  # type: Any
    


```python
retriever = WeaviateHybridSearchRetriever(
    client, index_name="LangChain", text_key="text"
)
```

Add some data:


```python
docs = [
    Document(
        metadata={
            "title": "Embracing The Future: AI Unveiled",
            "author": "Dr. Rebecca Simmons",
        },
        page_content="A comprehensive analysis of the evolution of artificial intelligence, from its inception to its future prospects. Dr. Simmons covers ethical considerations, potentials, and threats posed by AI.",
    ),
    Document(
        metadata={
            "title": "Symbiosis: Harmonizing Humans and AI",
            "author": "Prof. Jonathan K. Sterling",
        },
        page_content="Prof. Sterling explores the potential for harmonious coexistence between humans and artificial intelligence. The book discusses how AI can be integrated into society in a beneficial and non-disruptive manner.",
    ),
    Document(
        metadata={"title": "AI: The Ethical Quandary", "author": "Dr. Rebecca Simmons"},
        page_content="In her second book, Dr. Simmons delves deeper into the ethical considerations surrounding AI development and deployment. It is an eye-opening examination of the dilemmas faced by developers, policymakers, and society at large.",
    ),
    Document(
        metadata={
            "title": "Conscious Constructs: The Search for AI Sentience",
            "author": "Dr. Samuel Cortez",
        },
        page_content="Dr. Cortez takes readers on a journey exploring the controversial topic of AI consciousness. The book provides compelling arguments for and against the possibility of true AI sentience.",
    ),
    Document(
        metadata={
            "title": "Invisible Routines: Hidden AI in Everyday Life",
            "author": "Prof. Jonathan K. Sterling",
        },
        page_content="In his follow-up to 'Symbiosis', Prof. Sterling takes a look at the subtle, unnoticed presence and influence of AI in our everyday lives. It reveals how AI has become woven into our routines, often without our explicit realization.",
    ),
]
```


```python
retriever.add_documents(docs)
```




    ['eda16d7d-437d-4613-84ae-c2e38705ec7a',
     '04b501bf-192b-4e72-be77-2fbbe7e67ebf',
     '18a1acdb-23b7-4482-ab04-a6c2ed51de77',
     '88e82cc3-c020-4b5a-b3c6-ca7cf3fc6a04',
     'f6abd9d5-32ed-46c4-bd08-f8d0f7c9fc95']



Do a hybrid search:


```python
retriever.get_relevant_documents("the ethical implications of AI")
```




    [Document(page_content='In her second book, Dr. Simmons delves deeper into the ethical considerations surrounding AI development and deployment. It is an eye-opening examination of the dilemmas faced by developers, policymakers, and society at large.', metadata={}),
     Document(page_content='A comprehensive analysis of the evolution of artificial intelligence, from its inception to its future prospects. Dr. Simmons covers ethical considerations, potentials, and threats posed by AI.', metadata={}),
     Document(page_content="In his follow-up to 'Symbiosis', Prof. Sterling takes a look at the subtle, unnoticed presence and influence of AI in our everyday lives. It reveals how AI has become woven into our routines, often without our explicit realization.", metadata={}),
     Document(page_content='Prof. Sterling explores the potential for harmonious coexistence between humans and artificial intelligence. The book discusses how AI can be integrated into society in a beneficial and non-disruptive manner.', metadata={})]



Do a hybrid search with where filter:


```python
retriever.get_relevant_documents(
    "AI integration in society",
    where_filter={
        "path": ["author"],
        "operator": "Equal",
        "valueString": "Prof. Jonathan K. Sterling",
    },
)
```




    [Document(page_content='Prof. Sterling explores the potential for harmonious coexistence between humans and artificial intelligence. The book discusses how AI can be integrated into society in a beneficial and non-disruptive manner.', metadata={}),
     Document(page_content="In his follow-up to 'Symbiosis', Prof. Sterling takes a look at the subtle, unnoticed presence and influence of AI in our everyday lives. It reveals how AI has become woven into our routines, often without our explicit realization.", metadata={})]



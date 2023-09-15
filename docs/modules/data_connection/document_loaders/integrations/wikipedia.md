# Wikipedia

>[Wikipedia](https://wikipedia.org/) is a multilingual free online encyclopedia written and maintained by a community of volunteers, known as Wikipedians, through open collaboration and using a wiki-based editing system called MediaWiki. `Wikipedia` is the largest and most-read reference work in history.

This notebook shows how to load wiki pages from `wikipedia.org` into the Document format that we use downstream.

## Installation

First, you need to install `wikipedia` python package.


```python
#!pip install wikipedia
```

## Examples

`WikipediaLoader` has these arguments:
- `query`: free text which used to find documents in Wikipedia
- optional `lang`: default="en". Use it to search in a specific language part of Wikipedia
- optional `load_max_docs`: default=100. Use it to limit number of downloaded documents. It takes time to download all 100 documents, so use a small number for experiments. There is a hard limit of 300 for now.
- optional `load_all_available_meta`: default=False. By default only the most important fields downloaded: `Published` (date when document was published/last updated), `title`, `Summary`. If True, other fields also downloaded.


```python
from langchain.document_loaders import WikipediaLoader
```


```python
docs = WikipediaLoader(query="HUNTER X HUNTER", load_max_docs=2).load()
len(docs)
```


```python
docs[0].metadata  # meta-information of the Document
```


```python
docs[0].page_content[:400]  # a content of the Document
```
